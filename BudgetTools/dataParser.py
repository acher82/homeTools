# -*- coding: utf-8 -*-
import re
from xlrd import open_workbook

import de

def parse_IsraNew(args):
    
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
    return entities
