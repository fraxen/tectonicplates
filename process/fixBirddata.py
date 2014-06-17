import sys,os
import subprocess

if os.getcwd().find('process') > 0:
	outDir = os.path.abspath(os.path.join(os.getcwd(),'..'))
else:
	outDir = os.getcwd()

pbData = [\
	{'file':'PB2002_boundaries','geom':'line','type':'plate boundary'},\
	{'file':'PB2002_orogens','geom':'poly','type':'orogen'},\
	{'file':'PB2002_plates','geom':'poly','type':'plate'},\
	# {'file':'PB2002_poles','geom':'point','type':'poles'},\
	# {'file':'PB2002_steps','geom':'point','type':'steps'},\
	]


for dataset in pbData:
	# Prepare each data file for conversion in Global Mapper
	outData = os.path.join(os.environ['TEMP'],dataset['file'] + '2.txt')
	outBuffer = ''

	with open(os.path.join('original',dataset['file'] + '.dig.txt')) as fp:
		for line in fp:
			if line == '*** end of line segment ***\n':
				continue
			if line[0] == ' ':
				outBuffer = outBuffer + line
				continue
			outBuffer = outBuffer + 'Type,' + dataset['type'] + '\n'
			if line.find('    ') > 0:
				outBuffer = outBuffer + 'Name,' + line.split(' ')[0] + '\n'
				outBuffer = outBuffer + 'Source,' + ' '.join(line.split(' ')[1:]).strip() + '\n'
			else:
				outBuffer = outBuffer + 'Name,' + line.strip() + '\n'
	with open(outData,'w') as fp:
		fp.write(outBuffer)

# Next we process all the data files in GM
gmScript = os.path.join(os.environ['TEMP'],"dataprocess.gms")
with open(gmScript,'w') as fp:
	fp.write('GLOBAL_MAPPER_SCRIPT VERSION=1.00')
	for dataset in pbData:
		if dataset['geom'] == 'line': gmShpType = 'LINES'
		if dataset['geom'] == 'poly': gmShpType = 'AREAS'
		if dataset['geom'] == 'point': gmShpType = 'POINTS'
		fp.write('UNLOAD_ALL\n')
		fp.write('IMPORT_ASCII FILENAME="%s" TYPE="POINT_AND_LINE" COORD_DELIM=AUTO COORD_ORDER=X_FIRST PROJ_EPSG_CODE=4326 LABEL_FIELD=Name\n' \
			% os.path.join(os.environ['TEMP'],dataset['file'] + '2.txt') )
		fp.write('EXPORT_VECTOR FILENAME="%s" TYPE="SHAPEFILE" SHAPE_TYPE="%s" GEN_PRJ_FILE=YES OVERWRITE_EXISTING=YES GEN_MULTI_PATCH=YES\n' \
			% (os.path.join(outDir,dataset['file'] + '.shp'), 'LINES') )

# Execute GM
subprocess.call(['cmd.exe','/c','start','global_mapper11.exe', gmScript])
sys.exit()

























































# I sort of gave up on the stuff below, got too messy with trying to fix inconsistency along the -180/180 line
import sys
import arcpy

arcpy.env.workspace = r'C:\data\library\world_geo\peterbird'
arcpy.env.overwriteOutput = True

pbData = [\
	{'file':'PB2002_boundaries','geom':'line','type':'plate boundary'},\
	{'file':'PB2002_orogens','geom':'poly','type':'orogen'},\
	{'file':'PB2002_plates','geom':'poly','type':'plate'},\
	]

for dataset in pbData:
	point = arcpy.Point()
	array = arcpy.Array()

	featureList = []
	outData = dataset['file']+'.shp'
	if dataset['geom'] == 'line':
		arcpy.CreateFeatureclass_management(arcpy.env.workspace,outData,'POLYLINE','','ENABLED','DISABLED',r'C:\home\hugo\AppData\Roaming\ESRI\Desktop10.2\ArcMap\Coordinate Systems\WGS 1984.prj')
	else:
		arcpy.CreateFeatureclass_management(arcpy.env.workspace,outData,'POLYGON','','ENABLED','DISABLED',r'C:\home\hugo\AppData\Roaming\ESRI\Desktop10.2\ArcMap\Coordinate Systems\WGS 1984.prj')
	for field in ['type','name','source']:
		arcpy.AddField_management(outData,field,"TEXT")
	cursor = arcpy.da.InsertCursor(outData,('type','name','source','SHAPE@'))
	with open(dataset['file'] + '.dig.txt') as fp:
		array.removeAll()
		attName = ''
		for line in fp:
			# First line is attribute
			if attName == '':
				attName = line
				attType = dataset['type']
				attSource = ''
				if line.find('     ') > 0:
					attName = line.split(' ')[0]
					attSource = ' '.join(line.split(' ')[1:]).lstrip()
				continue
			if line != '*** end of line segment ***\n':
				point.X = float(line.split(',')[0])
				point.Y = float(line.split(',')[1])
				array.add(point)
			else:
				print 'Adding segment:' + attName
				if dataset['geom'] == 'line':
					cursor.insertRow((attType,attName,attSource,arcpy.Polyline(array)))
				else:
					cursor.insertRow((attType,attName,attSource,arcpy.Polygon(array)))
				array.removeAll()
				attName = ''
	del cursor
	del point
	del array
