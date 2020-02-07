# -*- coding: utf-8 -*-
import argparse
import csv
import importlib
import os.path
import re


def is_valid_file(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError("The file {} does not exist!".format(path))

def is_valid_month(month):
    if re.match(r"^(19|20)\d{2}\/(0?[1-9]|1[012])$", month):
        return month
    else:
        raise argparse.ArgumentTypeError("Invalid month format. YYYY/MM expected")

parser = argparse.ArgumentParser(description="Consumption excel parser")
parser.add_argument("-p","--path", dest="filename", required=True,
            help="path to excel file", metavar="FILE", type=is_valid_file)
parser.add_argument("-m", "--month", dest="month", required=True,
            help="report's month in format YYYY/MM", type=is_valid_month)
parser.add_argument("-st", "--source-type", dest="source_type", required=True,
            help="excel's file source type")
parser.add_argument("-sn", "--source-name", dest="source_name", required=False,
            help="excel's file source name (credit card or bank account number)")
parser.add_argument("-o", "--output", dest="output", required=False,
            help="output format", choices=["csv"])
args = parser.parse_args()

parser = importlib.import_module("parsers.{}".format(args.source_type))
entities = parser.parse(args.filename, "'{}".format(args.month), args.source_name)

if (args.output == "csv"):
    file_name = "{}_{}.csv".format(args.source_type, args.month.replace("/", "_"))
    with open(file_name, 'wt') as output_file:
        file_writer = csv.writer(output_file)
        file_writer.writerows(entities)
else:
    for de in entities:
        print(de)
