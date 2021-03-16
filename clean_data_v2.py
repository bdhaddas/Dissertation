import os
import glob

#Define Constants
#Index of data records
cQUAD, cYEAR, cMONTH, cDAY, cSITE, cFILENAME, cCORD, cSITENUM = 0, 1, 2, 3, 4, 5, 6, 7
cNODATA = -9999


#Create Variables
rootDataFolder = 'D:\\Balraj\\WIP\\DATA\\'

#Create a list sites
Sites = os.listdir(rootDataFolder)
Sites.sort(key = int)
#print (Sites)

#Create data structure of input data
ld = {}             #Lidar Data from website
unusedData = []     #duplicate data that is not used
ldmq = {}           #For years where the ld was in 0.5m quads, merge in 1km files

for x in Sites:
    subFolder = rootDataFolder + x + "\\"
    os.chdir(subFolder)
    sSite = "Site " + x
#    print ("-------------------------------------------------------------")
#    print (sSite)
    for file in glob.glob("*.asc"):
        fileParts = file.split("_")  #Separate filename at _
        #print (fileParts)
        c = fileParts[0].upper()  #Location - for comparison change to uppercase
        cord = c[0:6]
        quad = '  '
        if (len(c) > 6):
            quad = c[6:8]
                    
        yr = fileParts[1][0:4]  #Year
        mt = fileParts[1][4:6]  #Month
        da = fileParts[1][6:8]  #Day
        
        dRec = [quad, yr, mt, da, sSite, file, cord, x]
        if (quad == 'XX'): continue
        print (dRec)
        if cord in ld:
            tmp = ld[cord]
            #print (tmp, quad, yr, mt, da, sSite, file)
            if yr in tmp:
                #An entry for this cord and year already existes
                #So, replace it if this one is older and the 'quad' is the same
                #  0      1      2     3     4          5
                #['NE', '2008', '03', '09', 'Site 12', 'SW7960ne_20080309lidarf.asc']
                t2 = tmp[yr]
                
                #For this cord and year look for this quad
                found = False
                for i in range(len(t2)):
                    #print (i, t2[i][0])
                    if ( quad == t2[i][cQUAD]):
                        found = True
                    
                if (found):
                    #same quad
                    #print (mt, t2[0][2], t2[0][0], t2[0][5],file, "Same")
                    if ( mt < t2[0][cMONTH]):
                        #This entry is older than one we have 
                        #So, subsitute it for the current one
                        print ("********* Subsitute ***********")
                    else:
                        #This entry is newer than one we have
                        #So, discard it,
                        #    and save it for reference
                        unusedData.append(dRec)
                    
                else:
                    #different quad
                    #print (mt, t2[0][2], t2[0][0], t2[0][5],file, "Different")
                    t2.append(dRec)
                    tmp[yr] = t2
            else:
                #An entry for this cord existes but not this year
                t3 = list()
                t3.append(dRec)
                tmp[yr] = t3
                
            #print (tmp)
        else:
            #No entry for this cord, create a new one
            ld[cord] =  {yr : [dRec]}


        
def showDataItems(di, ud=None):
    print ("\n")
    for c, y in di.items():
        print ("Cord", c)
        #print (y)
        for yy, dl in y.items():
            print ("       Year", yy)
            for d in dl:
                print ("              ", d)
            if (ud != None):
                #show unused data for that year
                uf = False
                for i in ud:
                    if ((i[cCORD] == c) and (i[1] == yy)): uf = True
                if (uf):
                    print ("          Unused Data")
                    for i in ud:
                        if ((i[cCORD] == c) and (i[cYEAR] == yy)):
                            print ("              ", i)
                print('')

    if (ud != None):    
        #Show unused Data
        print ('\n')
        print ("==================================================================")
        print ("All unused Data")
        for i in ud:
            print (i)
        print ("#unused=", len(ud))

def readQuadfile(fn, folder, c, q):
##    print("               ===== Read Quad ======")
##    print ("              ", fn)
    with open (rootDataFolder + folder + "\\" + fn, 'r') as  f:
        ncols = int(f.readline()[14:].rstrip())
        nrows = int(f.readline()[14:].rstrip())
        xcorn = int(f.readline()[14:].rstrip())
        ycorn = int(f.readline()[14:].rstrip())
        cells = int(f.readline()[14:].rstrip())
        ndata = int(f.readline()[14:].rstrip())
        xbase = 0
        ybase = 0
        if (q == 'SW'):
            xbase = xcorn
            ybase = ycorn
            xstart = 0
            ystart = nrows
        if (q == 'SE'):
            xbase = xcorn - nrows
            ybase = ycorn
            xstart = ncols
            ystart = nrows
        if (q == 'NW'):
            xbase = xcorn
            ybase = ycorn - ncols
            xstart = 0
            ystart = 0
        if (q == 'NE'):
            xbase = xcorn - nrows
            ybase = ycorn - ncols
            xstart = ncols
            ystart = 0
            
        #read the data
        for y in range(nrows):
            #print (r)
            l = f.readline().rstrip()
            vals = l.split(' ')
            for x in range(len(vals)):
                c[y + ystart][x + xstart] = vals[x]


