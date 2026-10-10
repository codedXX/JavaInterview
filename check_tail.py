import openpyxl
import json

wb = openpyxl.load_workbook(r'C:\Users\YX\Desktop\2026年10月预付定金小程序抽奖.xlsx', data_only=True)
sheet = wb.active
rows_20_25 = []
for r in range(20, sheet.max_row + 1):
    vals = [sheet.cell(r, c).value for c in range(1, sheet.max_column + 1)]
    rows_20_25.append({"row": r, "vals": [str(x) if x is not None else "" for x in vals]})

with open(r'F:\Projects\JavaInterview\preview_rows.json', 'w', encoding='utf-8') as f:
    json.dump(rows_20_25, f, ensure_ascii=False, indent=2)
