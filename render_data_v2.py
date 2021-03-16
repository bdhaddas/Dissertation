import os
import glob

#Create Variables
srcFile = 'D:\\Balraj\\WIP\\gooddata.txt'
groupName = 'DATA'


#Create Site data layers
root = QgsProject.instance().layerTreeRoot()
gData = root.findGroup(groupName)  #DATA
if (not gData):
    gData = root.addGroup(groupName)  #DATA

rLayers = list()
nLayers = list()
yLayers = list()
cLayers = list()

with open(srcFile, 'r') as f:
    for df in f:
        line = df.split(",")
        sSite = line[0]
        sYear = line[1]
        sFname = line[2]
        sFpath = line[3]
        sCord   = line[4].rstrip() #Remove the '\n' at the end
        print (sSite, sFname)
        #if (sSite == "Site 2"): break 
        nLayer = gData.findGroup(sSite)  #Site 1, Site 2, etc
        if (not nLayer):
            nLayer = gData.addGroup(sSite)  #Site 1, Site 2, etc
        nLayers.append(nLayer)

        cLayer = nLayer.findGroup(sCord)  #SW8161, SW8262 etc
        if (not cLayer):
            cLayer = nLayer.addGroup(sCord)  #SW8161, SW8262 etc


        yLayer = cLayer.findGroup(sYear)  #2007, 2008, 2009 etc
        if (not yLayer):
            yLayer = cLayer.addGroup(sYear)  #2007, 2008, 2009 etc
        yLayers.append(yLayer)

        #Add layers to map
        rLayer =QgsRasterLayer(sFpath, sFname)
        rLayers.append(rLayer)
        yLayer.addLayer(rLayer)
    
