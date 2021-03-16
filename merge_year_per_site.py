import os
import glob


#Create Variables
rootDataFolder = 'D:\\Balraj\\WIP\\DATA\\'
outputRootFolder = 'D:\\Balraj\\WIP\\DATA_OUT\\'



#Create data structure
cXMIN, cYMIN, cXMAX, cYMAX = 0, 1, 2, 3                         #form minmax
cSITENUM, cCORD, cYEAR, cXLLC, cYLLC, cDVALS = 0, 1, 2, 3, 4, 5 #for siteData


def writeSiteYearFile(filename, sn, nc, nr, xll, yll, cell, ndata, vals):
    print("\n\n", filename, sn, nc, nr, xll, yll, cell, ndata)
    fileloc = outputRootFolder + "\\" + filename
    print (fileloc)
    with open(fileloc,'w') as f:
        f.write("{:14s}".format("ncols") + nc + "\n")
        f.write("{:14s}".format("nrows") + nr + "\n")
        f.write("{:14s}".format("xllcorner") + "{:s}\n".format(xll))
        f.write("{:14s}".format("yllcorner") + "{:s}\n".format(yll))
        f.write("{:14s}".format("cellsize") + "1\n")
        f.write("{:14s}".format("NODATA_value") + "-9999\n")
        for y in range(len(vals)):
            print ("Y=", y)
            for n in range(1000):
                l = ""
                for x in range(len(vals[y])):
                    #print (y, n, x, len(vals[y][x][n]))
                    for i in range(len(vals[y][x][n])):
                        v = vals[y][x][n][i]
                        #if (v == '-9999'): v = '0'
                        l += v + " "
                l = l[:-1]
                f.write(l + '\n')


def initCord (cord):
    cord.clear()
    for y in range(1000):
        rd = []
        for x in range(1000):
            rd.append('-9999')
        cord.append(rd)
            


def readFile(file,sd, mm, subFolder, sn):
    fileParts = file.split("_")  #Separate filename at _
    c = fileParts[0].upper()  #Location - for comparison change to uppercase
    cord = c[0:6]
    yr = fileParts[1][0:4]  #Year
    mt = fileParts[1][4:6]  #Month
    da = fileParts[1][6:8]  #Day

    fileloc = subFolder + file

    with open(fileloc, 'r') as f:
        ncols = int(f.readline()[6:].rstrip())
        nrows = int(f.readline()[6:].rstrip())
        xcorn = int(f.readline()[10:].rstrip())
        ycorn = int(f.readline()[10:].rstrip())
        cells = int(f.readline()[9:].rstrip())
        ndata = int(f.readline()[14:].rstrip())

        #print (mm[cXMIN], xcorn)
        if (mm[cXMIN] == None):   mm[cXMIN] = xcorn
        elif (xcorn < mm[cXMIN]): mm[cXMIN] = xcorn

        if (mm[cYMIN] == None): mm[cYMIN] = ycorn
        elif (ycorn < mm[cYMIN]):   mm[cYMIN] = ycorn

        if (mm[cXMAX] == None):   mm[cXMAX] = xcorn
        elif (xcorn > mm[cXMAX]): mm[cXMAX] = xcorn

        if (mm[cYMAX] == None): mm[cYMAX] = ycorn
        elif (ycorn > mm[cYMAX]):   mm[cYMAX] = ycorn

        #Read data rows
        drows = []
        for y in range(nrows):
            l = f.readline().rstrip()
            vals = l.split(' ')
            #print(y, vals)
            drows.append(vals)
        print("Len of dp=", len (drows), len(drows[0]))
            
        yData = [sn, cord, yr, xcorn, ycorn, drows]
        if not(yr in sd):
            sd[yr] = {cord:yData}
        else:
            if not(cord in sd[yr]):
                sd[yr][cord] = yData
        

def getFilesToRead(subFolder):
    os.chdir(subFolder)
    files = {}
    for file in glob.glob("??????_*.asc"):
        #print (file)
        fileParts = file.split("_")  #Separate filename at _
        c = fileParts[0].upper()  #Location - for comparison change to uppercase
        cord = c[0:6]
        yr = fileParts[1][0:4]  #Year
        mt = fileParts[1][4:6]  #Month
        da = fileParts[1][6:8]  #Day
        key = yr + " " + cord
        if key in files:
            #print("Duplicate file for this year", files[key], file)
            fileParts = files[key].split("_") 
            oldMt = fileParts[1][4:6]
            if int(mt) < int(oldMt):
                print ("Replaced")
                files[key] = file
        else:
            files[key] = file
    return files


