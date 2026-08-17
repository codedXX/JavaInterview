from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "01-Redis" / "Redis面试题-参考回答.md"
OUTPUT = ROOT / "01-Redis" / "Redis面试题-参考回答.pdf"
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"


def inline(value: str) -> str:
    value = html.escape(value)
    value = value.replace("⭐⭐", "重点问题：").replace("⭐", "重点问题：")
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`(.+?)`", r'<font face="STHeiti" color="#9D3434">\1</font>', value)
    return value.replace("  ", "&nbsp;&nbsp;")


def strip_quote(line: str) -> str:
    if line.startswith(">"):
        return line[1:].lstrip()
    return line


def page_chrome(canvas, document):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#B42318"))
    canvas.setLineWidth(1)
    canvas.line(document.leftMargin, height - 0.48 * inch, width - document.rightMargin, height - 0.48 * inch)
    canvas.setFont("STHeiti", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(document.leftMargin, height - 0.35 * inch, "Redis 面试题参考回答")
    canvas.drawRightString(width - document.rightMargin, 0.36 * inch, f"第 {document.page} 页")
    canvas.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "DocTitle", parent=base["Title"], fontName="STHeiti", fontSize=25,
            leading=32, alignment=TA_CENTER, textColor=colors.HexColor("#B42318"), spaceAfter=14,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName="STHeiti", fontSize=10,
            leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#6B7280"), spaceAfter=26,
        ),
        "question": ParagraphStyle(
            "Question", parent=base["Normal"], fontName="STHeiti", fontSize=12,
            leading=19, textColor=colors.HexColor("#8E1F18"), backColor=colors.HexColor("#FFF3F0"),
            borderColor=colors.HexColor("#F5C2B8"), borderWidth=0.6, borderPadding=8,
            spaceBefore=10, spaceAfter=8,
        ),
        "answer_label": ParagraphStyle(
            "AnswerLabel", parent=base["Normal"], fontName="STHeiti", fontSize=10,
            leading=14, textColor=colors.HexColor("#0F5E77"), spaceBefore=3, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="STHeiti", fontSize=10.5,
            leading=18, textColor=colors.HexColor("#20242A"), spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="STHeiti", fontSize=10.5,
            leading=18, leftIndent=17, firstLineIndent=-11, textColor=colors.HexColor("#20242A"), spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "Code", parent=base["Code"], fontName="STHeiti", fontSize=8.5,
            leading=13, leftIndent=8, rightIndent=8, textColor=colors.HexColor("#343A40"),
            backColor=colors.HexColor("#F5F6F8"), borderColor=colors.HexColor("#E1E4E8"),
            borderWidth=0.5, borderPadding=7, spaceBefore=3, spaceAfter=9,
        ),
        "image_note": ParagraphStyle(
            "ImageNote", parent=base["Normal"], fontName="STHeiti", fontSize=8,
            leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#6B7280"), spaceAfter=9,
        ),
    }


def document_story():
    styles = build_styles()
    story = [
        Spacer(1, 0.42 * inch),
        Paragraph("Redis 相关面试题", styles["title"]),
        Paragraph("参考回答", styles["subtitle"]),
    ]
    lines = [strip_quote(line.rstrip()) for line in SOURCE.read_text(encoding="utf-8").splitlines()]
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    paragraph = []
    code = []
    in_code = False

    def flush_paragraph():
        nonlocal paragraph
        if not paragraph:
            return
        text = " ".join(part.strip() for part in paragraph).strip()
        paragraph = []
        if not text:
            return
        interviewer = re.match(r"\*\*面试官\*\*：?(.*)", text)
        candidate = re.match(r"\*\*候选人\*\*：?(.*)", text)
        if interviewer:
            story.append(Paragraph("面试官：" + inline(interviewer.group(1).strip()), styles["question"]))
        elif candidate:
            story.append(Paragraph("候选人：" + inline(candidate.group(1).strip()), styles["answer_label"]))
        elif text.startswith("重点问题：") or text.startswith("【"):
            story.append(Paragraph(inline(text), styles["question"]))
        elif re.match(r"(?:[-*]|[0-9]+\.)\s+", text):
            item = re.sub(r"^(?:[-*]|[0-9]+\.)\s+", "", text)
            story.append(Paragraph("• " + inline(item), styles["bullet"]))
        else:
            story.append(Paragraph(inline(text), styles["body"]))

    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code), styles["code"]))
                code = []
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        image_match = re.fullmatch(r"!\[[^]]*\]\(([^)]+)\)", line.strip())
        if image_match:
            flush_paragraph()
            image_path = SOURCE.parent / image_match.group(1)
            if image_path.exists():
                image = Image(str(image_path))
                image._restrictSize(6.55 * inch, 4.55 * inch)
                story.append(image)
                story.append(Paragraph("示意图", styles["image_note"]))
            continue
        if not line.strip():
            flush_paragraph()
            continue
        if re.match(r"(?:[-*]|[0-9]+\.)\s+", line.strip()):
            flush_paragraph()
            story.append(Paragraph("• " + inline(re.sub(r"^(?:[-*]|[0-9]+\.)\s+", "", line.strip())), styles["bullet"]))
            continue
        if re.match(r"\*\*(?:面试官|候选人)\*\*：", line.strip()) or line.startswith("⭐"):
            flush_paragraph()
        paragraph.append(line)
    flush_paragraph()
    if in_code and code:
        story.append(Preformatted("\n".join(code), styles["code"]))
    return story


def main():
    pdfmetrics.registerFont(TTFont("STHeiti", FONT_PATH, subfontIndex=0))
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=0.72 * inch, rightMargin=0.72 * inch,
        topMargin=0.74 * inch, bottomMargin=0.66 * inch, title="Redis 相关面试题", author="JavaInterview",
    )
    document.build(document_story(), onFirstPage=page_chrome, onLaterPages=page_chrome)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
