import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS
from OSGridConverter import latlong2grid

GPSINFO = 34853

photosDir = # 'drive:\\***********\\'

os.chdir(photosDir)
with open (photosDir + 'vols.csv', 'w') as f:
    f.write("File,latitude,longitude,fileloc\n")
    for file in glob.glob("*.jpg"):
        with Image.open(file) as img:
            try:
                exifdata = img.getexif()
                val = exifdata.get(GPSINFO)
                latt = float(val[2][0] + (val[2][1]/60) + (val[2][2]/3600))
                lngt = float(val[4][0] + (val[4][1]/60) + (val[4][2]/3600))
                if val[1] == 'S': latt = -latt
                if val[3] == 'W': lngt = -lngt
                gVal = latlong2grid(latt, lngt)
                f.write("{},{},{},{},{},{},{},{}\n".format(file, gVal.N, gVal.E, photosDir + file, val[1], val[2], val[3], val[4]))
                print("{}, {}, {},    {}, {}, {}, {}".format(file, gVal.N, gVal.E, val[1], val[2], val[3], val[4]))
            except:
                pass        


