import sys
from os import listdir, rename
from os.path import isfile, join

if (len(sys.argv) == 1):
    print("Provide a path")
    sys.exit(1)

mypath = sys.argv[1]
print(mypath)

onlyFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyFiles:
    if "-" not in file:
        continue        
    newName = file.replace("-","_")
    rename(join(mypath, file), join(mypath, newName))
    print(file, newName)
