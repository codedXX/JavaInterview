from pathlib import Path
import html
import re
import struct
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, XPreformatted
from pypdf import PdfReader
from build_batch_interview_pdfs import make_table


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "01-Redis" / "Redis面试题-参考回答.md"
OUTPUT = ROOT / "01-Redis" / "Redis面试题-参考回答.pdf"
REFERENCE = ROOT / "tmp/pdfs/current-reference/original.pdf"
FONT_PATH = "C:/Windows/Fonts/simhei.ttf"
CHAR_FONTS = {}
RENDERED_TEXT = []


def register_fonts():
    """Reuse the reference's embedded glyphs; use Windows Heiti for new ones."""
    pdfmetrics.registerFont(TTFont("HeitiFallback", FONT_PATH))
    pdfmetrics.registerFontFamily("HeitiFallback", normal="HeitiFallback", bold="HeitiFallback", italic="HeitiFallback", boldItalic="HeitiFallback")
    seen = set()
    for page in PdfReader(REFERENCE).pages:
        for entry in page["/Resources"]["/Font"].values():
            resource = entry.get_object()
            name = str(resource.get("/BaseFont", ""))
            if name in seen or "STHeiti" not in name:
                continue
            seen.add(name)
            font_name = "STHeiti" if len(seen) == 1 else f"STHeiti{len(seen)}"
            font = TTFont(font_name, BytesIO(resource["/FontDescriptor"]["/FontFile2"].get_data()))
            # ReportLab embeds a format-6 cmap indexed by the PDF byte code.
            cmap = font.face.get_table("cmap")
            offset = struct.unpack_from(">I", cmap, 8)[0]
            fmt, _, _, first, count = struct.unpack_from(">5H", cmap, offset)
            if fmt != 6:
                raise ValueError("Unsupported reference cmap")
            glyphs = struct.unpack_from(f">{count}H", cmap, offset + 10)
            mapping = dict((int(a, 16), int(b, 16)) for a, b in re.findall(rb"<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{4})>", resource["/ToUnicode"].get_data()))
            font.face.charToGlyph = {unicode: glyphs[byte - first] for byte, unicode in mapping.items() if first <= byte < first + count}
            font.face.charWidths = {unicode: font.face.hmetrics[glyph][0] * 1000 / font.face.unitsPerEm for unicode, glyph in font.face.charToGlyph.items()}
            font.face.name = font_name.encode("ascii")
            if 32 in font.face.charToGlyph:
                font.face.charToGlyph[160] = font.face.charToGlyph[32]
                font.face.charWidths[160] = font.face.charWidths[32]
            pdfmetrics.registerFont(font)
            pdfmetrics.registerFontFamily(font_name, normal=font_name, bold=font_name, italic=font_name, boldItalic=font_name)
            for unicode in font.face.charToGlyph:
                CHAR_FONTS.setdefault(chr(unicode), font_name)
    if not CHAR_FONTS:
        raise ValueError("No reference fonts found")


def font_text(value):
    runs = []
    current = None
    buffer = []
    for char in value:
        font = CHAR_FONTS.get(char, "HeitiFallback")
        if current and font != current:
            runs.append(f'<font face="{current}">{html.escape("".join(buffer))}</font>')
            buffer = []
        current = font
        buffer.append(char)
    if buffer:
        runs.append(f'<font face="{current}">{html.escape("".join(buffer))}</font>')
    return "".join(runs)


def inline(value: str) -> str:
    value = value.replace("⭐⭐", "重点问题：").replace("⭐️", "重点问题：").replace("⭐", "重点问题：")
    pattern = r"(\*\*.+?\*\*|`[^`]+`|\[[^]]+\]\([^)]+\))"
    result = []
    for part in re.split(pattern, value):
        if part.startswith("**") and part.endswith("**"):
            result.append("<b>" + inline(part[2:-2]) + "</b>")
        elif part.startswith("`") and part.endswith("`"):
            result.append('<font color="#9D3434">' + font_text(part[1:-1]) + "</font>")
        elif match := re.fullmatch(r"\[([^]]+)\]\(([^)]+)\)", part):
            result.append(f'<link href="{html.escape(match.group(2), quote=True)}" color="#0F5E77">{font_text(match.group(1))}</link>')
        else:
            result.append(font_text(part))
    return "".join(result)


