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
    fecha = datetime.now()
    fechaFormato = fecha.strftime('%d_%m_%Y')
    sistemas = ["s1","s2","s3s","s3p"]

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



#Creamos la API
app = FastAPI()

#Método para retornar los archivos de los sistemas
@app.get("/download")
def download(sistema = None,elemento = None):
    global actualizar

    #Leemos la ultima actualización
    with open("ultimaActualizacion.txt",'r') as file:
        fechaFormato = file.read()

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
                path = "./descargas/datos_PDN_"+sistema+"_"+fechaFormato+".zip"
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
            path = "./descargas/datos_PDN_all_"+fechaFormato+".zip"
            tam = 12

        #Retornamos la información
        return FileResponse(path=path,filename=path[tam:])

if __name__ == '__main__':

    #Leemos la ultima actualización
    with open("ultimaActualizacion.txt",'r') as file:
        fechaFormato = file.read()

    #Verificamos si tenemos los archivos
    if (not os.path.exists("./descargas/datos_PDN_all_"+fechaFormato+".zip")):
        #Creamos las carpetas
        carpetas = ["./descargas","./descargas/data","./descargas/data/s1","./descargas/data/s2","./descargas/data/s3p","./descargas/data/s3s"]
        for carpeta in carpetas:
            if (not os.path.exists(carpeta)):
                os.mkdir(carpeta)
        
        #Descargamos los archivos
        update()

    #Encender el servidor
    uvicorn.run(app,host='0.0.0.0', port=9000)
