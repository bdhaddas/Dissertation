import os
import glob

#Create Variables
rootDataFolder = 'D:\\Balraj\\WIP\\DATA_OUT\\'
outpDataFolder = 'D:\\Balraj\\WIP\\DATA_CALC\\'
outpDataFolder2 = 'D:\\Balraj\\WIP\\DATA_CALC2\\'
cNCOLS, cNROWS, cXCORN, cYCORN, cCELLS, cNDATA = 0, 1, 2, 3, 4, 5


def writeCalcFile(fileloc, meta, drows):
    with open (fileloc, 'w') as  f:
        f.write("{:14s}".format("ncols") + str(meta[cNCOLS]) + "\n")
        f.write("{:14s}".format("nrows") + str(meta[cNROWS]) + "\n")
        f.write("{:14s}".format("xllcorner") + "{:d}\n".format(meta[cXCORN]))
        f.write("{:14s}".format("yllcorner") + "{:d}\n".format(meta[cYCORN]))
        f.write("{:14s}".format("cellsize") + str(meta[cCELLS])+ "\n")
        f.write("{:14s}".format("NODATA_value") + str(meta[cNDATA])+ "\n")
        
        for r in range(meta[cNROWS]):
            line = ""
            for c in range(meta[cNCOLS]):
                line += "{} ".format(drows[r][c])
            line = line + "\n"
            f.write(line)


def processMinus(r, c, nd):
    mi = []
    for row in range(len(r)):
        line = []
        for col in range(len(r[0])):
            if (r[row][col] == nd) or (c[row][col] == nd):
                line.append(nd)
            else:
                v = float(r[row][col]) - float(c[row][col])
                vs = "{:.4f}".format(v)
                line.append(vs)
        
        mi.append(line)
    return mi


def readFile (fileloc):
    print("reading: ", fileloc, end=" ")
    metaData = []
    drows = []
    with open(fileloc, 'r') as f:
        ncols = int(f.readline()[6:].rstrip())
        nrows = int(f.readline()[6:].rstrip())
        xcorn = int(f.readline()[10:].rstrip())
        ycorn = int(f.readline()[10:].rstrip())
        cells = int(f.readline()[9:].rstrip())
        ndata = int(f.readline()[14:].rstrip())
        metaData = [ncols, nrows, xcorn, ycorn, cells, ndata]
        print("r={} c={}".format(nrows, ncols), end="  ")

        #Read data rows
        for y in range(nrows):
            if ((y%1000) == 0): print (y, end=" ", flush=True)
            l = f.readline().rstrip()
            vals = l.split(' ')
            drows.append(vals)
        print()
    
    return metaData, drows


def processFiles(root, cmp, out):
    rm, r = readFile(root)
    cm, c = readFile(cmp)

    if (rm[cXCORN] == cm[cXCORN]) and (rm[cYCORN] == cm[cYCORN]) and (rm[cNROWS] == cm[cNROWS]) and (rm[cNCOLS] == cm[cNCOLS]):
        m = processMinus(r, c, str(rm[cNDATA]))
        print (out)
        writeCalcFile(out, rm, m)
    else:
        rf = root.split('\\')[-1]
        cf = cmp.split('\\')[-1]
        of = out.split('\\')[-1]
        print ("Unable to process - size not the same   {}".format(of))


# ---------------------------------------------------
def writeCalcFileHeader(f, meta):
    f.write("{:14s}".format("ncols") + str(meta[cNCOLS]) + "\n")
    f.write("{:14s}".format("nrows") + str(meta[cNROWS]) + "\n")
    f.write("{:14s}".format("xllcorner") + "{:d}\n".format(meta[cXCORN]))
    f.write("{:14s}".format("yllcorner") + "{:d}\n".format(meta[cYCORN]))
    f.write("{:14s}".format("cellsize") + str(meta[cCELLS])+ "\n")
    f.write("{:14s}".format("NODATA_value") + str(meta[cNDATA])+ "\n")


def writeCalcFileDataLine(f, drow, meta):
    line = " ".join(drow)
    line = line + "\n"
    f.write(line)


def processMinus_v2(r, c, nd, meta, fileloc):
    with open (fileloc, 'w') as  f:
        writeCalcFileHeader(f, meta)
        
        for row in range(meta[cNROWS]):
            line = []
            for col in range(meta[cNCOLS]):
                if (r[row][col] == nd) or (c[row][col] == nd):
                    line.append(nd)
                else:
                    v = float(r[row][col]) - float(c[row][col])
                    vs = "{:.4f}".format(v)
                    line.append(vs)
                    
            writeCalcFileDataLine(f, line, meta)


