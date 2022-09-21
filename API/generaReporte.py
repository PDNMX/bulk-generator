import requests
import pandas as pd
import json
import sys

def validacion(sistema):
    #Diccionario
    archivo = []

    #Cadenas para formar las url
    base = "https://api.plataformadigitalnacional.org/"
    entities = "/api/v1/entities"
    summary = "/api/v1/summary"

    #Headers
    headers = {
    'Content-Type': 'application/json'
    
    }

    #Armamos la url de las entidades
    url = base + sistema + entities

    #Realizamos la petición
    resp = requests.post(url)

    #Validamos que la petición se haya hecho correctamente
    if (resp.status_code == 200):

        #Convertimos en un Dataframe
        df = pd.json_normalize(json.loads(resp.text, strict=False))

        #Cambiamos de url
        url = base + sistema + summary

        #Iteramos los nombres de las instituciones
        for i in df.index:

            #Obtenemos el número de elementos de archivo
            tam = len(archivo)

            #Mensaje para ver en cual estamos
            print("Vamos en "+str(i)+" de "+str(df.index))

            #Armamos la data
            payload = json.dumps({
            "query": {
                "institucionDependencia": df["nombre"][i]
            },
            "institucion": df["nombre"][i]
            })

            #Realizamos la petición
            resp = requests.request("POST", url, headers=headers, data=payload)

            #Verificamos que las peticiones se hagan correctamente
            if (resp.status_code == 200):

                #Convertimos en un Dataframe
                dfInterno = pd.json_normalize(json.loads(resp.text, strict=False))

                #Iteramos nuestro df interno
                for j in dfInterno.index:
                    #Checamos si tiene al menos un elemento
                    if(dfInterno["totalRows"][j] > 0):
                        if sistema == "s2":
                            archivo.append({'nombre':str(df["nombre"][i]).strip(),'siglas':str(df["siglas"][i]).strip(),'clave':str(df["clave"][i]).strip(),'supplier_id':str(df["supplier_id"][i]).strip(),'status':True})
                        else:
                            archivo.append({'nombre':str(df["nombre"][i]).strip(),'status':True})
                        break
                
                #Si no se agrego un elemento significa que no hay información
                if(len(archivo) == tam):
                    if(sistema == "s2"):
                        archivo.append({'nombre':str(df["nombre"][i]).strip(),'siglas':str(df["siglas"][i]).strip(),'clave':str(df["clave"][i]).strip(),'supplier_id':str(df["supplier_id"][i]).strip(),'status':False})
                    else:
                        archivo.append({'nombre':str(df["nombre"][i]).strip(),'status':False})

            elif (resp.status_code >= 400):
                print("Ocurrio el error " +str(resp.status_code)+" con: "+df["nombre"][i])

        #Creamos el archivo json
        with open('./descargas/reporte_'+sistema+'.json','w') as file:
            json.dump(archivo,file,indent=4)

    elif (resp.status_code >= 400):
        #Notificacmos el error
        print("Ocurrio un error con las entidades del sistema: "+sistema)