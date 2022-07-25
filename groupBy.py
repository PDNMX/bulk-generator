import pandas as pd
from pathlib import Path
import json
import os

#Función encargada de obtener los nombres de directorios y ficheros
def readName(s,mode):

    #Lista de nombres
    names = []

    #Checamos si buscamos directorios o ficheros
    with os.scandir(s) as files:
        for f in files:
            #Si son carpetas
            if mode == 0 and f.is_dir():
                names.append(f.name)
            #Si son archivos .json
            elif mode == 1 and f.name.endswith('.json'):
                names.append(f.name)

    #Retornamos los nombres
    return names


#Funciones para realizar el conteo
def csv(sistema,directorio,names):

    #Lista que contendra los dataframes
    dataframes = []

    #Iteramos los archivos del directorio
    for name in names:

        #Ruta del .json
        p = Path('data/'+directorio+'/'+name)

        #Leemos el json
        with p.open('r', encoding='utf-8') as f:
            s = f.read()
            
            #Cargamos el .json
            data = json.loads(s, strict=False)

            #Creamos el dataframe y lo agregamos a la lista
            dataframes.append(pd.json_normalize(data))        
    
    #Creamos el contenedor de todos los dataframes
    df = pd.DataFrame()

    #Unimos los dataframes en el contenedor
    for d in dataframes:
        df = pd.concat([df,d])


    #Verificamos que haya datos
    if True:#(len(data) != 0):

        #Creamos el dataframe
        #df = pd.json_normalize(data)

        if(sistema == "s1"):
            #Realizamos el conteo
            df_grouped = df.groupby(["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"])["id"].count().reset_index(name="count")

            #Renombramos columna
            df_grouped.rename(columns={'declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico':'nombreEntePublico'},inplace=True)
            
        elif (sistema == "s2" or sistema == "s3s" or sistema == "s3p"):
            #Realizamos el conteo
            df_grouped = df.groupby(["institucionDependencia.nombre"])["id"].count().reset_index(name="count")

            #Renombramos columna
            df_grouped.rename(columns={'institucionDependencia.nombre':'institucionDependencia'},inplace=True)

        #Agregamos entidadPublica
        df_grouped.insert(0,"entidadPublica",directorio)

    else:
        #Creamos el dataframe
        df_grouped = pd.DataFrame()

        #Asignamos valores de vacío
        df_grouped['entidadPublica'] = [name[:len(name)-5]]
        df_grouped['institucionDependencia'] = ['N/A']
        df_grouped['count'] = [0]

    #Retornamos el datframe
    return df_grouped


#Función encargada de juntar los archivos en uno
def merge(s,directorios):

    #Lista que guarda los dataFrames
    list = []

    #Bandera de ayuda para encabezados
    flag = True

    #Creamos archivo que contendra todo
    with open("conteo_registros_"+s+'.csv', 'w') as file:

        #Iteramos los directorios
        for directorio in directorios:

            #Obtenemos el nombre de los .json del directorio
            names = readName(Path('data/'+directorio),1)

            if(len(names) != 0):
                csv(s,directorio,names).to_csv(file, header=flag, index=False)
            else:
                #Creamos el dataframe
                df_tmp = pd.DataFrame()

                #Asignamos valores de vacío
                df_tmp['entidadPublica'] = [directorio]
                df_tmp['institucionDependencia'] = ['N/A']
                df_tmp['count'] = [0]

                df_tmp.to_csv(file, header=flag, index=False)
            
            flag = False

"""
            #Iteramos cada archivo .json del directorio y lo unimos
            for name in names:
                if not flag:
                    #Agregamos el resto de dataframes sin encabezados
                    csv(s,directorio,name).to_csv(file, header=False, index=False)
                else:
                    #Agremos el primer dataframe junto con sus encabezados
                    csv(s,directorio,name).to_csv(file, header=True, index=False)
                    flag = False
"""