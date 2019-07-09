
import argparse
import os
import random
import sys
from datetime import datetime

import exifread

parser = argparse.ArgumentParser(description="Renames image files in folder to name based on 'EXIF DateTimeOriginal' field")
parser.add_argument("-p","--path", dest="path", required=True,
            help="path")
parser.add_argument("-f","--format", dest="format", default="IMG_%Y%m%d_%H%M%S.jpg",
            help="new name format")
args = parser.parse_args()

only_files = [f for f in os.listdir(args.path) if os.path.isfile(os.path.join(args.path, f))]
for file in only_files:
    sys.stdout.write(file)
    sys.stdout.write("-->")
    try:
        f = open(os.path.join(args.path,file), 'rb')
        tags = exifread.process_file(f)
        f.close()
        
        dateStr = tags['EXIF DateTimeOriginal']
        dt = datetime.strptime(dateStr.__str__(), "%Y:%m:%d %H:%M:%S")
        newName = dt.strftime(args.format)
        if os.path.exists(os.path.join(args.path, newName)):
            newName = newName.replace(".jpg", "_{}.jpg".format(random.randint(1000,9999)))
        os.rename(os.path.join(args.path, file), os.path.join(args.path, newName))
        print(newName)

    except Exception as ex:
        print("{} {}".format(type(ex).__name__, ex))
