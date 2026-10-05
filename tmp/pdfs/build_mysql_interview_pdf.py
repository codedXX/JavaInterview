"""Regenerate the MySQL handout using the existing PDF's typography."""
from pathlib import Path
import re

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import KeepTogether, SimpleDocTemplate, XPreformatted

import build_batch_interview_pdfs as layout
import build_redis_interview_pdf as typography


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "02-数据库/MySQL面试题-参考回答.md"
OUTPUT = SOURCE.with_suffix(".pdf")
REFERENCE = ROOT / "tmp/pdfs/mysql-reference/original.pdf"
STAGING = ROOT / "tmp/pdfs/MySQL面试题-参考回答-new.pdf"
WIDTH = A4[0] - 1.44 * inch


def inline(text):
    text = re.sub(r"(?:⭐\ufe0f?)+", "重点问题：", text)
    return typography.inline(text)


def quote_text(raw):
    depth = 0
    probe = raw.lstrip()
    while probe.startswith(">"):
        depth += 1
        probe = probe[1:].lstrip()
    return typography.strip_quote(raw).rstrip(), depth


def code_block(text, style):
    lines = []
    for line in text.split("\n"):
        current = ""
        width = 0
        for char in line.expandtabs(4):
            advance = pdfmetrics.stringWidth(
                char, typography.CHAR_FONTS.get(char, "HeitiFallback"), style.fontSize
            )
            if current and width + advance > WIDTH - 32:
                lines.append(current)
                current = "    "
                width = pdfmetrics.stringWidth(current, "STHeiti", style.fontSize)
            current += char
            width += advance
        lines.append(current)
    block = XPreformatted("\n".join(typography.font_text(line) for line in lines), style)
    return KeepTogether([block]) if len(lines) <= 12 else block


def build():
    typography.SOURCE = SOURCE
    typography.REFERENCE = REFERENCE
    typography.register_fonts()
    layout.inline = inline
    layout.quote_text = quote_text
    layout.Preformatted = code_block
    original_styles = layout.styles

    def styles():
        result = original_styles()
        for name, style in result.items():
            if name != "code":
                style.wordWrap = "CJK"
            if name in ("question", "answer"):
                style.keepWithNext = True
        return result

    layout.styles = styles
    document = SimpleDocTemplate(
        str(STAGING), pagesize=A4,
        leftMargin=0.72 * inch, rightMargin=0.72 * inch,
        topMargin=0.74 * inch, bottomMargin=0.66 * inch,
        title=SOURCE.stem, author="JavaInterview",
    )
    document.doc_title = SOURCE.stem
    document.build(
        layout.build_story(SOURCE, WIDTH),
        onFirstPage=typography.page_chrome, onLaterPages=typography.page_chrome,
    )
    reader = PdfReader(STAGING)
    print(f"Built {len(reader.pages)} pages: {STAGING}")


if __name__ == "__main__":
    build()
