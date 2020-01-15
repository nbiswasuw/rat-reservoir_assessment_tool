import os, csv
import datetime

for fn in os.listdir('./data/inflow/'):
    reservoir = fn[:-4]
    print reservoir
    storagedate = []
    storagevol = []
    if os.path.exists('./data/deltas/l8/' + reservoir + '.txt') == True:
        storagefile = open('./data/deltas/l8/' + reservoir + '.txt', 'r')
        storagedata = storagefile.readlines()
        for lines in storagedata:
            line = lines.split(',')
            rdate = datetime.datetime.strptime(line[0], "%Y-%m-%d")
            storagedate.append(rdate)
            storagevol.append(float(line[1]))
    
        hindcastdate = []
        hindcastinflow = []
        hindcastfile = open('data/inflow/' + reservoir + '.txt', 'r')
        hindcast = csv.DictReader(hindcastfile, delimiter = ',')
    
        for row in hindcast:
            hindcastdate.append(datetime.datetime.strptime(row['Date'], '%Y-%m-%d'))
            hindcastinflow.append(float(row['Streamflow']))
    
        str2forecast = "Date,Streamflow"
        for dateindex in xrange(len(storagedate)-1):
            inflowvol = 0.0
            fdate = storagedate[dateindex]
            sdate = storagedate[dateindex+1]
            for j in xrange(len(hindcastdate)):
                if hindcastdate[j]>=fdate and hindcastdate[j]<=sdate:
                    inflowvol = inflowvol + hindcastinflow[j]*86400
            outflowvol = inflowvol - storagevol[dateindex]*1000000000.0
            if float((sdate-fdate).days)==0.0:
                outflowrate = 0.0
            else:
                outflowrate = outflowvol/(float((sdate-fdate).days)*86400)
                if outflowrate<0:
                    outflowrate = 0.0
            
            str2forecast= str2forecast + '\n' + datetime.datetime.strftime(sdate, '%Y-%m-%d') + ',' + "{0:.2f}".format(outflowrate)
        with open('./data/outflow/' + reservoir + '.txt', 'w') as txt:
            txt.write(str2forecast)
