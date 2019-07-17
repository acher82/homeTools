# -*- coding: utf-8 -*-
import argparse
import csv
import os.path
import json


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

    for dev in soup.find_all("script"):
        if len(dev.contents) > 0 :
            if dev.contents[0].strip().startswith("window.__MADLAN_SSR_CONFIG__="):
                jsonContent = dev.contents[0].strip().replace("window.__MADLAN_SSR_CONFIG__=","")
                dictionary = json.loads(jsonContent)["apiCache"]
                flatsKey = [key for key in dictionary if "https://www.madlan.co.il/homes" in key][0]
                flatsList = dictionary[flatsKey]["jointMarkers"]
                for flat in flatsList:
                    entity=(
                        flat["record"]["id"],                        
                        flat["location"]["formattedAddress"],
                        flat["record"]["features"]["rooms"],
                        flat["record"]["features"]["floor"],
                        flat["record"]["features"]["buildedArea"] if "buildedArea" in flat["record"]["features"] else "",
                        flat["record"]["price"],
                        flat["record"]["publishDate"],
                        flat["record"]["updateDate"],
                        flat["record"]["features"]["floors"],
                        flat["record"]["sellerType"],
                        flat["shareTexts"]["shareUrl"])
                    entities.append(entity)

entities = sorted(entities, key=lambda x: x[0])

if (args.output == "csv"):
    file_name = "{}.csv".format(os.path.splitext(os.path.basename(args.filename))[0])
    with open(file_name, 'wt') as output_file:
        file_writer = csv.writer(output_file)
        file_writer.writerows(entities)
else:
    for de in entities:
        print(de)