def processMinus_v3(r, c, nd, meta, fileloc, fileloc2):
    import time
    start = time.time()    
    print (fileloc2, end=" ")
    with open (fileloc, 'w') as  f:
        with open (fileloc2, 'w') as  f2:
            writeCalcFileHeader(f, meta)
            writeCalcFileHeader(f2, meta)
            
            for row in range(meta[cNROWS]):
                line = []
                line2 = []
                for col in range(meta[cNCOLS]):
                    if (r[row][col] == nd) or (c[row][col] == nd):
                        line.append(nd)
                        line2.append(nd)
                    else:
                        v = float(r[row][col]) - float(c[row][col])
                        vs = "{:.4f}".format(v)
                        line.append(vs)
                        v = float(c[row][col]) - float(r[row][col])
                        vs = "{:.4f}".format(v)
                        line2.append(vs)
                        
                writeCalcFileDataLine(f, line, meta)
                writeCalcFileDataLine(f2, line2, meta)
    end = time.time()
    print ("Done {:.4f}".format(end - start))


def nodata1kmrow(cols, nd):
    cord = []
    rd = []
    for c in range(cols):  rd.append(nd)
    for r in range(1000):  cord.append(rd)
    return (cord)



def processFiles(root, cmp, out, out2):
    rm, r = readFile(root)
    cm, c = readFile(cmp)

    if (rm[cXCORN] != cm[cXCORN]) or (rm[cYCORN] != cm[cYCORN]) or (rm[cNROWS] != cm[cNROWS]) or (rm[cNCOLS] != cm[cNCOLS]):
        print ("          X Corner= {} y Corner= {} x size= {} y size= {}".format(rm[cXCORN], rm[cYCORN], rm[cNCOLS], rm[cNROWS]))
        print ("          X Corner= {} y Corner= {} x size= {} y size= {}".format(cm[cXCORN], cm[cYCORN], cm[cNCOLS], cm[cNROWS]))
        if (rm[cXCORN] == cm[cXCORN]) and (rm[cNCOLS] == cm[cNCOLS]) and  (rm[cYCORN] == cm[cYCORN] and (rm[cNROWS] > cm[cNROWS])):
            if (cm[cNROWS] < rm[cNROWS]):
                nodatasq = nodata1kmrow(cm[cNCOLS], str(cm[cNDATA]))
                i = int((rm[cNROWS] - cm[cNROWS])/1000)
                padding = []
                for y in range(i):
                    print (i)
                    padding = padding + nodatasq
                
                print (len(c))
                c = padding + c
                print (len(c))
                print("=====")
                processMinus_v3(r, c, str(rm[cNDATA]), rm, out, out2)
            else:
                rf = root.split('\\')[-1]
                cf = cmp.split('\\')[-1]
                of = out.split('\\')[-1]
                print ("          Sizes different {} ({},{}) ({},{})\n".format(of, rm[cXCORN], rm[cYCORN], cm[cXCORN], cm[cYCORN]))

        elif (rm[cXCORN] == cm[cXCORN]) and (rm[cNCOLS] == cm[cNCOLS]) and  (rm[cYCORN] > cm[cYCORN]) and (rm[cNROWS] < cm[cNROWS]):
            print ("Here")
            processMinus_v3(r, c, str(rm[cNDATA]), rm, out, out2)
        elif (rm[cXCORN] == cm[cXCORN]) and (rm[cNCOLS] == cm[cNCOLS]) and  (rm[cYCORN] < cm[cYCORN]) and (rm[cNROWS] > cm[cNROWS]):
            print ("There There")
            processMinus_v3(r, c, str(cm[cNDATA]), cm, out, out2)

        else:
            rf = root.split('\\')[-1]
            cf = cmp.split('\\')[-1]
            of = out.split('\\')[-1]
            print ("          Sizes different {} ({},{}) ({},{})\n".format(of, rm[cXCORN], rm[cYCORN], cm[cXCORN], cm[cYCORN]))
    else:
        processMinus_v3(r, c, str(rm[cNDATA]), rm, out, out2)
# ---------------------------------------------------


def keyForSort(e):
    line = e.split("_")
    sSite = line[1]
    return int(sSite)

    
def main():
    sites = {}
    os.chdir(rootDataFolder)
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

    xmax = 0
    for s, yrs in sites.items():
        yrs.sort(reverse=True, key=int)
        if len(yrs) > xmax: xmax = len(yrs)

    for x in range(0, xmax - 1):
        for s, yrs in sites.items():
            if x >= len(yrs): continue
            rootFile = rootDataFolder + "site_{}_{}.asc".format(s, yrs[x])
            for i in range(x+1, len(yrs)):
                cmpFile = rootDataFolder + "site_{}_{}.asc".format(s, yrs[i])
                outFile = outpDataFolder + "site_{}_{}-{}.asc".format(s, yrs[x], yrs[i])
                outFile2 = outpDataFolder2 + "site_{}_{}-{}.asc".format(s, yrs[i], yrs[x])
                if not os.path.exists(outFile):
                    of = outFile.split('\\')[-1]
                    processFiles(rootFile, cmpFile, outFile, outFile2)
                    print()

    

main()