def mergeYearPerSite(fileType, sn):
    #Create a list sites
    # nSites = os.listdir(rootDataFolder)
    # nSites.sort(key = int)
    # sSites = list()
    # print (nSites)
    # for x in nSites:
    #     print (x)
    #     sSites.append("Site " + x)
    
    # for sn in nSites:
        print("\n************************************")
        print ("Site ", sn)
        siteData = {}
        minmax = [None, None, None, None]

        subFolder = rootDataFolder + sn + "\\"
        os.chdir(subFolder)
        if fileType == "XX":
            file = None
            for file in glob.glob("??????XX_*.asc"):
                print (file)
                readFile(file,siteData, minmax, subFolder, sn)
            if (file == None): return
        else:
            filesToRead = getFilesToRead(subFolder)        
            for key, file in filesToRead.items():
                print (file)
                readFile(file,siteData, minmax, subFolder, sn)

        # file = None
        # for file in glob.glob("??????_*.asc"):
        #     print (file)
        #     readFile(file,siteData, minmax, subFolder, sn)
        # if (file == None): continue
    
                
        #print("Site Data len=", len(siteData))
        print (minmax[cXMIN],minmax[cYMIN],minmax[cXMAX],minmax[cYMAX])
        ncols = int((minmax[cXMAX] - minmax[cXMIN])/1000) + 1
        nrows = int((minmax[cYMAX] - minmax[cYMIN])/1000)+ 1
        print (ncols, nrows)
        #format of siteData
        #{"year" : {         cSITENUM    cCORD   cYEAR   cXLLC        cYLLC        cDVALS
        #            cord: [
        #                    'site num', 'cord', 'year', 'xllcorner', 'yllcorner', [
        #                                                                           [dv1, dv2, ... ,dv1000] <- row 1
        #                                                                           [dv1, dv2, ... ,dv1000] <- row 2
        #                                                                            ...
        #                                                                           [dv1, dv2, ... ,dv1000] <- row 1000
        #                                                                          ]
        #                  ]
        #          } 
        #
        for y in siteData:
            print (sn, y)
            for c in siteData[y]:
                print ("   ", c, len(siteData[y][c]), end=' [ ')
                for i in range(5): print (siteData[y][c][i], end=' ')
                print ('"CData"] ', len(siteData[y][c][5]))
            print ()

        #merge all cord for each year
        msd = []   #merged site data
        nodataVals = [] #no data cord dp vals 1000 x 1000 each of -9999
        initCord(nodataVals)
        for r in range(nrows):
            msdrd =[]
            for c in range(ncols):
                print ( r, c, end="    ")
                msdrd.append(nodataVals.copy())
            msd.append(msdrd)
            print()

        
        for sy in siteData:
            print ("Site year", sy)
            i = siteData[sy]
            print(len(i), minmax[cYMAX], minmax[cYMIN]-1000)
            for row in range(nrows):
                y =  minmax[cYMAX] - (row * 1000)
                print ("Row", row, y)
                
                for col in range(ncols):  # minmax[cXMIN], minmax[cXMAX]+1000, +1000
                    x = minmax[cXMIN] + (col * 1000)
                    print (col, x)
                    #found = False
                    for c in siteData[sy]:
                        #print (" Cord", c)
                        if (siteData[sy][c][4] == y) and (siteData[sy][c][3] == x):
                            #found = True
                            print ("      FOUND", siteData[sy][c][1], siteData[sy][c][3], siteData[sy][c][4], "\n")
                            ret = msd[row].pop(col)
                            msd[row].insert(col, siteData[sy][c][5])
                            #print (len(ret), len(siteData[sy][c][5]))
                            
                    #if not found: print("      --- NOT FOUND", x, y, "---\n")
            fn = "site" + "_" + sn + "_" + sy + ".asc"
            nc = str(ncols * 1000)
            nr = str(nrows * 1000)
            xll = str(minmax[cXMIN])
            yll = str(minmax[cYMIN])
            cell = '1'
            ndata = '-9999'
            writeSiteYearFile(fn, sn, nc, nr, xll, yll, cell, ndata, msd)


def main():
    #Create a list sites
    nSites = os.listdir(rootDataFolder)
    nSites.sort(key = int)
    sSites = list()
    print (nSites)
    for x in nSites:
        print (x)
        sSites.append("Site " + x)

    for sn in nSites: mergeYearPerSite("XX", sn)
    for sn in nSites: mergeYearPerSite("", sn)

main()
