"""Convert a Markdown test-case table into a formatted .xlsx file.

Usage: python md_to_xlsx.py <input.md> <output.xlsx>
Requires: openpyxl
"""
import sys
import re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

md_path = sys.argv[1]
xlsx_path = sys.argv[2]

with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Markdown files may contain several tables (traceability matrix, notes, ...).
# Group consecutive "|"-prefixed lines into separate table blocks, then pick the
# block that looks like the actual test-case table (header contains "TC ID"),
# falling back to the largest block if none matches.
blocks = []
current = []
for l in lines:
    if l.strip().startswith("|"):
        current.append(l)
    elif current:
        blocks.append(current)
        current = []
if current:
    blocks.append(current)

if not blocks:
    raise SystemExit("No markdown table found in " + md_path)


def parse_block(block_lines):
    parsed = []
    for l in block_lines:
        if re.match(r"^\|[\s:\-|]+\|$", l.strip()):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        parsed.append(cells)
    return parsed


parsed_blocks = [parse_block(b) for b in blocks]
parsed_blocks = [b for b in parsed_blocks if b]

target = next((b for b in parsed_blocks if b[0] and "tc id" in b[0][0].strip().lower()), None)
if target is None:
    target = max(parsed_blocks, key=len)

rows = target

if not rows:
    raise SystemExit("No markdown table found in " + md_path)

wb = Workbook()
ws = wb.active
ws.title = "TestCases"

header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF")
thin = Side(style="thin", color="B7B7B7")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")

for r_idx, row in enumerate(rows, start=1):
    for c_idx, val in enumerate(row, start=1):
        val = val.replace("<br>", "\n")
        cell = ws.cell(row=r_idx, column=c_idx, value=val)
        cell.border = border
        cell.alignment = wrap
        if r_idx == 1:
            cell.fill = header_fill
            cell.font = header_font

default_widths = [18, 14, 22, 32, 26, 32, 10, 14, 12, 14]
ncols = len(rows[0])
for i in range(1, ncols + 1):
    w = default_widths[i - 1] if i - 1 < len(default_widths) else 18
    ws.column_dimensions[get_column_letter(i)].width = w

ws.freeze_panes = "A2"
ws.auto_filter.ref = ws.dimensions

wb.save(xlsx_path)
print("Saved:", xlsx_path, "rows:", len(rows))
