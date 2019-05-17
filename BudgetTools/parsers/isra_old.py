# -*- coding: utf-8 -*-
import csv
import re

def parse(path, month, source):    
    # tuple format date,month,sum,source,target,place
    entities = []

    with open(path,'r', encoding="cp1255") as tsv:
        tsv.readline()
        for line in csv.reader(tsv, dialect="excel-tab"):
            if not line: continue
            if re.match(r"\d{2}\/\d{2}\/\d{4}", line[0]):
                total = float(line[3].replace(',',''))
                if total > 0:
                    entities.append((line[0], month, total, source, '', line[1]))
        tsv.close()

    return entities
