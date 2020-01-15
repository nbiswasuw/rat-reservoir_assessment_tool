'''
Created on Aug 11, 2019

@author: nbiswas
'''
# from osgeo import ogr

import datetime, ee, math, os
ee.Initialize()


allreservoirs = ee.FeatureCollection("users/nbiswas/sereservoirs")

Date_Start = ee.Date('2015-01-01');
Date_End = ee.Date('2019-09-31');
        
def clipimage(img):
    return img.clip(bgeometry);



def l8aweish(img):
    aweish = img.expression(
    'BLUE + 2.5 * GREEN - 1.5 * (NIR + SWIR1) - 0.25 * SWIR2', {
      'BLUE': img.select('B3'),
      'GREEN': img.select('B3'),
      'NIR': img.select('B5'),
      'SWIR1':img.select('B6'),
      'SWIR2':img.select('B7')
    }).rename('AWEISH');
    return img.addBands(aweish)

def tareadate(img):
    area = img.gt(0).multiply(ee.Image.pixelArea()).divide(1000000).reduceRegion(
      reducer = ee.Reducer.sum(), 
      geometry = rgeometry, 
      scale = calcScale,
      maxPixels = 10e9
    ).get('B3')
    return img.set('rarea', area).set('date', ee.Date(img.get('system:time_start')).format('YYYY-MM-dd'))

def ndwiarea(img):
    area = img.gt(0).multiply(ee.Image.pixelArea()).divide(1000000).reduceRegion(
      reducer = ee.Reducer.sum(), 
      geometry = bgeometry, 
      scale = calcScale,
      maxPixels = 10e9
    ).get('NDWI');
    return img.set('ndwi', area)
        
def mndwiarea(img):
    area = img.gt(0).multiply(ee.Image.pixelArea()).divide(1000000).reduceRegion(
      reducer = ee.Reducer.sum(), 
      geometry = bgeometry, 
      scale = calcScale,
      maxPixels = 10e9
    ).get('MNDWI')
    return img.set('mndwi', area)

def wiarea(img):
    area = img.gt(0).multiply(ee.Image.pixelArea()).divide(1000000).reduceRegion(
      reducer = ee.Reducer.sum(), 
      geometry = bgeometry, 
      scale = calcScale,
      maxPixels = 10e9
    ).get('WI')
    return img.set('wi', area)

def aweisharea(img):
    area = img.gt(0).multiply(ee.Image.pixelArea()).divide(1000000).reduceRegion(
      reducer = ee.Reducer.sum(), 
      geometry = bgeometry, 
      scale = calcScale,
      maxPixels = 10e9
    ).get('AWEISH')
    return img.set('aweish', area)

def aweinsharea(img):
    area = img.gt(0).multiply(ee.Image.pixelArea()).divide(1000000).reduceRegion(
      reducer = ee.Reducer.sum(), 
      geometry = bgeometry, 
      scale = calcScale,
      maxPixels = 10e9
    ).get('AWEINSH')
    return img.set('aweinsh', area)


def extentseries(reservoir):
    rgeometry = reservoir.geometry();
    bgeometry = reservoir.geometry().buffer(3000)

#    bufferarea = bgeometry.area().divide(1000000)
    rarea = rgeometry.area().divide(1000000)
    
    Date_Start = ee.Date('2008-01-01')
    Date_End = ee.Date('2019-09-30')
    l8images = L8.filterDate(Date_Start,Date_End).filterBounds(bgeometry)
    l8images = l8images.map(clipimage)
    l8images = l8images.map(maskClouds)
    l8images = l8images.select(["B2", "B3","B4","B5","B6","B7"]);


    l8areas = l8images.map(tareadate)
    l8areas = l8areas.filter(ee.Filter.gt('rarea', rarea.multiply(.80)));
    
    l8images = l8areas.map(l8ndwi);
    l8images = l8images.map(l8mndwi);
    l8images = l8images.map(l8wi);
    l8images = l8images.map(l8aweinsh);
    l8images = l8images.map(l8aweish);
        
    # calculate ndwi for each image in imagecollection
    l8images = l8images.map(ndwiarea);
    l8images = l8images.map(mndwiarea);
    l8images = l8images.map(wiarea);
    l8images = l8images.map(aweisharea);
    mosaics = l8images.map(aweinsharea)
    mosaics = ee.ImageCollection(mosaics);
    mosaic = mosaics.sort('system:time_start', True);
    list = mosaic.reduceColumns(ee.Reducer.toList(7), ['date', 'rarea','ndwi','mndwi', 'wi', 'aweish', 'aweinsh']).get('list');
