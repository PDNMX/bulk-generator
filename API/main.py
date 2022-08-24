"""
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import uvicorn
import groupBy as gb
import shutil

#Definición de día y horas de actualización
day = 6
limiteInferior = datetime.strptime("8:00:00","%X").time()
limiteSuperior = datetime.strptime("9:00:00","%X").time()
actualizar = True

#Función encargada de actualizar los archivos
def update():

    sistemas = ["s1","s2","s3s","s3p"]
    
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
        
        #Creamos los zip con todos los elementos de cada sistema
        zip = shutil.make_archive("./descargas/all_"+sistema,"zip","./descargas/data/"+sistema+"/")

    #Creamos el zip de todos los sistemas
    zip = shutil.make_archive("./descargas/all","zip","./descargas/data")



#Creamos la API
app = FastAPI()

#Método para retornar los archivos de los sistemas
@app.get("/download")
def download(sistema = None,elemento = None):
    global actualizar

    #Verificamos si toca actualizar los datos
    if(datetime.today().weekday() == day and datetime.now().time() >= limiteInferior and datetime.now().time() < limiteSuperior):

        if actualizar:
            actualizar = False
            update()
            
        return {"Pagina en mantenimiento"}
        
    else:
        #Actualizamos el valor de la bandera
        actualizar = True

        #Verificamos el sistema
        if sistema is not None:
            if elemento is None:
                #Descarga csv y zip del sistema dado
                path = "./descargas/all_"+sistema+".zip"
                tam = 12
            elif elemento == "conteo":
                #Descarga unicamente el csv
                path = "./descargas/data/"+sistema+"/conteo_registros_"+sistema+".csv"
                tam = 18 +len(sistema)
            elif elemento == "reporte":
                #Descarga unicamente el csv
                path = "./descargas/data/"+sistema+"/reporte_de_conexiones_"+sistema+".csv"
                tam = 18 + len(sistema)
            elif elemento == "zip":
                #Descarga unicamente el zip
                path = "./descargas/data/"+sistema+"/"+sistema+".zip"
                tam = 18 + len(sistema)
        else:
            #Descargamos todos los archivos
            path = "./descargas/all.zip"
            tam = 12

        #Retornamos la información
        return FileResponse(path=path,filename=path[tam:])
    
"""
import groupBy as gb

if __name__ == '__main__':
    """
    #Verificamos si tenemos los archivos
    if (not os.path.exists("./descargas/all.zip")):
        #Creamos las carpetas
        carpetas = ["./descargas","./descargas/data","./descargas/data/s1","./descargas/data/s2","./descargas/data/s3p","./descargas/data/s3s"]
        for carpeta in carpetas:
            if (not os.path.exists(carpeta)):
                os.mkdir(carpeta)
        
        #Descargamos los archivos
        update()

    #Encender el servidor
    uvicorn.run(app,host='127.0.0.1', port=8000)
    """

    gb.init("s1",gb.readName("../data",0))
