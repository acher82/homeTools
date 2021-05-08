# -*- coding: utf-8 -*-
import re

from xlrd import open_workbook

def parse(path, month, source):    
    # tuple format date,month,sum,source,target,place
    entities = []

    wb = open_workbook(path)
    for sheet in wb.sheets():
        local = not ('חו"ל' in sheet.name or 'ל"וח' in sheet.name)
        for row in range(sheet.nrows):
            if sheet.cell(row,0).value :
                value = sheet.cell(row,0).value
                if 'max executive' in value:
                    source = "'{}".format(''.join(c for c in value if c.isdigit()))
                elif re.match(r"\d{1,2}-\d{1,2}-\d{4}", value):
                    if local:
                        entities.append((
                            value.replace("-", "/"), month, sheet.cell(row,5).value,
                            sheet.cell(row,3).value, '', sheet.cell(row,1).value))
                    else:
                        entities.append((
                            value.replace("-", "/"), month, sheet.cell(row,5).value,
                            sheet.cell(row,3).value, '', sheet.cell(row,1).value, '',
                            str(sheet.cell(row,7).value) + " " + sheet.cell(row,8).value))

    return entities