def strip_quote(line: str) -> str:
    while line.lstrip().startswith(">"):
        line = line.lstrip()[1:]
        if line.startswith(" "):
            line = line[1:]
    return line


def page_chrome(canvas, document):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#B42318"))
    canvas.setLineWidth(1)
    canvas.line(document.leftMargin, height - 0.48 * inch, width - document.rightMargin, height - 0.48 * inch)
    canvas.setFont("STHeiti", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    header = Paragraph(inline(SOURCE.stem), ParagraphStyle("Header", fontName="STHeiti", fontSize=8, leading=10, textColor=colors.HexColor("#6B7280")))
    header.wrap(document.width, 12)
    header.drawOn(canvas, document.leftMargin, height - 0.35 * inch - 1.6)
    footer = Paragraph(inline(f"第 {document.page} 页"), ParagraphStyle("Footer", fontName="STHeiti", fontSize=8, leading=10, textColor=colors.HexColor("#6B7280"), alignment=2))
    footer.wrap(document.width, 12)
    footer.drawOn(canvas, document.leftMargin, 0.36 * inch - 1.6)
    canvas.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    styles = {
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
            spaceBefore=10, spaceAfter=8, keepWithNext=True,
        ),
        "answer_label": ParagraphStyle(
            "AnswerLabel", parent=base["Normal"], fontName="STHeiti", fontSize=10,
            leading=14, textColor=colors.HexColor("#0F5E77"), spaceBefore=3, spaceAfter=3, keepWithNext=True,
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
        "h2": ParagraphStyle("Section", fontName="STHeiti", fontSize=17, leading=24, textColor=colors.HexColor("#B42318"), spaceBefore=18, spaceAfter=10, keepWithNext=True),
        "h3": ParagraphStyle("Subsection", fontName="STHeiti", fontSize=14, leading=21, textColor=colors.HexColor("#0F5E77"), spaceBefore=14, spaceAfter=8, keepWithNext=True),
        "h4": ParagraphStyle("MinorHeading", fontName="STHeiti", fontSize=12, leading=18, textColor=colors.HexColor("#344054"), spaceBefore=12, spaceAfter=6, keepWithNext=True),
        "table": ParagraphStyle("TableBody", fontName="STHeiti", fontSize=9, leading=14, textColor=colors.HexColor("#20242A")),
    }
    for name, style in styles.items():
        if name != "code":
            style.wordWrap = "CJK"
    return styles


def document_story():
    styles = build_styles()
    story = [
        Spacer(1, 0.42 * inch),
        Paragraph(inline("Redis相关面试题"), styles["title"]),
        Paragraph(inline("参考回答"), styles["subtitle"]),
    ]
    lines = [strip_quote(line.rstrip()) for line in SOURCE.read_text(encoding="utf-8").splitlines()]
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    paragraph = []
    code = []
    in_code = False
    table_rows = []
    width = A4[0] - 1.44 * inch

    def flush_code():
        wrapped = []
        for line in code:
            current = ""
            size = 0
            for char in line.expandtabs(4):
                advance = pdfmetrics.stringWidth(char, CHAR_FONTS.get(char, "HeitiFallback"), styles["code"].fontSize)
                if size + advance > width - 32:
                    wrapped.append(current)
                    current = "    "
                    size = pdfmetrics.stringWidth(current, "STHeiti", styles["code"].fontSize)
                current += char
                size += advance
            wrapped.append(current)
        RENDERED_TEXT.append("\n".join(code))
        story.append(XPreformatted("\n".join(font_text(line) for line in wrapped), styles["code"]))

    def flush_table():
        if not table_rows:
            return
        # Use the shared table layout with this document's inline formatting.
        import build_batch_interview_pdfs as batch
        original_inline = batch.inline
        batch.inline = inline
        try:
            story.append(make_table(table_rows, width, styles["table"]))
            story.append(Spacer(1, 9))
            RENDERED_TEXT.extend(table_rows)
        finally:
            batch.inline = original_inline
        table_rows.clear()

    def flush_paragraph():
        nonlocal paragraph
        if not paragraph:
            return
        text = " ".join(part.strip() for part in paragraph).strip()
        paragraph = []
        if not text:
            return
        RENDERED_TEXT.append(text)
        interviewer = re.match(r"\*\*面试官[：:]?\*\*\s*[：:]?(.*)", text)
        candidate = re.match(r"\*\*候选人[：:]?\*\*\s*[：:]?(.*)", text)
        if interviewer:
            story.append(Paragraph(inline("面试官：" + interviewer.group(1).strip()), styles["question"]))
        elif candidate:
            story.append(Paragraph(inline("候选人：" + candidate.group(1).strip()), styles["answer_label"]))
        elif text.lstrip("*").startswith(("⭐", "重点问题：", "【")):
            story.append(Paragraph(inline(text), styles["question"]))
        elif re.match(r"(?:[-*]|[0-9]+\.)\s+", text):
            item = re.sub(r"^(?:[-*]|[0-9]+\.)\s+", "", text)
            story.append(Paragraph(inline("• " + item), styles["bullet"]))
        else:
            story.append(Paragraph(inline(text), styles["body"]))

    for line in lines:
        if re.fullmatch(r"```(?:[A-Za-z0-9_+.-]+)?\s*", line.strip()):
            flush_table()
            if in_code:
                flush_code()
                code = []
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if line.strip().startswith("|") and line.strip().endswith("|"):
            flush_paragraph()
            table_rows.append(line.strip())
            continue
        flush_table()
        heading = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if heading:
            flush_paragraph()
            style = "h3" if len(heading.group(1)) == 3 else "h4" if len(heading.group(1)) > 3 else "h2"
            story.append(Paragraph(inline(heading.group(2)), styles[style]))
            RENDERED_TEXT.append(heading.group(2))
            continue
        image_match = re.fullmatch(r"!\[[^]]*\]\(([^)]+)\)", line.strip())
        if image_match:
            flush_paragraph()
            image_path = SOURCE.parent / image_match.group(1)
            if image_path.exists():
                image = Image(str(image_path))
                image._restrictSize(6.55 * inch, 4.55 * inch)
                story.append(image)
                story.append(Paragraph(inline("示意图"), styles["image_note"]))
            else:
                raise FileNotFoundError(image_path)
            continue
        if not line.strip():
            flush_paragraph()
            continue
        if match := re.match(r"^(\s*)([-*+]\s+|[0-9]+[.、]\s*)(.+)$", line):
            flush_paragraph()
            marker = "• " if match.group(2).strip() in ("-", "*", "+") else match.group(2)
            indent = min(len(match.group(1)) // 2, 4)
            style = ParagraphStyle("IndentedBullet", parent=styles["bullet"], leftIndent=17 + indent * 13)
            story.append(Paragraph(inline(marker + match.group(3)), style))
            RENDERED_TEXT.append(match.group(3))
            continue
        if re.match(r"\*\*(?:面试官|候选人)[：:]?\*\*", line.strip()) or line.strip().lstrip("*").startswith("⭐"):
            flush_paragraph()
        paragraph.append(line)
    flush_paragraph()
    flush_table()
    if in_code and code:
        flush_code()
    return story


def main():
    register_fonts()
    staging = ROOT / "tmp/pdfs/Redis面试题-参考回答-new.pdf"
    document = SimpleDocTemplate(
        str(staging), pagesize=A4, leftMargin=0.72 * inch, rightMargin=0.72 * inch,
        topMargin=0.74 * inch, bottomMargin=0.66 * inch, title=SOURCE.stem, author="JavaInterview",
    )
    document.build(document_story(), onFirstPage=page_chrome, onLaterPages=page_chrome)
    (ROOT / "tmp/pdfs/rendered-source.txt").write_text("\n".join(RENDERED_TEXT), encoding="utf-8")
    missing = set(SOURCE.read_text(encoding="utf-8")) - set(CHAR_FONTS)
    print(f"Reference glyphs reused: {len(CHAR_FONTS)}; fallback characters: {''.join(sorted(missing - set(chr(c) for c in range(33))))}")
    # Copy into the existing file: a viewer may hold a handle without delete sharing.
    output = OUTPUT
    try:
        output.write_bytes(staging.read_bytes())
    except PermissionError:
        output = OUTPUT.with_name(OUTPUT.stem + "-新版.pdf")
        output.write_bytes(staging.read_bytes())
        print("Original PDF is open in another process; saved a new version alongside it.")
    print(f"Created {output}")


if __name__ == "__main__":
    main()
