import os
import glob

#Create Variables
groupName = 'DATA_CALCS2'
rootDataFolder = # 'Drive:\\'
rLayers = list()
nLayers = list()
yLayers = list()
gData   = None

def keyForSortByYear(e):
    line = e.split("_")
    return int(line[2][5:9])

    

def main():
    global gData
    #Get files to render
    os.chdir(rootDataFolder)
    minDataVal = 9999
    maxDataVal = 0
    
    maxYear = 0
    minYear = 9999
    maxSite = 0
    fileToRender = {}
    for df in glob.glob("*.asc"):
        dfp = df.split('_')
        sn = int(dfp[1])
        byr = int(dfp[2][0:4])
        if sn > maxSite: maxSite = sn
        if byr < minYear: minYear = byr
        if byr > maxYear: maxYear = byr
        if not (sn in fileToRender):
            fileToRender[sn] =  {byr : [df]} 
        else:
            if not (byr in fileToRender[sn]):
                fileToRender[sn][byr] = [df]
            else:
                fileToRender[sn][byr].append(df)

    #sort with highest year first one in array
    for s in range(1, maxSite + 1):
        yrs = fileToRender[s]
        for y in range(maxYear, minYear-1, -1):
            if (y in yrs):
                yrs[y].sort(reverse=True, key=keyForSortByYear)

 
    #Create Site data layers
    root = QgsProject.instance().layerTreeRoot()
    gData = root.findGroup(groupName)
    if not gData:
        gData = root.addGroup(groupName)
        
    for s in range(1, maxSite + 1):
        yrs = fileToRender[s]
        for y in range(maxYear, minYear-1, -1):
            if (y in yrs):
                yfiles = yrs[y]
                for df in yfiles:
                    line = df.split("_")
                    sSite = "Site " + line[1]
                    sYear = line[2][0:4]
                    sFname = line[2][0:9]
                    sFpath = rootDataFolder + df
                    print (sSite, sFname, end="  ")
                    nLayer = gData.findGroup(sSite)  #Site 1, Site 2, etc
                    if (not nLayer):
                        nLayer = gData.addGroup(sSite)  #Site 1, Site 2, etc
                    nLayers.append(nLayer)

                    yLayer = nLayer.findGroup(sYear)  #2007, 2008, 2009 etc
                    if (not yLayer):
                        yLayer = nLayer.addGroup(sYear)  #2007, 2008, 2009 etc
                    yLayers.append(yLayer)

                    #Add layers to map
                    rLayer =QgsRasterLayer(sFpath, sFname)
                    rLayers.append(rLayer)
                    yLayer.addLayer(rLayer)
                    
                    provider = rLayer.dataProvider()
                    ext = rLayer.extent()
                    stats = provider.bandStatistics(1,QgsRasterBandStats.All,ext,0)
                    print ("Min: {:2.4f}  Max: {:2.4f}".format(stats.minimumValue, stats.maximumValue))
                    if stats.minimumValue < minDataVal : minDataVal = stats.minimumValue
                    if stats.maximumValue > maxDataVal : maxDataVal = stats.maximumValue
                    #print ("mean = ", stats.mean)
                    #print ("stdDev = ", stats.stdDev)
                    #break
                #break
        #break
    print ("\nSite Data Values: Min: {:2.4f}  Max: {:2.4f}".format(minDataVal, maxDataVal))


main()
