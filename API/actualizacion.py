from datetime import datetime
import shutil
import groupBy as gb
import os
import generaReporte as gr
from os import remove

#Definición de día y horas de actualización
day = 4
limiteInferior = datetime.strptime("13:21:00","%X").time()
limiteSuperior = datetime.strptime("13:40:00","%X").time()
actualizar = True

#Función encargada de actualizar los archivos y los reportes
def run():

    #Creamos las carpetas
    carpetas = ["./descargas","./descargas/data","./descargas/data/s1","./descargas/data/s2","./descargas/data/s3p","./descargas/data/s3s"]
    for carpeta in carpetas:
        if (not os.path.exists(carpeta)):
            os.mkdir(carpeta)

    #Obtenemos la fecha actual
    fecha = datetime.now()
    fechaFormato = fecha.strftime('%d_%m_%Y')

    #Sistemas con los cuales se trabaja
    #sistemas = ["s1","s2","s3s","s3p"]
    sistemas = ["s3s","s3p"]

    #Guardamos la fecha de creación de archivos
    with open("ultimaActualizacion.txt",'w') as file:
        file.write(fechaFormato)

    #Descargamos la información para cada sistema
    for sistema in sistemas:

        #Descarga de la información
        comando = "yarn startDownload " + sistema
        os.system(comando)

        #Iniciamos el proceso de conteo
        gb.init(sistema,gb.readName("../data",0))

        #Creamos el archivo comprimido de los .json
        zip = shutil.make_archive("./descargas/data/"+sistema+"/"+sistema,"zip","../data")

        #limpiamos lo descargado
        os.system("yarn cleanDownload")

        #Creamos el readme
        with open("./descargas/data/"+sistema+"/readme.txt",'w') as file:
            file.write("Datos PDN "+fecha.strftime("%d/%m/%Y")+"\n")
            file.write("*conteo_registros: Archivo encargado de indicar el número de instituciones por cada sistema.\n")
            file.write("*reporte_de_conexiones: Indica si una entidad esta disponible o no, en caso de que no lo este dentro del archivo de conteo no se verá reflejada.\n")
            file.write("*Zip: Dentro del comprimido estarán los archivos JSON de cada entidad separados por carpetas.\n")
        
        #Creamos los zip con todos los elementos de cada sistema
        zip = shutil.make_archive("./descargas/datos_PDN_"+sistema+"_"+fechaFormato,"zip","./descargas/data/"+sistema+"/")

    #Creamos el zip de todos los sistemas
    zip = shutil.make_archive("./descargas/datos_PDN_all_"+fechaFormato,"zip","./descargas/data")

    #Actualiza reportes de instituciones
    for sistema in sistemas[1:]:
        gr.validacion(sistema)

if __name__ == '__main__':
    while(True):
        if (datetime.today().weekday() == day and datetime.now().time() >= limiteInferior and datetime.now().time() < limiteSuperior):
            if actualizar:
                print("Comence la actualizacion")
                #Creamos el archivo de control
                open("actualizando", "w").close()
                
                #Eliminamos la carpeta con los antiguos datos
                #shutil.rmtree("descargas")

                #Eliminamos el registro de la ultimaActualziacion
                #remove("ultimaActualizacion.txt")

                #Actualizamos
                #run()

                actualizar = False
        else:
            if not actualizar:
                actualizar = True
                #Removemos el archivo de control
                remove("actualizando")
                print("Termine la actualizacion")
