# -*- coding: utf-8 -*-
import re

from xlrd import open_workbook

def convertDate(date):
    parts = date.split("-")
    return "{}/{}/{}".format(parts[2],parts[1],parts[0])

def parse(path, month, source):    
    # tuple format date,month,sum,source,target,place
    entities = []

    wb = open_workbook(path)
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            if sheet.cell(row,0).value :
                value = sheet.cell(row,0).value
                if re.match(r"\d{4}-\d{1,2}-\d{1,2}", value):
                    entities.append((convertDate(value), month, sheet.cell(row,5).value, source, '', sheet.cell(row,1).value))

    return entities
