# qgis2geowe
Script Python para generar un proyecto GeoWE desde QGIS

![qgis2geowe](img/qgis2geowe.png)

##Descripción
Desde la versión 1.4.8 Beta la plataforma de edición de datos en WEB [GeoWE](geowe.org), permite crear un archivo de proyecto con las capas utilizadas. 
Este script ejecutado desde la consola de Python de QGIS crea un archivo de GeoWE a partir de las capas seleccionadas.

La especificaciones del fichero de proyecto GeoWE pueden consultarse en este [enlace](http://www.geowe.org/guide/proyectos/index.html)

##Uso
- Clonar/descargar el repositorio.
- Abrir QGIS y cargar capas.
- En QGIS cargar el archivo qgis2geowe.py en la consola de Python de QGIS.
- Configurar los metadatos del proyecto.
- Asignar un nombre al proyecto.
- Definir la dirección de creación del proyecto.
- Ejecutar

*Nota: El proyecto se creará en el directorio definido.*

##2do
- Usar el mismo directorio del archivo py para crear el proyecto
- Plugin de QGIS
- Crear un script inverso: de GeoWE a QGIS
