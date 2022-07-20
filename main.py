import groupBy as gb
import shutil
import sys
from os import system

def init():
    
    #Obtención del nombre del sistema
    sistema = str(sys.argv[1])

    #Verificamos que sea un sistema valido
    if (sistema == "s1" or sistema == "s2" or sistema == "s3s" or sistema == "s3p"):
        
        #Descarga de la información
        comando = "yarn startDownload " + sistema
        system(comando)

        #Mensaje de inicio
        print("\nProcesando: "+sistema)

        #Iniciamos el proceso de conteo
        gb.merge(sistema,gb.readName("data",0))

        #Creamos el archivo comprimido
        zip = shutil.make_archive(sistema,"zip","data")
        print(sistema+" procesado correctamente")
        print("Se generaron los archivos "+sistema+".zip y conteo_registros_"+sistema+".csv\n")

        #limpiamos lo descargado
        system("yarn cleanDownload")

    else:
        #Mensaje de fallo
        print("Fallo el procesado del "+sistema)

init()

