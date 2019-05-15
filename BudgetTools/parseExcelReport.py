# -*- coding: utf-8 -*-
import argparse
import os.path
import re

import data_parser
import de


def is_valid_file(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError("The file %s does not exist!" % path)
    else:
        return path

def is_valid_month(month):
    if re.match(r"\d{2}/\d{4}", month):
        return month
    else:
        raise argparse.ArgumentTypeError("Invalid month format. MM/YYYY expected")

parser = argparse.ArgumentParser(description="Consumption excel parser")
parser.add_argument("-p","--path", dest="filename", required=True,
            help="path to excel file", metavar="FILE", type=is_valid_file)
parser.add_argument("-m", "--month", dest="month", required=True,
            help="report's month in format MM/YYYY", type=is_valid_month)
parser.add_argument("-s", "--source", dest="source", required=True,
            help="excel's file source (source name_[credit card or bank account number])")
args = parser.parse_args()

parserName = args.source.split('_')[0]
parser_method = getattr(data_parser, "parse_%s" % parserName)
entities = parser_method(args)
for de in entities:
    print(de)
