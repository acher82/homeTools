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
                if 'דראקרטסמ' in value or 'מסטרקארד' in value or 'טרכארשי' in value or 'ישראכרט' in value:
                    source = "'{}".format(''.join(c for c in value if c.isdigit()))
                    local = True
                elif source and re.match(r"\d{2}\/\d{2}\/\d{4}", value):
                    if local:
                        entities.append((value, month, sheet.cell(row,4).value, source, '', sheet.cell(row,1).value))
                    elif not sheet.cell(row,2).value.startswith('TOTAL FOR DATE'):
                        entities.append((
                            value, month, sheet.cell(row,5).value, source, '',
                            sheet.cell(row,2).value, '',
                            str(sheet.cell(row,3).value) + " " + sheet.cell(row,4).value))
                elif source and 'עסקאות בחו˝ל' in value:
                    local = False

    return entities
