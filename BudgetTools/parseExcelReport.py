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
    if re.match(r"^(0?[1-9]|1[012])\/(19|20)\d{2}$", month):
        return month
    else:
        raise argparse.ArgumentTypeError("Invalid month format. MM/YYYY expected")

parser = argparse.ArgumentParser(description="Consumption excel parser")
parser.add_argument("-p","--path", dest="filename", required=True,
            help="path to excel file", metavar="FILE", type=is_valid_file)
parser.add_argument("-m", "--month", dest="month", required=True,
            help="report's month in format MM/YYYY", type=is_valid_month)
parser.add_argument("-st", "--source-type", dest="source_type", required=True,
            help="excel's file source type(source name_[credit card or bank account number])")
parser.add_argument("-sn", "--source-name", dest="source_name", required=True,
            help="excel's file source name (credit card or bank account number)")
args = parser.parse_args()

parser_method = getattr(data_parser, "parse_%s" % args.source_type)
entities = parser_method(args)
for de in entities:
    print(de)
