import os
import glob

#Create Variables
groupName = 'DATA_YEAR_PER_SITE'
rootDataFolder = 'D:\\Balraj\\WIP\\DATA_OUT\\'
rLayers = list()
nLayers = list()
yLayers = list()
cLayers = list()

def keyForSort(e):
    line = e.split("_")
    sSite = line[1]
    return int(sSite)

    

def main():
    #Create Site data layers
    root = QgsProject.instance().layerTreeRoot()
    gData = root.findGroup(groupName)
    if (not gData):
        gData = root.addGroup(groupName)

    os.chdir(rootDataFolder)
    fileToRender = []
    for df in glob.glob("*.asc"):
        fileToRender.append(df)
    fileToRender.sort(key=keyForSort)
    
    for df in fileToRender:
        line = df.split("_")
        #line = df.split(",")
        sSite = "Site " + line[1]
        sYear = line[2][0:4]
        sFname = df
        sFpath = rootDataFolder + df
        #sCord   = line[4].rstrip() #Remove the '\n' at the end
        print (sSite, sYear, sFname)
        #if (sSite == "Site 2"): break 
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

main()
