import groupBy as gb
import shutil
import sys
import json
from os import system

def init():

    #Descarga de la información
    system("yarn startDownload")

    #Obtención del nombre del sistema
    sistema = str(sys.argv[1])

    #Mensaje de inicio
    print("Procesando: "+sistema)

    #Checamos si podemos empezar a procesar la información
    if gb.init(sistema):
        zip = shutil.make_archive(sistema,"zip",sistema)
        print(sistema+" procesado correctamente")
        print("Se genero el archivo: "+sistema+".zip")
    else:
        print("Fallo el procesado del "+sistema)

#s1, s2, s3s, s3p
init()

