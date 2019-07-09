# -*- coding: utf-8 -*-
import re

from xlrd import open_workbook

def parse(path, month, source):    
    # tuple format date,month,sum,source,target,place
    entities = []

    account_number = source

    wb = open_workbook(path)
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            if sheet.cell(row,0).value :
                value = sheet.cell(row,0).value
                if not account_number and 'מספר חשבון' in value:
                    account_number = re.search(r"\d{2}-\d{3}-\d{6}", value).group()
                elif account_number and isinstance(value, float):
                    total = None
                    if isinstance(sheet.cell(row,5).value, float):
                        total = sheet.cell(row,5).value
                        source = ''
                        target = account_number
                    if isinstance(sheet.cell(row,4).value, float):
                        total = sheet.cell(row,4).value
                        source = account_number
                        target = ''
                    if total:
                        entities.append((value, month, total, source, target, sheet.cell(row,1).value))
                    
    return entities
