from pathlib import Path
import html
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[2]
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
SOURCES = [
    ROOT / "04-微服务" / "微服务面试题-参考回答1.md",
    ROOT / "05-消息中间件" / "消息中间件面试题-参考回答.md",
    ROOT / "06-常见集合" / "Java集合相关面试题.md",
    ROOT / "07-并发编程" / "多线程相关面试题.md",
    ROOT / "08-JVM虚拟机" / "JVM相关面试题.md",
]


def inline(value: str) -> str:
    value = value.replace("⭐⭐", "重点问题：").replace("⭐️", "重点问题：").replace("⭐", "重点问题：")
    value = html.escape(value)
    value = re.sub(r"!\[[^]]*\]\([^)]+\)", "", value)
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`(.+?)`", r'<font face="STHeiti" color="#9D3434">\1</font>', value)
    value = value.replace("  ", "&nbsp;&nbsp;")
    return value


def quote_text(line: str) -> tuple[str, int]:
    depth = 0
    value = line.lstrip()
    while value.startswith(">"):
        depth += 1
        value = value[1:].lstrip()
    return value.rstrip(), depth


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName="STHeiti", fontSize=24, leading=31, alignment=TA_CENTER, textColor=colors.HexColor("#B42318"), spaceAfter=12),
        "subtitle": ParagraphStyle("Subtitle", parent=base["Normal"], fontName="STHeiti", fontSize=10, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#6B7280"), spaceAfter=24),
        "h2": ParagraphStyle("Heading2", parent=base["Heading2"], fontName="STHeiti", fontSize=17, leading=24, textColor=colors.HexColor("#A82D22"), spaceBefore=18, spaceAfter=10, keepWithNext=True),
        "h3": ParagraphStyle("Heading3", parent=base["Heading3"], fontName="STHeiti", fontSize=14, leading=20, textColor=colors.HexColor("#0B637F"), spaceBefore=14, spaceAfter=7, keepWithNext=True),
        "h4": ParagraphStyle("Heading4", parent=base["Heading4"], fontName="STHeiti", fontSize=11.5, leading=17, textColor=colors.HexColor("#344054"), spaceBefore=11, spaceAfter=5, keepWithNext=True),
        "question": ParagraphStyle("Question", parent=base["Normal"], fontName="STHeiti", fontSize=11.5, leading=18, textColor=colors.HexColor("#8E1F18"), backColor=colors.HexColor("#FFF3F0"), borderColor=colors.HexColor("#F5C2B8"), borderWidth=0.6, borderPadding=8, spaceBefore=10, spaceAfter=7),
        "answer": ParagraphStyle("Answer", parent=base["Normal"], fontName="STHeiti", fontSize=10, leading=14, textColor=colors.HexColor("#0F5E77"), spaceBefore=2, spaceAfter=3),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="STHeiti", fontSize=10.3, leading=17, textColor=colors.HexColor("#20242A"), spaceAfter=7),
        "quote": ParagraphStyle("Quote", parent=base["BodyText"], fontName="STHeiti", fontSize=10.2, leading=17, leftIndent=12, borderColor=colors.HexColor("#D0D5DD"), borderWidth=0.8, borderPadding=7, textColor=colors.HexColor("#344054"), spaceAfter=7),
        "bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName="STHeiti", fontSize=10.3, leading=17, leftIndent=17, firstLineIndent=-11, textColor=colors.HexColor("#20242A"), spaceAfter=3),
        "code": ParagraphStyle("Code", parent=base["Code"], fontName="STHeiti", fontSize=8.2, leading=12.5, leftIndent=8, rightIndent=8, textColor=colors.HexColor("#343A40"), backColor=colors.HexColor("#F5F6F8"), borderColor=colors.HexColor("#E1E4E8"), borderWidth=0.5, borderPadding=7, spaceBefore=4, spaceAfter=9),
        "table": ParagraphStyle("Table", parent=base["Normal"], fontName="STHeiti", fontSize=8.4, leading=11, textColor=colors.HexColor("#20242A")),
        "caption": ParagraphStyle("Caption", parent=base["Normal"], fontName="STHeiti", fontSize=8, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#6B7280"), spaceAfter=9),
    }


