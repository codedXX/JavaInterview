from pathlib import Path
import base64, html, io, json, zipfile
import xml.etree.ElementTree as ET
from PIL import Image
SOURCE = Path(r"C:\Users\YX\Downloads\企业文化墙报价.xlsx")
OUT = Path(__file__).resolve().parent
SUPPORT = OUT / "support"
SUPPORT.mkdir(parents=True, exist_ok=True)
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
with zipfile.ZipFile(SOURCE) as archive:
    strings = ["".join(si.itertext()) for si in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
    sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    cells = {}
    for cell in sheet.findall(".//s:sheetData/s:row/s:c", NS):
        value = cell.find("s:v", NS)
        if value is not None:
            cells[cell.attrib["r"]] = strings[int(value.text)] if cell.attrib.get("t") == "s" else value.text
    image_bytes = archive.read("xl/media/image1.jpeg")
Image.MAX_IMAGE_PIXELS = None
image = Image.open(io.BytesIO(image_bytes))
original_size = image.size
# Decode at reduced resolution for print, preserving the entire uncropped image.
image.draft("RGB", (3000, 3000))
image.load()
image.thumbnail((3600, 3600), Image.Resampling.LANCZOS)
image_path = SUPPORT / "culture-wall-reference.jpg"
image.save(image_path, "JPEG", quality=95, subsampling=0)
data_url = "data:image/jpeg;base64," + base64.b64encode(image_path.read_bytes()).decode("ascii")
esc = lambda value: html.escape(value, quote=True)
rows = []
for row in range(2, 6):
    effect = f'<td class="effect" rowspan="4"><img src="{data_url}" alt="文化金句区、荣誉星光榜、爱心公益墙、电商中心发展历史四大板块设计及效果图"></td>' if row == 2 else ""
    rows.append(f'<tr><td class="company">{esc(cells[f"A{row}"])}</td><td class="material">{esc(cells[f"B{row}"])}</td><td class="estimate">{esc(cells[f"C{row}"])}</td>{effect}</tr>')
document = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>企业文化墙报价</title>
<style>
* { box-sizing: border-box; }
:root { color-scheme: light; }
html, body { margin: 0; padding: 0; }
body { background: #eceef1; color: #111; font-family: "Microsoft YaHei", "Noto Sans CJK SC", "SimSun", sans-serif; }
.toolbar { max-width: 297mm; margin: 20px auto 14px; padding: 0 20px; display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.toolbar p { margin: 0; font-size: 14px; line-height: 1.7; }
button { font: inherit; font-size: 14px; font-weight: 600; padding: 10px 20px; border: 0; border-radius: 6px; background: #244e72; color: white; cursor: pointer; white-space: nowrap; }
button:focus-visible { outline: 3px solid #76a7d0; outline-offset: 3px; }
.sheet { width: 297mm; height: 210mm; padding: 10mm; margin: 0 auto 20px; background: white; box-shadow: 0 2px 15px #0002; }
h1 { font-size: 17pt; line-height: 1.2; margin: 0 0 5mm; text-align: center; font-weight: 600; }
table { border-collapse: collapse; width: 100%; height: 168mm; table-layout: fixed; font-size: 10pt; }
th, td { border: 0.25mm solid #222; padding: 3mm 2mm; text-align: center; vertical-align: middle; overflow-wrap: anywhere; }
thead { height: 16mm; }
th { background: #f5f6f7; font-size: 10pt; line-height: 1.55; font-weight: 600; }
th:last-child { font-size: 9.5pt; }
tbody tr { height: 38mm; }
.company, .material, .estimate { line-height: 1.8; }
.estimate { font-variant-numeric: tabular-nums; }
.effect { padding: 2mm; }
.effect img { display: block; width: 100%; height: 144mm; object-fit: contain; }
.note { margin: 2mm 0 0; font-size: 8.5pt; line-height: 1.3; color: #444; }
@page { size: A4 landscape; margin: 10mm; }
@media print {
  html, body { width: 277mm; background: white; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .toolbar { display: none !important; }
  .sheet { width: 277mm; height: 190mm; padding: 0; margin: 0; box-shadow: none; }
  table, tr, td, img { break-inside: avoid; page-break-inside: avoid; }
  thead { display: table-header-group; }
}
</style>
</head>
<body>
<div class="toolbar">
  <p>打印设置：A4 · 横向 · 缩放 100% · 关闭页眉和页脚<br>图片已内嵌，文件可离线打开和打印。</p>
  <button type="button" onclick="window.print()">打印 / 保存 PDF</button>
</div>
<main class="sheet">
  <h1>企业文化墙报价</h1>
  <table aria-label="企业文化墙报价比较">
    <colgroup><col style="width:17.5%"><col style="width:22%"><col style="width:14.5%"><col style="width:46%"></colgroup>
    <thead><tr>HEADERS</tr></thead>
    <tbody>ROWS</tbody>
  </table>
  <p class="note">原表备注：NOTE</p>
</main>
</body>
</html>
""".replace("HEADERS", "".join(f'<th scope="col">{esc(cells[f"{col}1"]).replace("整体估价（", "整体估价<br>（").replace("、电商中心", "、<br>电商中心")}</th>' for col in "ABCD")).replace("ROWS", "\n".join(rows)).replace("NOTE", esc(cells["D1192"]))
output = OUT / "企业文化墙报价_打印版.html"
output.write_text(document, encoding="utf-8")
(SUPPORT / "source-data.json").write_text(json.dumps({"cells": cells, "original_image_size": original_size, "print_image_size": image.size}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"html": str(output), "size_bytes": output.stat().st_size, "original_image_size": original_size, "print_image_size": image.size, "quote_rows": 4}, ensure_ascii=False))



