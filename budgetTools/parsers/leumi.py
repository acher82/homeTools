# -*- coding: utf-8 -*-
import re

from xlrd import open_workbook

def parse(path, month, source):    
    # tuple format date,month,sum,source,target,place
    entities = []

    wb = open_workbook(path)
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            if sheet.cell(row,0).value :
                value = sheet.cell(row,0).value
                if re.match(r"\d{1,2}\/\d{1,2}\/\d{4}", value):
                    entities.append((value, month, sheet.cell(row,6).value, source, '', sheet.cell(row,2).value))

    return entities
