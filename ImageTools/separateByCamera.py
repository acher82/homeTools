
import argparse
import os
import sys

import exifread

parser = argparse.ArgumentParser(description="Separates images to folders by camera information from EXIF")
parser.add_argument("-p","--path", dest="path", required=True,
            help="path")
args = parser.parse_args()

only_files = [f for f in os.listdir(args.path) if os.path.isfile(os.path.join(args.path, f))]
for file in only_files:
    sys.stdout.write(file)
    sys.stdout.write("-->")
    try:
        f = open(os.path.join(args.path,file), 'rb')
        tags = exifread.process_file(f)
        f.close()
        
        model = tags['Image Model']
        path = os.path.join(args.path, model.printable)
        os.makedirs(path, exist_ok=True)
        os.rename(os.path.join(args.path, file), os.path.join(path, file))
        print(model)

    except Exception as ex:
        print("{} {}".format(type(ex).__name__, ex))
