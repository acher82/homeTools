import argparse
import os
import sys
import PyPDF2
import random
from datetime import datetime

parser = argparse.ArgumentParser(description="Renames PDF file according CreationDate")
parser.add_argument("-p","--path", dest="path", required=True,
            help="path")
args = parser.parse_args()

srcFrmt = "D:%Y%m%d%H%M%S"
tgtFrmt = "%Y%m%d_%H%M%S.pdf"

pdf_files = [f for f in os.listdir(args.path) if os.path.isfile(os.path.join(args.path, f)) and f.endswith(".pdf")]
for file in pdf_files:
    sys.stdout.write(file)
    sys.stdout.write("-->")
    try:
        f = open(os.path.join(args.path, file), 'rb')
        pdfReader = PyPDF2.PdfFileReader(f)
        pdfInfo = pdfReader.getDocumentInfo()
        f.close()
        
        dateStr = pdfInfo["/CreationDate"]
        dt = datetime.strptime(dateStr[:len(srcFrmt)], srcFrmt)
        newName = dt.strftime(tgtFrmt)
        if os.path.exists(os.path.join(args.path, newName)):
            newName = newName.replace(".pdf", "_{}.pdf".format(random.randint(1000,9999)))
        os.rename(os.path.join(args.path, file), os.path.join(args.path, newName))
        print(newName)

    except Exception as ex:
        print("{} {}".format(type(ex).__name__, ex))
