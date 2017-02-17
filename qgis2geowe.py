#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nombre:
qgis2geowe.py
Autor:
Patricio Soriano :: SIGdeletras.com
Descripción:
Script Python para generar un proyecto GeoWE desde QGIS.
"""

import os
import zipfile
import json
import time

def rgb_to_hex(rgb):
    return '#'+'%02x%02x%02x' % rgb

# Variables con metadatos para el proyecto GeoWE

geoweprojVersion = '1.0.0'
geoweprojTile = 'Proyecto GeoWE2QGIS'
geoweprojDescription = 'Ejemplo de proyecto GeoWE generado desde QGIS'
geoweprojDate = (time.strftime("%d/%m/%Y"))

# Variable con directorio para salvar el proyecto

prjurl = '/home/user/Documentos/carpeta'
#prjurl = 'C:/carpeta'

# Nombre del proyecto GeoWE
geoweprojName = 'geowe-project-prueba'

# Generación de zip de proyecto

zf = zipfile.ZipFile(prjurl+geoweprojName, "w")

# Creación de proyecto
fo = open(prjurl+ geoweprojName+".prj", "w")

# Metadatos de proyecto
fo.write('{"version": "'+geoweprojVersion+'", "title": "'+geoweprojTile+'", "description": "'+geoweprojDescription+'", "date": "'+geoweprojDate+'", "vectors": [')

## Crea variable para SRC 4326. Obligatorio para proyectos GeoWE

crs4326 = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)

## Convierte las capas cargadas en QGIS a GeoJSON y las añade al proyecto
for l in QgsMapLayerRegistry.instance().mapLayers().values():
    # crea e geojson
    print l.name()
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(l,prjurl+l.name()+'.geojson', 'utf-8', crs4326, 'GeoJson')
    
    data = json.loads(open(prjurl+l.name()+'.geojson').read())
    
    jsonString = json.dumps(data)
    
    double_encode = json.dumps(jsonString)
    fo.write('{"name": "'+l.name()+'", "content": ')
    fo.write(double_encode)
    
    props = l.rendererV2().symbol().symbolLayer(0).properties()
    if l.wkbType()==QGis.WKBLineString:
        #obtener propiedades cuando la capa es lin 
        #print 'Layer is a lin layer'
        
        colorlist = eval((props['line_color']))
               
        hexColor = rgb_to_hex((colorlist[0],colorlist[1],colorlist[2]))
        
        fo.write(', "style": {"fillColor": "'+hexColor+'", "fillOpacity": 0.70, "strokeColor": "'+hexColor+'", "strokeWidth": 3 } } ,')
    else:
        colorlist = eval((props['color']))
        outlineColorlist = eval((props['outline_color']))
        
        hexColor = rgb_to_hex((colorlist[0],colorlist[1],colorlist[2]))
        hexOutlineColor = rgb_to_hex((outlineColorlist[0],outlineColorlist[1],outlineColorlist[2]))
        
        fo.write(', "style": {"fillColor": "'+hexColor+'", "fillOpacity": 0.70, "strokeColor": "'+hexOutlineColor+'", "strokeWidth": 3 } } ,')
    #    os.remove(prjurl+l.name()+'.geojson')
	

fo.write('] }')
fo.close()

zf.write(prjurl+geoweprojName+".prj")
os.remove(prjurl+geoweprojName+".prj")
zf.close()
