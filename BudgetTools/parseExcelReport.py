# -*- coding: utf-8 -*-
import sys
import os.path
import argparse

import de
import dataParser

def is_valid_file(p):
    if not os.path.exists(p):
        raise argparse.ArgumentTypeError("The file %s does not exist!" % p)
    else:
        return p

def is_valid_month(m):
    m = int(m)
    if m < 1 or m > 12:
        raise argparse.ArgumentTypeError("Month must to be in rage 1..12")
    return m

parser = argparse.ArgumentParser(description="Consumption excel parser")
parser.add_argument("-p","--path", dest="filename", required=True,
                    help="path to excel file", metavar="FILE", type=is_valid_file)
parser.add_argument("-m", "--month", dest="month", required=True,
                    help="report's month", type=is_valid_month)
parser.add_argument("-s", "--source", dest="source", required=True,
                    help="excel's file source (last 4 digits of credid card or bank account number)")
args = parser.parse_args()

parserName = args.source.split('_')[0]
parser_method = getattr(dataParser, "parse_%s" % parserName)
entities = parser_method(args)
for de in entities:
    print(de)
