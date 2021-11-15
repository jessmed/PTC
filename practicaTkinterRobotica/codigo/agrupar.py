# -*- coding: utf-8 -*-

import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors # Lista de colores de matplotlib
import json
import os
import glob
import math

# Parámetros fijados empíricamente
min_puntos_cluster_ =3  
max_puntos_cluster_ =50 
umbral_distancia_ = 0.04 

distancias = ['Cerca', 'Medio', 'Lejos']

def leer_datos_json(nom_fichero):
    """
    Lee un archivo JSON correspondiente a los datos del simulador y
    devuelve los puntos como una lista de diccionarios.
    """
    
    objetos = []
    
    # Leo el fichero JSON
    with open(nom_fichero, 'r') as f:
        for line in f:
            objetos.append(json.loads(line))
                
            
    # Devuelvo los puntos como una lista de la forma siguiente:
    # puntos[i] -> puntos de la iteración i
    # puntos[i][0] -> coordenadas X de los puntos de la iteración i
    # puntos[i][1] -> coordenadas Y de los puntos de la iteración i
    puntos = [[obj['PuntosX'], obj['PuntosY']] for obj in objetos[1:-1]]
    
    return puntos

def leer_ejemplos_carpetas(nombre_carpetas):
    """
    Lee los datos de los ficheros JSON en el interior de todas las carpetas
    de nombre_carpetas.
    """
    datos = []
    
    listaDir=sorted(glob.glob(nombre_carpetas)) # Carpetas con los ejemplos
    
    for carpeta in listaDir:
        os.chdir(carpeta) # Cambio el directorio de trabajo a la carpeta
        
        # Obtengo el nombre del archivo json con los datos
        nom_archivo = glob.glob('*.json')[0]
        
        # Leo los datos del archivo
        datos_archivo = leer_datos_json(nom_archivo)
        
        # Los añado a los datos positivos
        datos += datos_archivo
        
        os.chdir('..') # Vuelvo al antiguo directorio de trabajo
    
    return datos

def dist(x1, y1, x2, y2):
    """
    Calcula la distancia euclídea entre los puntos 1 y 2.
    """
    
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def crear_clusters(datos, min_puntos_cluster, max_puntos_cluster,
                   umbral_distancia):
    """
    Devuelve los clusters de puntos usando el algoritmo de agrupación
    por distancia de salto.

    """
    
    clusters = []
    
    # Calculo los clusters para los puntos de cada iteración
    for datos_it in datos:
        # Añado el primer punto al posible cluster
        x_prev, y_prev = datos_it[0][0], datos_it[1][0]
        cluster_actual = [[x_prev, y_prev]]
        
        # Recorro el resto de puntos
        for i in range(1, len(datos_it[0])):
            x, y = datos_it[0][i], datos_it[1][i] # Coordenadas del nuevo punto
            
            # Si se va a superar el número máximo de puntos del clúster,
            # este nuevo punto se añade como primer punto del siguiente cluster
            if len(cluster_actual) == max_puntos_cluster:
                # Añado el cluster actual a los clusters
                clusters.append(cluster_actual)
                
                cluster_actual = [[x, y]]
            else:
                # Si la distancia con el punto anterior no supera a umbral_distancia
                # el nuevo punto se incorpora al cluster actual
                if dist(x, y, x_prev, y_prev) <= umbral_distancia:
                    cluster_actual.append([x, y])
                # Si la supera, se crea un nuevo clúster
                else:
                    # Añado el cluster_actual a los clusters siempre que
                    # el número de puntos sea suficiente
                    if len(cluster_actual) >= min_puntos_cluster:
                        clusters.append(cluster_actual)
                    
                    cluster_actual = [[x, y]]
                    
            x_prev, y_prev = x, y
                
    return clusters

def visualizar_clusters(datos, min_puntos_cluster, max_puntos_cluster,
                                     umbral_distancia):
    """
    Función auxiliar que uso para crear y visualizar los clusters y así
    elegir los mejores valores para el algoritmo de clustering.
    """
    
    print("\nClusters\n")
    
    # Represento por separado los clusters de los puntos de cada iteracion
    for puntos_it in datos:
        # Obtengo los clusters de los puntos de la iteración actual
        clusters_it = crear_clusters(np.expand_dims(puntos_it, axis=0),
                                     min_puntos_cluster, max_puntos_cluster,
                                     umbral_distancia) # Uso expand_dims porque es necesario que el array tenga 3 dimensiones

        # Pinto los puntos de la iteración actual de un color según el cluster
        # al que pertenecen
        if len(clusters_it) > 0:
            for cluster, color in zip(clusters_it, mcolors.BASE_COLORS):
                arr_puntos = np.array(cluster)
                
                plt.scatter(arr_puntos[:,0], arr_puntos[:,1], c=color)
        
            plt.show()

def clusters_to_json(clusters, nom_fich):
    """
    Transforma los clusters de @clusters a formato JSON y los guarda
    en el archivo nom_fich.
    """
    
    # Si el archivo ya existe lanzo una excepción
    if os.path.exists(nom_fich):
        raise FileExistsError('¡Ya existe el archivo!')
    
    # Abro el archivo
    with open(nom_fich, 'w') as f:
        # Cada cluster es una línea del fichero
        for i, cluster in enumerate(clusters):
            num_puntos = len(cluster) # Número de puntos del cluster
            
            puntos = np.array(cluster) # Lo convierto a numpy array para poder separar las coordenadas X e Y
            puntos_X = list(puntos[:,0]) # Los convierto a lista para que puedan ser guardados en el archivo
            puntos_Y = list(puntos[:,1]) # mediante json.dumps
            
            # Creo el diccionario que guarda la información del cluster actual
            dict_cluster = {'numero_cluster':i, 'numero_puntos':num_puntos,
                            'puntosX':puntos_X, 'puntosY':puntos_Y}
            
            # Añado el diccionario al fichero
            f.write(json.dumps(dict_cluster)+'\n')


def main(n1,n2,n3):
    
    global min_puntos_cluster_
    min_puntos_cluster_= int(n1)
    global max_puntos_cluster_
    max_puntos_cluster_= int(n2)
    global umbral_distancia_ 
    umbral_distancia_ = float(n3)
    # <Leo los puntos>
    
    # Ejemplos positivos
    datos_positivos = leer_ejemplos_carpetas('positivo*')

    # Ejemplos negativos
    datos_negativos = leer_ejemplos_carpetas('negativo*')

    # Creación de clústers
    
    # Clusters positivos (de piernas)
    clusters_positivos = crear_clusters(datos_positivos, 
                                        min_puntos_cluster_, 
                                        max_puntos_cluster_,
                                        umbral_distancia_)
    
    # Clusters negativos (de cilindros)
    clusters_negativos = crear_clusters(datos_negativos, 
                                        min_puntos_cluster_, 
                                        max_puntos_cluster_,
                                        umbral_distancia_)
    
    # Descomentar para visualizar
    #print("Clusters positivos")
    #visualizar_clusters(datos_positivos, min_puntos_cluster_, max_puntos_cluster_, umbral_distancia_)
    #print("Clusters negativos")
    #visualizar_clusters(datos_negativos, min_puntos_cluster_, max_puntos_cluster_, umbral_distancia_)

    # Creo los ficheros JSON de los clusters
    clusters_to_json(clusters_positivos, 'clustersPiernas.json')
    clusters_to_json(clusters_negativos, 'clustersNoPiernas.json')
    
    print("Agrupación finalizada con éxito")