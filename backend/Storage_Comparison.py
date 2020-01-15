# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os, csv, datetime, numpy
import matplotlib.pyplot as plt


# Read AECS
def aecs(reservoirID = 999903):
    infile = open('data/aec_modified/' + str(reservoirID) + '.txt', 'r')
    inlines = infile.readlines()
    elevations = []
    cumareas = []
    storages = []
    for line in inlines:
        elements = line.split(',')
        elevations.append(float(elements[0]))
        cumareas.append(float(elements[0]))
        storages.append(float(elements[0]))
    return elevations, cumareas

def deltaS(reservoirID = 999903, method = 'NDWI'):
    landsatdate = []
    surfacearea = []
    storagechanges = []

    reservoiraecinfo = aecs(reservoirID)
    elevations = reservoiraecinfo[0]
    cumareas = reservoiraecinfo[1]

    landsatfile = open(str(reservoirID) + '.csv', 'r')
    landsatdata = csv.DictReader(landsatfile, delimiter = ',')
    for row in landsatdata:
        landsatdate.append(datetime.datetime.strptime(row['Date'].replace('"', ''), "%b %d, %Y"))
        surfacearea.append(float(row[method]))

    surfacearea.sort(key = lambda date: landsatdate)
    storagechanges.append(0.0)
    for index in xrange(len(surfacearea)-1):
        elevation1 = 0.0
        for j in xrange(len(elevations)-1):
            if surfacearea[index] >= cumareas[j] and surfacearea[index] <= cumareas[j+1]:
                elevation1 = elevations[j]+(elevations[j+1] - elevations[j])/(cumareas[j+1]- cumareas[j])*(surfacearea[index] - cumareas[j])
        elevation2 = 0.0
        for j in xrange(len(elevations)-1):
            if surfacearea[index+1] >= cumareas[j] and surfacearea[index+1] <= cumareas[j+1]:
                elevation2 = elevations[j]+(elevations[j+1] - elevations[j])/(cumareas[j+1]- cumareas[j])*(surfacearea[index+1] - cumareas[j])
        storagechange = (surfacearea[index+1]+surfacearea[index])/2.0*(elevation2-elevation1)/1000
        storagechanges.append(storagechange)
    return landsatdate, storagechanges

def insitudeltas(reservoirID = 999903, landsatdates = []):
    infile = open('InsituData/ProcessedData.txt', 'r')
    indates = []
    storages = []
    deltaSs = []
    deltaSs.append(0)
    insitudata = csv.DictReader(infile, delimiter = '\t')
    for row in insitudata:
        if row[str(reservoirID)]!='-':
            indates.append(datetime.datetime.strptime(row['Date'], "%m/%d/%Y"))
            storages.append(float(row[str(reservoirID)]))
        
    for i in xrange(len(landsatdates)-1):
        deltas= storages[indates.index(landsatdates[i+1])] - storages[indates.index(landsatdates[i])]
        deltaSs.append(deltas)
        
    return deltaSs


    
def iterations(reservoirID = 999903):
    ndwidata = deltaS(reservoirID, 'NDWI')
    ndwidates = ndwidata[0]
    ndwideltas = ndwidata[1]
    mndwidata = deltaS(reservoirID, 'MNDWI')
    mndwidates = mndwidata[0]
    mndwideltas = mndwidata[1]
    widata = deltaS(reservoirID, 'WI')
    widates = widata[0]
    wideltas = widata[1]
    insitudata = insitudeltas(reservoirID, widates)
    
    with open('Data/' + str(reservoirID) + '_storage_change.txt', 'w') as txt:
        for x in xrange(len(ndwidates)):
            txt.write(datetime.datetime.strftime(ndwidates[x], "%Y-%m-%d") + "," + str(ndwideltas[x]) + "," + str(mndwideltas[x]) + "," + str(wideltas[x]) + "," + str(insitudata[x]) + '\n')
    fig = plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(ndwidates, ndwideltas, 'g-', label='NDWI',linewidth=2.0)
    plt.plot(mndwidates, mndwideltas, 'c-', label='MNDWI',linewidth=2.0)
    plt.plot(widates, wideltas, 'r-', label='WI',linewidth=2.0)
    plt.plot(widates, insitudata, 'b-', label='In-situ',linewidth=3.0)
    plt.legend(loc='upper left')
    plt.savefig(str(reservoirID)+ '.png')

def storagefromaec(reservoirID):
    infile = open('Analysis/storage/fromaec/' + str(reservoirID) + '.txt', 'r')
    inlines = infile.readlines()
    elevations = []
    cumareas = []
    for line in inlines:
        if "Elevation" not in line:
            elements = line.split(',')
            elevations.append(float(elements[0]))
            cumareas.append(float(elements[1]))
    storages = []
    for i in xrange(len(elevations)):
        if i==0:
            storage = 0
            storages.append(0)
        else:
            storage = (cumareas[i] + cumareas[i-1])/2.0*(elevations[i]-elevations[i-1])/1000.0
            storages.append(storage + storages[i-1])  
    return elevations, cumareas, storages
        
#    with open('data/storage/' + str(reservoirID) + '.txt', 'w') as txt:
#        for x in xrange(len(elevations)):
#            txt.write(str(elevations[x]) + "," + str(cumareas[x]) + "," + str(storages[x]) + '\n')
    
