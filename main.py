import groupBy as gb
import shutil
import sys
from os import system

def init():
    
    #Obtención del nombre del sistema
    sistema = str(sys.argv[1])

    #Descarga de la información
    comando = "yarn startDownload " + sistema
    system(comando)

    #Mensaje de inicio
    print("\nProcesando: "+sistema)

    #Checamos si podemos empezar a procesar la información
    if gb.init(sistema):
        #Creamos el archivo comprimido
        zip = shutil.make_archive(sistema,"zip","data")
        print(sistema+" procesado correctamente")
        print("Se genero el archivo: "+sistema+".zip\n")

        #limpiamos lo descargado
        system("yarn cleanDownload")

    else:
        print("Fallo el procesado del "+sistema)

init()

