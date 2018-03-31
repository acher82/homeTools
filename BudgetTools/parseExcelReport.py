# -*- coding: utf-8 -*-
import sys
import os.path
import argparse
import re
from xlrd import open_workbook

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

parser = argparse.ArgumentParser(description="Consumption excel parser")
parser.add_argument("-p","--path", dest="filename", required=True,
                    help="path to excel file", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
parser.add_argument("-s", "--source", dest="source", required=True,
                    help="excel's file source (last 4 digits of credid card or bank account number)")
args = parser.parse_args()

print(args.filename)
print(args.source)

wb = open_workbook(args.filename)
for sheet in wb.sheets():
    source = "none"
    for row in range(sheet.nrows):
        if sheet.cell(row,0).value :
            value = sheet.cell(row,0).value
            if (value.startswith('מסטרקארד'.decode('utf-8'))):
                source = ''.join(c for c in value if c.isdigit())
            elif source and re.match(r"\d{2}\/\d{2}\/\d{4}", value):
                print(value, sheet.cell(row,1).value, sheet.cell(row,4).value,source)
   
