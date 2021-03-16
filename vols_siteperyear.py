import os
import glob

#Create Variables
srcDataFolder = 'D:\\Balraj\\WIP\\DATA_OUT\\'
outpDataFolder = 'D:\\Balraj\\WIP\\DATA_CALC_VOLS\\'


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

    with open(outpDataFolder + "vols_siteperyear.csv", "w") as out:
        for s, yrs in sites.items():
            out.write("Site, Year, Volume(m3)\n")
            for yr in yrs:
                src = srcDataFolder + "site_{}_{}.asc".format(s, yr)
                vol = getVolume(src)
                out.write("{},{},{}\n".format(s, yr, vol))
            out.write("{},2020,\n".format(s))

    

main()