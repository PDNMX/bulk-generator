from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Response
import os
import uvicorn
from actualizacion import run

#Creamos la API
app = FastAPI()

#Método para retornar los archivos de los sistemas
@app.get("/download")
def download(sistema = None,elemento = None):
    #Verificamos si toca actualizar los datos
    if(os.path.exists("actualizando")):

        return {"Generando datos"}
        
    else:
        #Leemos la ultima actualización
        with open("ultimaActualizacion.txt",'r') as file:
            fechaFormato = file.read()

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

@app.get("/instituciones")
def download(sistema = None):
    if(os.path.exists("actualizando")):
        return {"Generando datos"}
    else:
        sistemas = ["s2","s3s","s3p"]
        if(sistema in sistemas):
            with open("./descargas/reporte_"+sistema+".json",'r') as file:
                r = file.read()
            return Response(content=r, media_type="application/json")


if __name__ == '__main__':

    if (not os.path.exists("ultimaActualizacion.txt")):        
        #Descargamos los archivos
        run("descargas")     

    #Encender el servidor
    uvicorn.run(app,host='0.0.0.0', port=9000)