def storage(reservoirID = 999903, method = 'NDWI'):
    landsatdate = []
    surfacearea = []
    storages = []

    reservoiraecinfo = storagefromaec(reservoirID)
    cumareas = reservoiraecinfo[1]
    storage_aec = reservoiraecinfo[2]
    
    landsatfile = open('Analysis/sarea/l8/' + str(reservoirID) + '.txt', 'r')
    landsatdata = csv.DictReader(landsatfile, delimiter = ',')
    for row in landsatdata:
        landsatdate.append(datetime.datetime.strptime(row['Date'], "%Y-%m-%d"))
        surfacearea.append(float(row[method]))
    surfacearea.sort(key = lambda date: landsatdate)
    
    for index in xrange(len(surfacearea)):
        storagett = 0.0
        for j in range(1, len(cumareas)):
            if surfacearea[index] >= cumareas[j-1] and surfacearea[index] <= cumareas[j]:
                if (cumareas[j]- cumareas[j-1]) >= 0.0:
                    storagett = storage_aec[j-1]+(storage_aec[j] - storage_aec[j-1])/(cumareas[j]- cumareas[j-1])*(surfacearea[index] - cumareas[j-1])
        storages.append(storagett)
    return landsatdate, storages
     
#    with open('data/storage/landsat_' + str(reservoirID) + '.txt', 'w') as txt:
#        for x in xrange(len(landsatdate)):
#            txt.write(landsatdate[x].strftime("%Y-%m-%d") + "," + str(surfacearea[x]) + "," + str(storages[x]) + '\n')


def insitustorage(reservoirID = 999903, landsatdates = []):
    infile = open('Analysis/insitu/ProcessedData.txt', 'r')
    indates = []
    storages = []
    insituS = []
    datess = []
    insitudata = csv.DictReader(infile, delimiter = '\t')
    for row in insitudata:
        if row[str(reservoirID)]!='-':
            indates.append(datetime.datetime.strptime(row['Date'], "%m/%d/%Y"))
            storages.append(float(row[str(reservoirID)]))
        
    for i in xrange(len(landsatdates)):
        if landsatdates[i] in indates:
            storage= storages[indates.index(landsatdates[i])]
            datess.append(indates[indates.index(landsatdates[i])])
            insituS.append(storage)

        
    return datess, insituS

selres = [5121,4860,4880,4961,4949,4953,4943,4952,4898,4861,4857,4863,4862,4865,4796,4795,4858,4826,4885,4859,4843,4881,4876,4953,4883,4991,4997,4991,5035,5039,5014,5015,5029,4953,4985,4946,4985,5002,4780,4989,4990,5000,5013,4992,4994,4776,5009,5043,5040,5024,5041,4739,4937,4768,4772,4752,4755,4748,4938,4908,4753,4895,4765,4942,4964,4994,4729,4743,4736,5002,4734,4737,4791,4836,4728,4793,4792]
#selres = [5039]

def corrcoef(insitu = [], satellite = []):
    return numpy.corrcoef(numpy.asarray(insitu), numpy.asarray(satellite))[0][1]

def standdev(satellite = []):
    return numpy.std(numpy.asarray(satellite))
def rmse(insitu = [], satellite = []):
    predictions = numpy.asarray(satellite)
    targets = numpy.asarray(insitu)
    return numpy.sqrt(numpy.mean((predictions-targets)**2))/numpy.mean(targets)

for reservoirID in selres:
    l8ndwistdata = storage(reservoirID)
    l8dates = l8ndwistdata[0]
    l8ndwist = l8ndwistdata[1]
    insitustdata = insitustorage(reservoirID, l8dates)
    insitudates = insitustdata[0]
    insitust = insitustdata[1]
    l8mndwistdata = storage(reservoirID, 'MNDWI')
    l8wistdata = storage(reservoirID, 'WI')
    l8aweishstdata = storage(reservoirID, 'AWEISH')
    l8aweinshstdata = storage(reservoirID, 'AWEINSH')
    l8mndwist = l8mndwistdata[1]
    l8wist = l8wistdata[1]
    l8aweishst = l8aweishstdata[1]
    l8aweinshst = l8aweinshstdata[1]

#    fig = plt.figure(figsize=(10, 6), dpi=300)
#    plt.plot(dates, l8ndwist, 'g--', label='L8-NDWI',linewidth=2.0)
#    plt.plot(dates, l8mndwist, 'y--', label='L8-MNDWI',linewidth=2.0)
#    plt.plot(dates, l8wist, 'b--', label='L8-WI',linewidth=2.0)
#    plt.plot(dates, l8aweist, 'c--', label='L8-AWEI',linewidth=2.0)
#    plt.plot(insitust[0], insitust[1], 'r-', label='In Situ',linewidth=2.0)
#    plt.legend(loc='upper left')
#    plt.savefig('Analysis/Figures/' + str(reservoirID)+ '.png')
    count = 0
    for x in l8dates:
        if x not in insitudates:
            l8ndwist.pop(l8dates.index(x)-count)
            l8mndwist.pop(l8dates.index(x)-count)
            l8wist.pop(l8dates.index(x)-count)
            l8aweishst.pop(l8dates.index(x)-count)
            l8aweinshst.pop(l8dates.index(x)-count)
            count = count+1
    
    print reservoirID, rmse(insitust, l8ndwist), rmse(insitust, l8mndwist), rmse(insitust, l8wist), rmse(insitust, l8aweishst)