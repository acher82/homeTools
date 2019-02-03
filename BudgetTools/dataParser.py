# -*- coding: utf-8 -*-
import csv
import re

from xlrd import open_workbook

import de


def parse_IsraNew(args):
    
    entities = []

    wb = open_workbook(args.filename)
    for sheet in wb.sheets():
        source = None
        for row in range(sheet.nrows):
            if sheet.cell(row,0).value :
                value = sheet.cell(row,0).value
                if 'דראקרטסמ'.decode('utf-8') in value or 'מסטרקארד'.decode('utf-8') in value:
                    source = ''.join(c for c in value if c.isdigit())
                    local = True
                elif source and re.match(r"\d{2}\/\d{2}\/\d{4}", value):
                    if local:
                        entities.append(de.dataEntity(value, args.month, sheet.cell(row,1).value, sheet.cell(row,4).value, source, ''))
                    elif not sheet.cell(row,2).value.startswith('TOTAL FOR DATE'):
                        entities.append(de.dataEntity(value, args.month, sheet.cell(row,2).value, sheet.cell(row,5).value, source, ''))
                elif source and 'עסקאות בחו˝ל'.decode('utf-8') in value:
                    local = False

    return entities

def parse_Leumi(args):
    
    entities = []

    source = args.source.split('_')[1]

    wb = open_workbook(args.filename)
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            if sheet.cell(row,0).value :
                value = sheet.cell(row,0).value
                if re.match(r"\d{1,2}\/\d{1,2}\/\d{4}", value):
                    entities.append(de.dataEntity(value, args.month, sheet.cell(row,2).value, sheet.cell(row,6).value, source, ''))

    return entities

def parse_Otzar(args):

    entities = []

    account_number = args.source.split('_')[1]    

    with open(args.filename,'rU') as tsv:
        tsv.readline()
        for line in csv.reader(tsv, dialect="excel-tab"):
            if not line: continue
            sum = None
            if line[2].strip():
                sum = float(line[2].replace(',',''))
                source = ''
                target = account_number
            if line[3].strip():
                sum = float(line[3].replace(',',''))
                source = account_number
                target = ''
            if sum:
                entities.append(de.dataEntity(line[1], args.month, line[4].decode('cp1255'), sum, source, target))
        tsv.close()

    return entities

def parse_Hapoalim(args):

    entities = []

    account_number = None

    wb = open_workbook(args.filename)
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            if sheet.cell(row,0).value :
                value = sheet.cell(row,0).value
                if not account_number and 'מספר חשבון'.decode('utf-8') in value:
                    account_number = re.search(r"\d{2}-\d{3}-\d{6}", value).group()
                    print(account_number)
                elif account_number and isinstance(value, float):
                    sum = None
                    if isinstance(sheet.cell(row,5).value, float):
                        sum = sheet.cell(row,5).value
                        source = ''
                        target = account_number
                    if isinstance(sheet.cell(row,4).value, float):
                        sum = sheet.cell(row,4).value
                        source = account_number
                        target = ''
                    if sum:
                        entities.append(de.dataEntity(value, args.month, sheet.cell(row,1).value, sum, source, target))
                    
    return entities
