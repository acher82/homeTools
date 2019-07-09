# -*- coding: utf-8 -*-
import argparse
import csv
import os.path

from bs4 import BeautifulSoup


def is_valid_file(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError("The file {} does not exist!".format(path))

parser = argparse.ArgumentParser(description="HTML file")
parser.add_argument("-p","--path", dest="filename", required=True,
            help="path to HTML file", metavar="FILE", type=is_valid_file)
parser.add_argument("-o", "--output", dest="output", required=False,
            help="output format", choices=["csv"])
args = parser.parse_args()

entities = []
with open(args.filename, 'rb') as file:
    content = file.read()
    soup = BeautifulSoup(content, 'html.parser')

    for dev in soup.find_all("div", "feeditem table"):
        item_id = dev.find("div", {"itemid" : True})["itemid"]
        address = dev.find("span", {"class" : "title"}).contents[0].strip()
        values = dev.find_all("span", {"class" : "val"})
        rooms = values[0].contents[0].strip()
        floor = values[1].contents[0].strip()
        sqrm = values[2].contents[0].strip()
        price = ''.join(c for c in dev.find("div", {"class" : "price"}).contents[0].strip() if c.isdigit())
        date = dev.find("div", {"class" : "merchant_name"})
        if date is not None:
            date = date.contents[1].strip()
        else:
            date = dev.find("span", {"class" : "date"}).contents[0].strip()
        entities.append((item_id, address, rooms, floor, sqrm, price, date))

entities = sorted(list(set(entities)), key=lambda x: x[0])

if (args.output == "csv"):
    file_name = "{}.csv".format(os.path.splitext(os.path.basename(args.filename))[0])
    with open(file_name, 'wt') as output_file:
        file_writer = csv.writer(output_file)
        file_writer.writerows(entities)
else:
    for de in entities:
        print(de)
