import os
import glob

#Create Variables
srcDataFolder = # 'Drive:\\input\\'
outpDataFolder = # 'Drive:\\output\\'


def getVolume (fileloc):
    print("reading: ", fileloc, end=" ")
    metaData = []
    st = 0.0
    with open(fileloc, 'r') as f:
        ncols = int(f.readline()[6:].rstrip())
        nrows = int(f.readline()[6:].rstrip())
        xcorn = int(f.readline()[10:].rstrip())
        ycorn = int(f.readline()[10:].rstrip())
        cells = int(f.readline()[9:].rstrip())
        ndata = f.readline()[14:].rstrip()
        print("r={} c={}".format(nrows, ncols), end="  ")

        #Read data rows
        for y in range(nrows):
            if ((y%1000) == 0): print (y, end=" ", flush=True)
            l = f.readline().rstrip()
            vals = l.split(' ')
            for v in vals:
                if v != ndata:
                    st += float(v)
        print()
    
    return st



def keyForSort(e):
    line = e.split("_") #site_XX_YYYY.asc
    sSite = line[1]     #XX
    return int(sSite)

    
def main():
    sites = {}
    os.chdir(srcDataFolder)
    filesToProcess = []
    for df in glob.glob("*.asc"):
        filesToProcess.append(df)
    filesToProcess.sort(key=keyForSort)

    for f in filesToProcess:
        x = f.split("_")
        sn = int(x[1])
        sYear = int(x[2][0:4])
        if not (sn in sites):
            sites[sn] = [sYear]
        else:
            sites[sn].append(sYear)

    for s, yrs in sites.items():
        yrs.sort(key=int)

    with open(outpDataFolder + "vols_change_siteperyear.csv", "w") as out:
        out.write("Site, Volume 2019, Volume 2008,Change\n")
        for s, yrs in sites.items():
            src1 = srcDataFolder + "site_{}_{}.asc".format(s, 2019)
            vol1 = getVolume(src1)
            src2 = srcDataFolder + "site_{}_{}.asc".format(s, 2008)
            vol2 = getVolume(src2)
            out.write("{},{:.4f},{:.4f},{:.4f}\n".format(s, vol1, vol2, vol1 - vol2))
            print ("{},{:.4f},{:.4f},{:.4f}".format(s, vol1, vol2, vol1 - vol2))

    

main()