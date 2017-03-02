#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name:
qgis2geowe.py
Autor:
Patricio Soriano :: SIGdeletras.com
Description:
Script Python para generar un proyecto GeoWE desde QGIS.
"""

import os
import zipfile
import json
import time
import shutil
from qgis.gui import QgsMessageBar
from PyQt4.QtGui import QMessageBox


def rgb_to_hex(rgb):
    return '#' + '%02x%02x%02x' % rgb


# Variables con metadatos para el proyecto GeoWE

geoweprojVersion = '1.0.0'
geoweprojTile = 'Proyecto GeoWE2QGIS'
geoweprojDescription = 'Ejemplo de proyecto GeoWE generado desde QGIS'
geoweprojDate = (time.strftime("%d/%m/%Y"))

# Variable con directorio para salvar el proyecto

prjurl = '/home/user/folder'
#prjurl = 'C:/folder'

# Nombre del proyecto GeoWE
geoweprojName = 'geowe-project-qgis'

selected_layers = iface.layerTreeView().selectedLayers()

# Comprueba si hay capas seleccionadas

if selected_layers:
    # GeneraciÃ³n de zip de proyecto

    zf = zipfile.ZipFile(prjurl + geoweprojName, "w")

    # Creación de proyecto
    fo = open(prjurl + "geowe-project.prj", "w")

    # Metadatos de proyecto
    fo.write('{"version": "' + geoweprojVersion + '", "title": "'
             + geoweprojTile + '", "description": "' + geoweprojDescription
             + '", "date": "' + geoweprojDate + '", "vectors": [')

    # Crea variable para SRC 4326. Obligatorio para proyectos GeoWE

    crs4326 = QgsCoordinateReferenceSystem(4326,
                                           QgsCoordinateReferenceSystem.EpsgCrsId)

    # Crear carpeta para geojson
    geojsonfolder = (prjurl + "geojson")
    os.mkdir(geojsonfolder, 0755)

    # Convierte las capas cargadas en QGIS a GeoJSON y las aÃ±ade al proyecto
    for l in selected_layers:
        # crea e geojson
        qgis.core.QgsVectorFileWriter.writeAsVectorFormat(l,
                                                          geojsonfolder + '/' + l.name() + '.geojson', 'utf-8',
                                                          crs4326, 'GeoJson')

        data = json.loads(open(geojsonfolder + '/' +
                               l.name() + '.geojson').read())

        jsonString = json.dumps(data)

        double_encode = json.dumps(jsonString)

        fo.write('{"name": "' + l.name() + '", "content": ')

        fo.write(double_encode)

        props = l.rendererV2().symbol().symbolLayer(0).properties()

        if l.wkbType() == QGis.WKBLineString:

            # obtener propiedades cuando la capa es lin 
            # print 'Layer is a lin layer'

            colorlist = eval((props['line_color']))

            hexColor = rgb_to_hex((colorlist[0], colorlist[1], colorlist[2]))

            fo.write(
                ", \"style\": {\"fillColor\": \"" + hexColor + '", "fillOpacity": 0.70, "strokeColor": "' + hexColor +
                '", "strokeWidth": 3 } } ,')
        else:
            colorlist = eval((props['color']))
            outlineColorlist = eval((props['outline_color']))

            hexColor = rgb_to_hex((colorlist[0], colorlist[1], colorlist[2]))

            hexOutlineColor = rgb_to_hex((outlineColorlist[0],
                                          outlineColorlist[1], outlineColorlist[2]))

            fo.write(
                ', "style": {"fillColor": "' + hexColor + '", "fillOpacity": 0.70, "strokeColor": "'
                + hexOutlineColor + '",  "strokeWidth": 3 } } ,')

    fo.write('] }')
    fo.close()
    projfile = prjurl + "geowe-project.prj"
    zf.write(projfile,os.path.basename(projfile))
    os.remove(prjurl + "geowe-project.prj")
    zf.close()

    shutil.rmtree(geojsonfolder)

    QMessageBox.information(iface.mainWindow(), "QGIS2GeoWE", 'El proyecto\
    \'%s.zip\' con %s capas se generado correctamente en la carpeta %s\
    ' % (geoweprojName, len(selected_layers), prjurl))


else:

    iface.messageBar().pushMessage("Error", "Please select one or more layers!", QgsMessageBar.CRITICAL, 6)
