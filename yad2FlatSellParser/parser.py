# -*- coding: utf-8 -*-
import argparse
import csv
import collections
import glob
import os
import re

from bs4 import BeautifulSoup

def is_valid_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError("The file {} does not exist!".format(path))
    return path

def parsable_row(tag):
    return not (
        tag.has_attr('is-platinum') or
        'boost_realtor' in tag['class']
    )

def parse_row(tag):
    response = {}
    response["id"] = tag["item-id"]
    response["address"] = tag.find("span", {"class" : "title"}).contents[0].strip()
    response["rooms"] = tag.find("span",
        {"id" : re.compile('^data_rooms_\\d+$')}).contents[0].strip()
    response["floor"] = tag.find("span",
        {"id" : re.compile('^data_floor_\\d+$')}).contents[0].strip()
    response["sqrm"] = tag.find("span",
        {"id" : re.compile('^data_SquareMeter_\\d+$')}).contents[0].strip()
    response["price"] = ''.join(c for c in tag.find("div",
        {"class" : "price"}).contents[0].strip() if c.isdigit())
    response["updated"] = tag.find("div", {"class" : "showDateInLobby"}).contents[0].strip()
    merchant = tag.find("div", {"class" : "merchant_name"})
    if merchant is not None:
        response["merchant"] = merchant.contents[1].strip()
    else:
        response["merchant"] = ""

    return collections.namedtuple("FlatData", response.keys())(*response.values())

def parse_page(file_name):
    response = []
    with open(file_name, 'rb') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'html.parser')

    for dev in soup.find_all("div", {"id" : re.compile('^feed_item_\\d+$')}):
        if parsable_row(dev):
            response.append(
                parse_row(dev)
            )

    return response

parser = argparse.ArgumentParser(description="real estate html parser")
parser.add_argument("-p","--path", required=True,
            help="path to a folder", type=is_valid_path)
parser.add_argument("-f", "--filter", required=True,
            help="files selector", default="*.html")
parser.add_argument("-o", "--output", required=False,
            help="output format", choices=["csv"])
args = parser.parse_args()

entities = []
for file in glob.glob(f"{args.path}{args.filter}"):
    entities = entities + parse_page(file)

entities.sort(key=lambda x: x.id)

if args.output == "csv":
    out_file_name = "output.csv"
    with open(out_file_name, 'wt') as output_file:
        file_writer = csv.writer(output_file)
        file_writer.writerows(entities)
else:
    for de in entities:
        print(de)
