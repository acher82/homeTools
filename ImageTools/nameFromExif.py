import sys
from datetime import datetime
from os import listdir, rename
from os.path import isfile, join

import exifread

if (len(sys.argv)==1):
    print("Provide a path")
    sys.exit(1)

mypath = sys.argv[1]
print(mypath)

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles:
    f = open(join(mypath,file), 'rb')
    tags = exifread.process_file(f)
    f.close()
    
    sys.stdout.write(file)
    dateStr = tags['EXIF DateTimeOriginal']
    dt = datetime.strptime(dateStr.__str__(), "%Y:%m:%d %H:%M:%S")
    newName = dt.strftime("IMG_%Y%m%d_%H%M%S.jpg")
    rename(join(mypath, file), join(mypath, newName))
    sys.stdout.write("-->")
    sys.stdout.write(newName)
    print
