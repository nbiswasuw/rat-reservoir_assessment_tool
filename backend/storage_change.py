import csv
reservoirs = ['Mdhsn','Lwshn','Nukng','Nuzdu','Xioan']
for i in xrange(len(reservoirs)):
	elevations = []
	cumareas = []
	aecfile = open('Parameters/' + reservoirs[i] + '_AEC.txt', 'r')
	aecdata = csv.DictReader(aecfile, delimiter = '\t')
	for row in aecdata:
		elevations.append(float(row['Elevation']))
		cumareas.append(float(row['CumArea']))
	landsatdate = []
	surfacearea = []
	landsatfile = open('./Reservoir_Area/Reservoir_' + reservoirs[i] + '.txt', 'r')
	landsatdata = csv.DictReader(landsatfile, delimiter = '\t')
	for row in landsatdata:
		landsatdate.append(row['Date'])
		surfacearea.append(float(row['Area']))

	strstoragechange = 'Date, Storage Change (km3)'
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
		strstoragechange = strstoragechange + '\n' + landsatdate[index+1] + ',' + "{0:0.4f}".format(storagechange)
	storagechangefile = 'Storage_Change/' + reservoirs[i] + '_storage_change.txt'
	with open(storagechangefile, 'w') as txt:
		txt.write(strstoragechange)
