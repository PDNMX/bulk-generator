from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse
from os import system
import uvicorn
import groupBy as gb
import shutil

#Bandera que indicara si ya se hizo la actualización
flag = False

#Función encargada de actualizar los archivos
def update():
    global flag
    
    #Verificamos si requerimos actualizar los datos
    if (datetime.today().weekday() == 4 and not flag):
        #sistemas = ["s2","s3s","s3p"]
        sistemas = ["s3s"]
        #Descargamos la información para cada sistema
        for sistema in sistemas:

            #Descarga de la información
            comando = "yarn startDownload " + sistema
            system(comando)

            #Iniciamos el proceso de conteo
            gb.merge(sistema,gb.readName("../data",0))

            #Creamos el archivo comprimido de los .json
            zip = shutil.make_archive("./descargas/data/"+sistema+"/"+sistema,"zip","../data")

            #limpiamos lo descargado
            system("yarn cleanDownload")
        
            #Creamos los zip con todos los elementos de cada sistema
            zip = shutil.make_archive("./descargas/all_"+sistema,"zip","./descargas/data/"+sistema+"/")

        #Creamos el zip de todos los sistemas
        zip = shutil.make_archive("./descargas/all","zip","./descargas/data")

        #Indicamos que ya se actualizo la información
        flag = True
        
    elif (datetime.today().weekday() != 4):
        #Indicamos que no se ha actualizado la información
        flag = False


#Creamos la API
app = FastAPI()

#Método para retornar los archivos de los sistemas
@app.get("/download")
def download(sistema = None,elemento = None):

    #Verificamos si toca actualizar los datos
    update()

    #Verificamos el sistema
    if sistema is not None:
        if elemento is None:
            #Descarga csv y zip del sistema dado
            path = "./descargas/all_"+sistema+".zip"
            len = 12
        elif elemento == "csv":
            #Descarga unicamente el csv
            path = "./descargas/data/"+sistema+"/conteo_registros_"+sistema+".csv"
            len = 17
        elif elemento == "zip":
            #Descarga unicamente el zip
            path = "./descargas/data/"+sistema+"/"+sistema+".zip"
            len = 17
    else:
        #Descargamos todos los archivos
        path = "./descargas/all.zip"
        len = 12

    #Retornamos la información
    return FileResponse(path=path,filename=path[len:])
        

#Encender el servidor
if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1', port=8000)
