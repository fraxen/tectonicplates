import sys
import os
import re
import base64
import platform
from xml.etree import ElementTree
import arcpy

basepath = os.path.abspath(os.path.join(sys.argv[0], '../..'))

mxd = arcpy.mapping.MapDocument(os.path.join(basepath, 'tools', 'data_thumb.mxd'))
df = arcpy.mapping.ListDataFrames(mxd)[0]

arcpy.env.workspace = basepath
shpFiles = arcpy.ListFeatureClasses()
for shp in shpFiles:
    print '  Fixing ' + shp

    # Generate thumbnail
    lyrThumb = arcpy.mapping.Layer(shp)
    arcpy.mapping.AddLayer(df, lyrThumb, 'BOTTOM')
    arcpy.mapping.ExportToJPEG(
        mxd, os.path.join(os.environ['TEMP'], 'thumb.jpg'), df, 200, 133, '', False, '24-BIT_TRUE_COLOR', 60
    )
    for lyr in arcpy.mapping.ListLayers(df):
        arcpy.mapping.RemoveLayer(df, lyr)

    # Import metadata
    metaFile = os.path.join(basepath, shp + '.xml')
    if platform.architecture()[0] != '64bit':
        if os.path.exists(metaFile):
            os.remove(metaFile)
        arcpy.ImportMetadata_conversion(
            os.path.join(basepath, 'tools', 'plates_template.xml'), 'FROM_ISO_19139', shp, 'ENABLED'
        )

    # Fix metadata
    metaDoc = ElementTree.parse(metaFile)

    # Fix title
    title = re.sub('ne_(\d+m)_(.*).shp', r'\2 (1:\1)', shp)
    title = title.replace('_', ' ')
    title = re.sub('(admin \d) (.*) (\(.*\))', r'\2, \1 \3', title).title()
    metaDoc.findall('.//itemProps/itemName')[0].text = title
    del metaDoc.findall('.//itemProps/itemName')[0].attrib['Sync']
    metaDoc.findall('.//itemProps/itemName')[0].attrib['Sync'] = 'FALSE'
    metaDoc.findall('.//dataIdInfo/idCitation/resTitle')[0].text = title
    del metaDoc.findall('.//dataIdInfo/idCitation/resTitle')[0].attrib['Sync']
    metaDoc.findall('.//dataIdInfo/idCitation/resTitle')[0].attrib['Sync'] = 'FALSE'

    # Fix credit
    metaDoc.findall('.//idCredit')[0].text = re.sub(' Hugo', '\nHugo', metaDoc.findall('.//idCredit')[0].text)

    # Fix Thumbnail
    bin = ElementTree.Element('Binary')
    thumb = ElementTree.SubElement(bin, 'Thumbnail')
    thumbData = ElementTree.SubElement(thumb, 'Data')
    with open(os.path.join(os.environ['TEMP'], 'thumb.jpg'), 'rb') as thumbFile:
        thumbData.text = base64.b64encode(thumbFile.read())
    thumbData.attrib['EsriPropertyType'] = 'PictureX'
    metaDoc.getroot().append(bin)

    # Insert scalerange
    sr = ElementTree.Element('scaleRange')
    minScale = ElementTree.SubElement(sr, 'minScale')
    minScale.text = re.sub('.*\(1:(.*)M\)', r'\1', title) + '000000'
    maxScale = ElementTree.SubElement(sr, 'maxScale')
    maxScale.text = minScale.text
    metaDoc.findall('.//Esri')[0].append(sr)

    # add tags
    for tagType in ['otherKeys', 'searchKeys']:
        tag = ElementTree.Element('keyword')
        tag.text = re.sub('(.*), .*', r'\1', title)
        metaDoc.findall('.//' + tagType)[0].append(tag)
        if title.find('Admin') > 0:
            tag = ElementTree.Element('keyword')
            tag.text = re.sub('.*, (Admin.*) \(.*', r'\1', title)
            metaDoc.findall('.//' + tagType)[0].append(tag)
        tag = ElementTree.Element('keyword')
        tag.text = re.sub('.*\(1:(.*)\)', r'\1', title)
        metaDoc.findall('.//' + tagType)[0].append(tag)

    # Write out metadata
    metaDoc.write(metaFile, encoding='UTF-8')
    del metaDoc

# Cleanup log files
for logfile in [x for x in os.listdir(basepath) if x[-4:] == '.log']:
    os.remove(os.path.join(basepath, logfile))
del df
del mxd
