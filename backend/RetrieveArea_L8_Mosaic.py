# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:43:53 2019

@author: nbiswas
"""
import ee
import os
ee.Initialize()

L8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT")
reservoirs = ee.FeatureCollection("users/nbiswas/grand1p3_reservoirs_saafseasia")

selreservoir = 1987;
selected = reservoirs.filter(ee.Filter.equals('GRAND_ID', selreservoir));

reservoir = selected;
rgeometry = reservoir.geometry();
bgeometry = reservoir.geometry().buffer(3000);
rbufferarea = bgeometry.area().divide(1000000);
rarea = rgeometry.area().divide(1000000);
print(rarea.getInfo());
print(rbufferarea.getInfo());

Date_Start = ee.Date('2013-08-01');
Date_End = ee.Date('2019-11-01');
diffday = Date_End.difference(Date_Start,'day').round();

indexes = ee.List.sequence(0,diffday,16);
print(indexes.getInfo());

def datelist(n):
    return Date_Start.advance(n, 'days')


dates = indexes.map(datelist);


    

def clipimage(img):
    return img.clip(bgeometry);

def getQABits(image, start, end, newName):
    #Compute the bits we need to extract.
    pattern = 0;
    for i in range(start, end+1):
       pattern += 2**i

    #Return a single band image of the extracted QA bits, giving the band a new name.
    return image.select([0], [newName]).bitwiseAnd(pattern).rightShift(start);

  
def cloud_shadows(image):
    # Select the QA band.
    QA = image.select(['BQA'])
    # Get the internal_cloud_algorithm_flag bit.
    return getQABits(QA, 7,8, 'Cloud_shadows').eq(1)
    
def clouds(image):
    QA = image.select(['BQA'])
    # Get the internal_cloud_algorithm_flag bit.
    return getQABits(QA, 4,4, 'Cloud').eq(0)

def maskClouds(image):
    cs = cloud_shadows(image)
    c = clouds(image)
    image = image.updateMask(cs)
    return image.updateMask(c)


def mosaicseries(Date_Start):
    startdate = ee.Date(Date_Start);
    enddate = startdate.advance(1,'months');
    l8images = L8.filterDate(startdate,enddate).filterBounds(bgeometry);
    l8images = l8images.map(clipimage)
    
    #Filtring out cloudy pixels from calculation
    l8images2 = l8images.map(maskClouds);
    
#    print(l8images2.first());
    
    l8mosaic = l8images2.mosaic().set('mosaicdate', startdate.advance(8,'days'));
    area = l8mosaic.gt(0).multiply(ee.Image.pixelArea()).divide(1000000).reduceRegion(
      reducer = ee.Reducer.sum(), 
      geometry = bgeometry, 
      scale = 1000,
      maxPixels = 1e10
    ).get('B3')
    
#        print(l8mosaic);
    return l8mosaic.set('rarea', area)
    
ppp = dates.map(mosaicseries);
cjkdnkjvn = ee.ImageCollection(ppp)
xlist = cjkdnkjvn.reduceColumns(ee.Reducer.toList(2), ['mosaicdate', 'rarea']).get('list')
print(xlist.getInfo())
