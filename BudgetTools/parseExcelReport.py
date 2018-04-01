# -*- coding: utf-8 -*-
import sys
import os.path
import argparse
import re
from xlrd import open_workbook

import de

def is_valid_file(p):
    if not os.path.exists(p):
        raise argparse.ArgumentTypeError("The file %s does not exist!" % p)
    else:
        return p

def is_valid_month(m):
    m = int(m)
    if m < 1 or m > 12:
        raise argparse.ArgumentTypeError("Month must to be in rage 1..12")
    return m

parser = argparse.ArgumentParser(description="Consumption excel parser")
parser.add_argument("-p","--path", dest="filename", required=True,
                    help="path to excel file", metavar="FILE", type=is_valid_file)
parser.add_argument("-m", "--month", dest="month", required=True,
                    help="report's month", type=is_valid_month)
parser.add_argument("-s", "--source", dest="source", required=True,
                    help="excel's file source (last 4 digits of credid card or bank account number)")
args = parser.parse_args()

print(args.filename)
print(args.source)

entities = []
wb = open_workbook(args.filename)
for sheet in wb.sheets():
    source = "none"
    for row in range(sheet.nrows):
        if sheet.cell(row,0).value :
            value = sheet.cell(row,0).value
            if (value.startswith('מסטרקארד'.decode('utf-8'))):
                source = ''.join(c for c in value if c.isdigit())
            elif source and re.match(r"\d{2}\/\d{2}\/\d{4}", value):
                entities.append(de.dataEntity(value, args.month, sheet.cell(row,1).value, sheet.cell(row,4).value, source))
for de in entities:
    print(de)
