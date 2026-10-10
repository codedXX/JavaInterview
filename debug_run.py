import sys
import os

try:
    with open(r'F:\Projects\JavaInterview\test_out.txt', 'w') as f:
        f.write('hello from python\n')
        import openpyxl
        f.write('openpyxl loaded\n')
        excel_path = r'C:\Users\YX\Desktop\2026年10月预付定金小程序抽奖.xlsx'
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        f.write('workbook loaded\n')
        sheet = wb.active
        f.write(f'sheet loaded: {sheet.title}, rows: {sheet.max_row}\n')
except Exception as e:
    with open(r'F:\Projects\JavaInterview\test_err.txt', 'w') as f:
        f.write(str(e))