#    print list.getInfo();
    return list.getInfo();
    
      
reservoirids = [4699,4700,4701,4702,4703,4704,4705,4706,4707,4708,4709,4710,4711,4712,4713,4714,4717,4718,4719,4721,4722,4723,4724,4725,4726,4727,4728,4729,4730,4731,4732,4733,4734,4735,4736,4737,4738,4739,4740,4741,4742,4743,4744,4745,4746,4747,4749,4750,4751,4752,4753,4754,4755,4756,4757,4758,4759,4760,4761,4762,4763,4764,4765,4766,4767,4768,4770,4771,4772,4773,4774,4776,4777,4778,4779,4780,4781,4782,4791,4792,4793,4794,4795,4796,4797,4798,4799,4800,4801,4802,4803,4804,4805,4806,4807,4808,4809,4810,4811,4812,4813,4814,4815,4816,4817,4818,4819,4820,4821,4822,4823,4824,4825,4826,4827,4828,4829,4830,4831,4832,4833,4834,4835,4836,4837,4838,4839,4840,4841,4842,4843,4844,4845,4846,4847,4848,4849,4850,4851,4852,4853,4854,4855,4856,4857,4858,4859,4860,4861,4862,4863,4864,4865,4866,4867,4868,4870,4871,4872,4873,4874,4875,4876,4877,4879,4880,4881,4882,4883,4884,4885,4886,4887,4888,4889,4890,4891,4892,4893,4894,4895,4896,4897,4898,4899,4900,4901,4902,4903,4904,4905,4906,4908,4909,4910,4911,4912,4913,4914,4915,4916,4917,4918,4919,4920,4921,4922,4923,4924,4925,4926,4927,4928,4929,4930,4931,4932,4933,4934,4935,4937,4938,4939,4940,4941,4942,4943,4944,4945,4946,4947,4948,4949,4950,4951,4952,4953,4954,4955,4956,4957,4958,4959,4960,4961,4962,4963,4964,4965,4966,4967,4968,4969,4970,4971,4972,4973,4974,4975,4976,4977,4979,4980,4981,4982,4983,4984,4985,4986,4987,4988,4989,4990,4991,4992,4993,4994,4995,4996,4997,4998,4999,5000,5001,5002,5003,5004,5005,5006,5007,5008,5009,5010,5011,5012,5013,5014,5015,5016,5017,5018,5019,5020,5021,5023,5024,5025,5026,5027,5028,5029,5030,5031,5032,5033,5034,5035,5036,5037,5038,5039,5040,5041,5043,5087,5095,5096,5100,5102,5103,5107,5108,5111,5113,5116,5117,5118,5120,5121,5122,5123,5124,5125,5126,5127,5128,5129,5130,5131,5132,5133,5134,5135,5136,5137,5138,5139,5140,5141,5143,5145,5146,5147,5148,5149,5150,5151,5152,5153,5154,5155,5156,5157,5158,5159,5160,5161,5162,5163,5164,5779,5782,5795,5796,5797,5798,5799,5800,5801,5802,5803,6844,6846,6847,6848,6849,6850,6852,6854,6855,6856,6857]

for reservoirid in reservoirids:
    series = "Date,Rarea,NDWI"
    selected = allreservoirs.filter(ee.Filter.equals('GRAND_ID', reservoirid))
    rgeometry = selected.geometry()
    bgeometry = selected.geometry().buffer(3000)
    
    rarea = rgeometry.area().divide(1000000)
    if rarea<=30.0:
        calcScale = 30.0
    elif rarea>30.0 and rarea<= 100:
        calcScale = 60.0
    else:
        calcScale = 100.0
    
    area1 = bgeometry.area().divide(1000000)
    area2 = rgeometry.area().divide(1000000)
    print str(reservoirid) + ',Reservoir Area: ' + str(area2.getInfo()) + ',Reservoir Buffer Area: ' + str(area1.getInfo()) + ',Computation Scale: ' + str(calcScale)
    
    try:        
        ppp = extentseries(selected);
        for xxx in ppp:
            series = series + '\n' + xxx[0] + "," + str(xxx[1]) + "," + str(xxx[2])+ "," +str(xxx[3]) + "," + str(xxx[4])+"," + str(xxx[5]) + "," + str(xxx[6])
            with open('sarea/L8/' + str(reservoirid) + '.txt', 'w') as txt:
                txt.write(series)
        print 'Done with ' + str(reservoirid)
    except:
        print 'problem with ' + str(reservoirid)
        continue
