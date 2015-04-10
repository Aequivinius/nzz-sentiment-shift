path = "/Users/Simon/UNI VII/bigdata/nzz/NZZ_1910_1920-with-uuid/"
import os
folderlist=os.listdir(path)
folderlist.remove('.DS_Store')
Nfolders=len(folderlist)
allfiles=[]

for folder in folderlist:
    folderpath=os.path.join(path, folder)
    print folderpath
    filelist=[]
    filelist = os.listdir(folderpath)
    for file in filelist:
        filepath=os.path.join(folderpath, file)
        print filepath
        allfiles.append(filepath)
    