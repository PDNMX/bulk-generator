# API - Bulk-generator

## Notas importantes
Para utilizar este software debe de asegurarse de tener instalado las siguientes herramientas con la versión indicada o superior.

- Python 3.10.5
- Node v16.16.0
- Yarn 1.22.19

Así mismo debe de contar con las bibliotecas necesarias de Python especificadas en el archivo denominado **requirements.txt**. 
Es importante recalcar que esta API cuenta con un sistema de actualización lo que ocasionará que durante los **domingos de 7:00 am a 8:00 am** cualquier petición que se le haga al sistema **será rechazada**. Pasando este periodo el sistema volverá a funcionar con normalidad.



## Instalar dependencias
`yarn install`

## Ejecutar
Para iniciar el programa se debe de ejecutar alguno de los siguientes comandos dentro de la carpeta API dependiendo el OS en el que se encuentre.

### Windows
`python main.py`
### Linux
`python3 main.py`

## Rutas y parámetros
- /download: Con ella se podría obtener un zip denominado “all.zip” en el cual se encontraran los .json de todos los sistemas así como sus reportes de conexión y sus reportes de conteo.

- /download?sistema=s: El parámetro “sistema” nos ayuda a definir específicamente el sistema del cual queramos obtener sus .json y sus reportes de conteo y de conexión. “s” debe de ser sustituido por cualquiera de las siguientes opciones según se requiera:
  - s1
  - s2
  - s3s
  - s3p

- /download?sistema=s&elemento=e: El parámetro “elemento” será el encargado de definir específicamente el archivo que necesitemos del sistema indicado ya sea únicamente los .json, el reporte de conexión o el reporte de conteo. “e” debe de ser sustituido por cualquiera de las siguientes opciones según se requiera:
  - conteo
  - reporte
  - zip

- /instituciones?sistema=s: Con ella podrás acceder al endpoint del sistema que se especifique. “s” debe de ser sustituido por cualquiera de las siguientes opciones según se requiera:
  - s2
  - s3s
  - s3p
