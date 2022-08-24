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


#Función encargada de unir los CSV
def merge(sistema,directorio,names):
    #Lista que contendra los dataframes
    dataframes = []

    #Lista que contendra los dataframes ya procesados
    listDataFramesGrouped = []

    #Limite de archivos a leer
    limite = 10000
    print("Empiezo a leer")
    #Iteramos todos los archivos y los vamos procesando poco a poco
    for i in range(0,len(names)):
        if (i<limite):
            #Ruta del .json
            p = Path('../data/'+directorio+'/'+names[i])

            #Leemos el json
            with p.open('r', encoding='utf-8') as f:
                s = f.read()
                
                #Cargamos el .json
                data = json.loads(s, strict=False)

                #Creamos el dataframe y lo agregamos a la lista
                dataframes.append(pd.json_normalize(data))    
        else:
            print("Procesando dataframes de if")
            #Retrocedemos una iteración
            i-=1

            #actualizamos limite
            limite +=10000

            #Creamos el contenedor de todos los dataframes hasta el momento
            df = pd.concat(dataframes)

            #Unimos los dataframes y lso agregamos a la lista
            listDataFramesGrouped.append(csv(sistema,directorio,df))

            #Limpiamos la lista
            dataframes.clear()

    #Procesamos los archivos restantes
    print("Procesando dataframes restantes")
    #Creamos el contenedor de todos los dataframes hasta el momento
    df = pd.concat(dataframes)

    #Unimos los dataframes y lso agregamos a la lista
    listDataFramesGrouped.append(csv(sistema,directorio,df))

    #contenedor final
    df_grouped = pd.DataFrame(listDataFramesGrouped[0])

    columna = ""

    #Definimos la columna
    if (sistema == "s1"):
        columna = "nombreEntePublico"
    elif (sistema == "s2" or sistema == "s3s" or sistema == "s3p"):
        columna = "institucionDependencia"
    print("Comienzo a sumar")
    #Iteramos los grupos
    for i in range(1,len(listDataFramesGrouped)):
        df_i = listDataFramesGrouped[i]

        #Iteramos los nombres
        for j in df_i.index:
            nombre = df_i[columna][j]

            #Si hay coincidencia se suman las cuentas
            if(df_grouped.isin([nombre]).any().any()):
                #Si hay coincidencia se suman las cuentas
                k = df_grouped.index[df_grouped[columna] == nombre].tolist()
                df_grouped["count"][k] = int(df_grouped["count"][k]+df_i["count"][j])
            else:
                #En caso contrario se agrega
                df_grouped = df_grouped.append({'entidadPublica':df_i['entidadPublica'][j],columna:df_i[columna][j],'count':df_i['count'][j]},ignore_index=True)

    print("Retornando dataframe final")
    return df_grouped



#Función encargada de generar los csv
def csv(sistema,directorio,df):

    if(sistema == "s1"):

        #Damos formato Camel al nombre de la institución
        df["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"] = df["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"].str.title()

        #Eliminamos espacios en blanco de más
        df["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"] = df["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"].str.strip()

        #Quitamos las comillas
        df["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"] = df["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"].str.replace("\"","")
        
        #Realizamos el conteo
        df_grouped = df.groupby(["declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico"])["id"].count().reset_index(name="count")

        #Renombramos columna
        df_grouped.rename(columns={'declaracion.situacionPatrimonial.datosEmpleoCargoComision.nombreEntePublico':'nombreEntePublico'},inplace=True)
            
    elif (sistema == "s2" or sistema == "s3s" or sistema == "s3p"):

        #Damos formato Camel al nombre de la institución
        df["institucionDependencia.nombre"] = df["institucionDependencia.nombre"].str.title()

        #Eliminamos espacios en blanco de más
        df["institucionDependencia.nombre"] = df["institucionDependencia.nombre"].str.strip()

        #Quitamos comillas
        df["institucionDependencia.nombre"] = df["institucionDependencia.nombre"].str.replace("\"","")

        #Realizamos el conteo
        df_grouped = df.groupby(["institucionDependencia.nombre"])["id"].count().reset_index(name="count")

        #Renombramos columna
        df_grouped.rename(columns={'institucionDependencia.nombre':'institucionDependencia'},inplace=True)

    #Agregamos entidadPublica
    df_grouped.insert(0,"entidadPublica",directorio)

    #Retornamos el datframe
    return df_grouped


#Función encargada de juntar los archivos en uno
def init(s,directorios):

    #Lista que guarda los dataFrames
    list = []

    #Lista que guarda las entidades que no tienen datos
    entidadVacia = []

    #Bandera de ayuda para encabezados
    flag = True

    #Creamos archivo que contendra todo
    with open("descargas/data/"+s+"/conteo_registros_"+s+'.csv', 'w') as file:

        #Iteramos los directorios
        for directorio in directorios:

            #Obtenemos el nombre de los .json del directorio
            names = readName(Path('../data/'+directorio),1)

            if(len(names) != 0):
                #csv(s,directorio,names).to_csv(file, header=flag, index=False)
                #Aqui se hace el cambio
                print("Llamada a merge")
                merge(s,directorio,names).to_csv(file, header=flag, index=False)
                print("Fin de merge")
                #pass
            else:
                
                #Agregamos el nombre a la lista de entidades vacias
                entidadVacia.append(directorio)

                #Creamos el dataframe temporal
                df_tmp = pd.DataFrame()

                #Asignamos valores de vacío
                df_tmp['entidadPublica'] = [directorio]
                df_tmp['institucionDependencia'] = ['N/A']
                df_tmp['count'] = [0]

                df_tmp.to_csv(file, header=flag, index=False)
            
            flag = False

    #Creamos el reporte de entidades vacias
    df = pd.DataFrame()
    estatusDeConexion = []

    #Definimos el estado de la conexión
    for directorio in directorios:
        if (directorio in entidadVacia):
            estatusDeConexion.append("No disponible")
        else:
            estatusDeConexion.append("Disponible")

    #agregamos los datos al dataframe
    df['Entidad'] = directorios
    df['Estatus de conexión'] = estatusDeConexion

    #Creamos el documento
    with open("descargas/data/"+s+"/reporte_de_conexiones_"+s+'.csv','w') as file:
        df.to_csv(file,header=True,index=False)