def page_chrome(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#B42318"))
    canvas.setLineWidth(1)
    canvas.line(doc.leftMargin, height - 0.48 * inch, width - doc.rightMargin, height - 0.48 * inch)
    canvas.setFont("STHeiti", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(doc.leftMargin, height - 0.35 * inch, doc.doc_title)
    canvas.drawRightString(width - doc.rightMargin, 0.36 * inch, f"第 {doc.page} 页")
    canvas.restoreState()


def make_table(rows, width, style):
    cleaned = []
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        cleaned.append(cells)
    if not cleaned:
        return None
    count = max(len(row) for row in cleaned)
    normalized = []
    for row in cleaned:
        row += [""] * (count - len(row))
        normalized.append([Paragraph(inline(cell), style) for cell in row])
    table = Table(normalized, colWidths=[width / count] * count, repeatRows=1 if len(normalized) > 1 else 0, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F4F7")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D5DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def build_story(source: Path, doc_width: float):
    style = styles()
    raw_lines = source.read_text(encoding="utf-8").splitlines()
    story = []
    paragraph = []
    paragraph_depth = 0
    code = []
    table_rows = []
    in_code = False
    first_heading = True

    def flush_paragraph():
        nonlocal paragraph
        if not paragraph:
            return
        text = " ".join(item.strip() for item in paragraph).strip()
        paragraph = []
        if not text:
            return
        text = re.sub(r"^```(.+?)```$", r"\1", text)
        interviewer = re.match(r"\*\*面试官[：:]?\*\*\s*(.*)", text)
        candidate = re.match(r"\*\*候选人[：:]?\*\*\s*(.*)", text)
        if interviewer:
            story.append(Paragraph("面试官：" + inline(interviewer.group(1).lstrip("：: ")), style["question"]))
        elif candidate:
            story.append(Paragraph("候选人：" + inline(candidate.group(1).lstrip("：: ")), style["answer"]))
        elif text.startswith("重点问题："):
            story.append(Paragraph(inline(text), style["question"]))
        else:
            story.append(Paragraph(inline(text), style["quote"] if paragraph_depth > 1 else style["body"]))

    def flush_table():
        nonlocal table_rows
        if table_rows:
            table = make_table(table_rows, doc_width, style["table"])
            if table:
                story.append(table)
                story.append(Spacer(1, 7))
        table_rows = []

    for raw in raw_lines:
        line, depth = quote_text(raw)
        stripped = line.strip()
        fence = re.fullmatch(r"```(?:[A-Za-z0-9_+.-]+)?\s*", stripped)
        if fence:
            flush_paragraph()
            flush_table()
            if in_code:
                story.append(Preformatted("\n".join(code), style["code"]))
                code = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_table()
            level, text = len(heading.group(1)), heading.group(2)
            if first_heading:
                story.extend([Spacer(1, 0.42 * inch), Paragraph(inline(text), style["title"]), Spacer(1, 0.16 * inch)])
                first_heading = False
            else:
                story.append(Paragraph(inline(text), style["h2"] if level == 2 else style["h3"] if level == 3 else style["h4"]))
            continue
        image_match = re.fullmatch(r"!\[[^]]*\]\(([^)]+)\)", stripped)
        if image_match:
            flush_paragraph()
            flush_table()
            image_path = source.parent / image_match.group(1)
            if image_path.exists():
                image = Image(str(image_path))
                image._restrictSize(doc_width, 4.85 * inch)
                story.append(image)
                story.append(Paragraph("示意图", style["caption"]))
            continue
        html_image_match = re.search(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", stripped, re.IGNORECASE)
        if html_image_match:
            flush_paragraph()
            flush_table()
            image_path = source.parent / html_image_match.group(1)
            if image_path.exists():
                image = Image(str(image_path))
                image._restrictSize(doc_width, 4.85 * inch)
                story.append(image)
                story.append(Paragraph("示意图", style["caption"]))
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            table_rows.append(stripped)
            continue
        if table_rows:
            flush_table()
        if not stripped:
            flush_paragraph()
            continue
        list_item = re.match(r"^(\s*)(?:[-*+] |(?:\d+|[①②③④⑤⑥⑦⑧⑨⑩])[.、]?)\s*(.+)$", line)
        if list_item:
            flush_paragraph()
            indent = min(len(list_item.group(1).expandtabs(2)) // 2, 4)
            bullet_style = ParagraphStyle("IndentedBullet", parent=style["bullet"], leftIndent=17 + indent * 13)
            story.append(Paragraph("• " + inline(list_item.group(2)), bullet_style))
            continue
        if re.match(r"\*\*(?:面试官|候选人)[：:]?\*\*", stripped) or stripped.startswith("⭐"):
            flush_paragraph()
        if not paragraph:
            paragraph_depth = depth
        paragraph.append(line)

    flush_paragraph()
    flush_table()
    if in_code and code:
        story.append(Preformatted("\n".join(code), style["code"]))
    return story


def main():
    pdfmetrics.registerFont(TTFont("STHeiti", FONT_PATH, subfontIndex=0))
    sources = [Path(argument).resolve() for argument in sys.argv[1:]] or SOURCES
    for source in sources:
        output = source.with_suffix(".pdf")
        document = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=0.72 * inch, rightMargin=0.72 * inch, topMargin=0.74 * inch, bottomMargin=0.66 * inch, title=source.stem, author="JavaInterview")
        document.doc_title = source.stem
        width = A4[0] - document.leftMargin - document.rightMargin
        document.build(build_story(source, width), onFirstPage=page_chrome, onLaterPages=page_chrome)
        print(f"Created {output}")


if __name__ == "__main__":
    main()
