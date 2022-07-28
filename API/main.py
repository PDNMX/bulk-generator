from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import shutil

#Creamos la API
app = FastAPI()


#Método para retornar todos los archivos
@app.get("/download")
def download(sistema = None,elemento = None):

    if sistema is not None:
        if elemento is None:
            path = "./descargas/all_"+sistema+".zip"
            len = 12
        elif elemento == "csv":
            path = "./descargas/data/conteo_registros_"+sistema+".csv"
            len = 17
        elif elemento == "zip":
            path = "./descargas/data/"+sistema+".zip"
            len = 17
    else:
        #Definimos la ruta
        path = "./descargas/all.zip"
        len = 12

    #Retornamos la información
    return FileResponse(path=path,filename=path[len:])
        







#Encender el servidor
if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1', port=8000)
