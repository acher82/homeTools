# -*- coding: utf-8 -*-
import csv
from datetime import datetime

date_format_long = '%Y-%m-%d %H:%M:%S'
date_format_short = '%Y-%m-%d'
date_format_out = '%d/%m/%Y'

def rur_to_rub(cur) :
    return 'RUB' if cur == 'RUR' else cur

def parse(path, month, source):    
    # tuple format date,month,sum,source,target,place,category,subcategory,manual,sum_orig,sum_real,cur
    entities = []

    with open(path,'r', encoding="cp1251") as tsv:
        tsv.readline()
        for line in csv.reader(tsv, delimiter=";"):
            if not line: continue
            if line[0].startswith('\'') :

                source = "'{}".format(line[0][-4:])
                date = datetime.strptime(line[1], date_format_long).strftime(date_format_out)
                sum_origin = float(line[3].replace(',','.').replace(' ','')) * -1
                sum_real = float(line[5].replace(',','.').replace(' ','')) * -1
                curency = rur_to_rub(line[4]) + rur_to_rub(line[6])
                place = line[7] if not line[7].startswith('Карта') else line[7][12:]

                entities.append((
                    date,
                    month,
                    0,
                    source,
                    '',
                    place,
                    '',
                    '',
                    '',
                    sum_origin,
                    sum_real,
                    curency))
        tsv.close()

    return entities