def readMetadata(fn, folder, q):
    with open (rootDataFolder + folder + "\\" + fn, 'r') as  f:
        ncols = int(f.readline()[14:].rstrip())
        nrows = int(f.readline()[14:].rstrip())
        xcorn = int(f.readline()[14:].rstrip())
        ycorn = int(f.readline()[14:].rstrip())
        if (q == 'SW'):
            xbase = xcorn
            ybase = ycorn
        if (q == 'SE'):
            xbase = xcorn - nrows
            ybase = ycorn
        if (q == 'NW'):
            xbase = xcorn
            ybase = ycorn - ncols
        if (q == 'NE'):
            xbase = xcorn - nrows
            ybase = ycorn - ncols
    return (xbase, ybase)
 
def addMergedFiletoList(file, folder):
    fileParts = file.split("_")  #Separate filename at _
    c = fileParts[0].upper()  #Location - for comparison change to uppercase
    cord = c[0:6]
    quad = '  '
    if (len(c) > 6):
        quad = c[6:8]
                
    yr = fileParts[1][0:4]  #Year
    mt = fileParts[1][4:6]  #Month
    da = fileParts[1][6:8]  #Day
    
    sSite = "Site {}".format(folder)
    dRec = [quad, yr, mt, da, sSite, file, cord, folder]
    print ("              ", dRec)
    if cord in ldmq:
        tmp = ldmq[cord]
        if not (yr in tmp):
            #An entry for this cord existes but not this year
            t3 = list()
            t3.append(dRec)
            tmp[yr] = t3
    else:
        #No entry for this cord, create a new one
        ldmq[cord] =  {yr : [dRec]}


    


def writeMergedFile(fn, folder, x, y, md):
##    print (fn, x, y)
    with open (rootDataFolder + folder + "\\" + fn, 'w') as  f:
        f.write("{:14s}".format("ncols") + "1000\n")
        f.write("{:14s}".format("nrows") + "1000\n")
        f.write("{:14s}".format("xllcorner") + "{:d}\n".format(x))
        f.write("{:14s}".format("yllcorner") + "{:d}\n".format(y))
        f.write("{:14s}".format("cellsize") + "1\n")
        f.write("{:14s}".format("NODATA_value") + "-9999\n")
        for r in range(1000):
            str = ""
            for c in range(1000):
                str += "{} ".format(md[r][c])
            str = str + "\n"
            f.write(str)
            
    addMergedFiletoList(fn, folder)
                
        


def init_1km_cord():
    cord = []
    for x in range(1000):
        rd = []
        for y in range(1000):
            rd.append(cNODATA)
        cord.append(rd)
    return (cord)


c1km = []

def mergeQuads(di):
    print ("===== Merge ======")
    #create array of NO DATA for 1km cord
    for c, y in di.items(): # c = cord, y = All years
        print ("Cord", c)
        #print (y)
        for yy, dl in y.items(): # yy = one year, dl = Quads for that year
            print ("       Year", yy, len(dl))

            if not ((len(dl) == 1) and (dl[0][cQUAD] == '  ')):
                #Has one or more files of quads
                merged = dl[0][cFILENAME]
                merged = merged[0:6] + "XX" + merged[8:]
                if not os.path.exists(rootDataFolder + dl[0][cSITENUM] + "\\" + merged):
                    c1km = init_1km_cord()
                    for d in dl:
                        if (d[cQUAD] == "XX"): continue
                        print ("              ", d, "Has quad data")
                        readQuadfile(d[cFILENAME], d[cSITENUM], c1km, d[cFILENAME][6:8].upper())
                    print ("              ", merged)
                    xorg, yorg = readMetadata(dl[0][cFILENAME], dl[0][cSITENUM], dl[0][cFILENAME][6:8].upper())
                    writeMergedFile(merged, dl[0][cSITENUM], xorg, yorg, c1km)


def outputGoodDatafile(dr):
    #Write good data to file
    with open(rootDataFolder + "..\\gooddata.txt", "w") as f:
        for gd in dr:
            #print (gd, "\n\n")
            for c, y in gd.items():
                #print (c, y, "\n\n")
                for yy, dl in y.items():
                    #print (yy, dl, "\n\n")
                    for d in dl:
                        if (d[cQUAD] == '  ') or (d[cQUAD] == 'XX'):
                            str = "{},{},{},{},{}{}".format(d[cSITE], d[cYEAR], d[cFILENAME], rootDataFolder + d[cSITE][5:] + "\\" +  d[cFILENAME], d[cCORD], "\n") 
                            f.write (str)
                            #print (str, end='')
                        else:
                            str = "{},{},{},{},{}{}".format(d[cSITE], d[cYEAR], d[cFILENAME], rootDataFolder + d[cSITE][5:] + "\\" +  d[cFILENAME], d[cCORD], " <- UNUSED")
                            #print(str)


def main():
    mergeQuads(ld)
    outputGoodDatafile([ld, ldmq])
    #showDataItems(ldmq)


main()
