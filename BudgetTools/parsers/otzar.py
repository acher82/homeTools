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
            value = sheet.cell(row,2).value
            if re.match(r"\d{2}\/\d{2}\/\d{4}", value):
                total = None
                if isinstance(sheet.cell(row,3).value, float):
                    total = sheet.cell(row,3).value
                    source = ''
                    target = account_number
                if isinstance(sheet.cell(row,4).value, float):
                    total = sheet.cell(row,4).value
                    source = account_number
                    target = ''
                if total:
                    entities.append((value, month, total, source, target, sheet.cell(row,5).value))
    return entities
