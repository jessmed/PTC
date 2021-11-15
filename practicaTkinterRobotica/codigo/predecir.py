# -*- coding: utf-8 -*-

import vrep
import sys
import time
import numpy as np
import joblib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.colors as mcolors # Lista de colores de matplotlib

import agrupar
import caracteristicas as carac
from caracteristicas import dist

def obtener_datos_laser_simulador(terminar_conexion=True):
    """
    Se conecta al simulador y obtiene los datos del láser, que devuelve
    como una lista de dos elementos: lista[0] es una lista con las coordenadas
    X de los puntos y lista[1] una lista con las coordenadas Y. También
    devuelve el clientID y robothandle.

    """
    vrep.simxFinish(-1) #Terminar todas las conexiones
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) #Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)
    
    # Primero lanzar play en la escena y después ejecutar python
     
    if clientID!=-1:
        print ('Conexion establecida')
    else:
        sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.") #Terminar este script
     
    #Guardar la referencia al robot
    
    _, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
                 
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    
    # Hay que esperar un segundo antes de poder acceder a los datos del láser
    time.sleep(1)    
    
    puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
    puntosy=[]
    puntosz=[]
    returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
    
    datosLaser=vrep.simxUnpackFloats(signalValue)
    for indice in range(0,len(datosLaser),3):
        puntosx.append(datosLaser[indice+1])
        puntosy.append(datosLaser[indice+2])
        puntosz.append(datosLaser[indice])

    if terminar_conexion:
        #detenemos la simulacion
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
        
        #cerramos la conexion
        vrep.simxFinish(clientID)   
    
    # Devuelvo los puntos y el clientID
    return [puntosx, puntosy], clientID, robothandle

def clusters_to_dict(clusters):
    """
    Transforma los clusters del formato que devuelve la función
    agrupar.crear_clusters() a un formato de lista de diccionarios 
    (formato que recibe la función caracteristicas.obtener_carac_clusters())
    """
    
    clusters_dict = []
    
    for ind_cluster, cluster in enumerate(clusters):
        num_puntos = len(cluster) # Número de puntos del cluster
            
        puntos = np.array(cluster) # Lo convierto a numpy array para poder separar las coordenadas X e Y
        puntos_X = list(puntos[:,0]) # Los convierto a lista para que puedan ser guardados en el 
        puntos_Y = list(puntos[:,1]) # diccionario
        
        # Creo el diccionario que guarda la información del cluster actual
        dict_cluster = {'numero_cluster':ind_cluster, 'numero_puntos':num_puntos,
                        'puntosX':puntos_X, 'puntosY':puntos_Y}
        
        # Añado el cluster a la lista de clusters
        clusters_dict.append(dict_cluster)

    return clusters_dict

def carac_clusters_to_matrix(caracs):
    """
    Transforma las características de los clústeres del formato que devuelve
    la función carac.obtener_carac_clusters al formato que recibe
    como entrada el modelo (un numpy array donde cada fila son las
    características de un clúster).
    """
    
    matrix_carac = [list(elem.values())[1:] for elem in caracs]
    
    # La convierto a numpy array
    matrix_carac = np.array(matrix_carac)
    
    return matrix_carac

def normalizar_dataset_test(X, fich_dataset_train, separador=','):
    """
    Normaliza X restándole la media y dividiéndolo entre la desviación
    típica del dataset de entrenamiento del fichero de la ruta 
    fich_dataset_train. Esta operación se hace por cada característica
    por separado.
    """
    # Leo el fichero csv conteniendo los datos
    datos = np.genfromtxt(fich_dataset_train, delimiter=separador) # Me formatea los contenidos del fichero en un numpy array
    
    # Me quedo solo con los atributos (elimino las etiquetas)
    X_train = datos[:,:-1] # Atributos

    # Calculo la media y desviación típica del dataset de entrenamiento
    medias = np.average(X_train, axis=0) # Media de cada característica
    desv_tipicas = np.std(X_train, axis=0) # Desviación típica de cada característica
    
    # Normalizo el dataset X
    X_norm = (X - medias) / desv_tipicas # dataset normalizado
    
    return X_norm

def dibujar_clusteres_clasificados(clusters_dict, y_pred, umbral_dist=0.4):
    """
    Dibuja los puntos de los clústeres usando matplotlib de un color
    diferente según si son clasificados como piernas o no. Además,
    se pinta la posición del objeto cuando se detectan dos clústeres
    cercanos pertenecientes al mismo objeto.
    """
        
    # Colores de cada clase
    colores = {0:'blue', 1:'red'}
    
    # Tamaño de la gráfica
    plt.figure(figsize = (7,5)) 
    
    # Dibujo cada cluster        
    for cluster, pred in zip(clusters_dict, y_pred):                        
        plt.scatter(cluster['puntosX'], cluster['puntosY'],
                    s=10,
                    color=colores[int(pred)])
        
    # Dibujo las posiciones de los objetos

    # Calculo los centroides de los clusters    
    cent_clusters = []
    
    for cluster in clusters_dict:
        cent_x = float(np.average(cluster['puntosX']))
        cent_y = float(np.average(cluster['puntosY']))
        
        cent_clusters.append((cent_x, cent_y))
        
    # Veo si cada clúster lo puedo agrupar con otro
    
    # Cada cluster solo se puede agrupar como máximo con otro
    clusters_agrupados = [False] * len(clusters_dict)
    
    for i in range(len(clusters_dict)-1):
        for j in range(i+1, len(clusters_dict)):
            # Cada cluster solo se puede agrupar con otro como mucho
            if clusters_agrupados[i] == False and clusters_agrupados[j] == False:
                # Para que ambos clústeres puedan ser del mismo objeto,
                # tienen que pertenecer a la misma clase
                if y_pred[i] == y_pred[j]:
                    # Calculo la distancia entre sus centroides
                    dist_clusters = dist(cent_clusters[i][0], cent_clusters[i][1],
                                         cent_clusters[j][0], cent_clusters[j][1])
                    
                    # Si están cerca, son del mismo objeto
                    if dist_clusters <= umbral_dist:
                        # Calculo la posición del objeto al que pertenecen
                        # los dos clusters
                        pos_obj_x = (cent_clusters[i][0] + cent_clusters[j][0]) / 2
                        pos_obj_y = (cent_clusters[i][1] + cent_clusters[j][1]) / 2
                        
                        # Muestro un punto (con forma de cuadrado) en la posición
                        # del objeto, según la clase a la que pertenece
                        plt.scatter(pos_obj_x, pos_obj_y, s=40,
                                    color='green',
                                    marker='.')
                        
                        # Marco los clusters como ya agrupados
                        clusters_agrupados[i] = clusters_agrupados[j] = True
        
    # Muestro las leyendas
    
    leg_no_pierna = mlines.Line2D([], [], color='blue', marker='o',
                          markersize=5, label='No Pierna (0)')
    leg_pierna = mlines.Line2D([], [], color='red', marker='o',
                          markersize=5, label='Pierna (1)')
    
    plt.legend(handles=[leg_no_pierna, leg_pierna], loc='upper left')
         
    plt.savefig("prediccion/prediccion.jpg")
    plt.show()
    
    
def visualizar_clusters_por_separado(dict_clusters):
    """
    Representa los clusters (clusters tiene como formato una lista
    de diccionarios), cada uno de un color diferente.
    """
        
    # Tamaño de la gráfica
    plt.figure(figsize = (7,5)) 
    
    for cluster in dict_clusters:                        
        plt.scatter(cluster['puntosX'], cluster['puntosY'],
                    s=10,
                    color=np.random.rand(3,)) # Cada cluster lo pinto de un color aleatorio
        
    plt.show()

def clusterizar_y_clasificar(datos_laser, min_puntos_cluster, max_puntos_cluster,
                             umbral_distancia, nom_modelo, nom_dataset_train):
    """
    A partir de los datos del láser del simulador, realiza todo el proceso:
    genera los clusters, obtiene sus características geométricas y los
    clasifica con el modelo nom_modelo preentrenado.

    """
    # Convierto los datos en clústeres
    clusters = agrupar.crear_clusters(datos_laser, min_puntos_cluster, 
                                        max_puntos_cluster,
                                        umbral_distancia)
    
    # Obtengo las características geométricas de los clústeres
    
    # Transformo los clusters a un formato de diccionario
    clusters_dict = clusters_to_dict(clusters)
    
    # Obtengo sus características geométricas
    # datos_etiquetados=False, porque no sé si los clusters son de piernas
    # o no
    carac_clusters = carac.obtener_carac_clusters(clusters_dict, False)
    
    # Uso el clasificador entrenado para clasificar los clústeres
    
    # Cargo el clasificador
    clasificador = joblib.load(nom_modelo) 
    
    # Convierto las características al formato que acepta el modelo
    # como entrada
    X = carac_clusters_to_matrix(carac_clusters)
    
    # Normalizo las características de la misma forma que el dataset
    # de entrenamiento (uso la media y desviación típica del dataset
    # de entrenamiento)
    X_norm = normalizar_dataset_test(X, nom_dataset_train)
    
    # Uso el clasificador para predecir la clase de cada clúster
    y_pred = clasificador.predict(X_norm)
    
    return clusters_dict, y_pred


def main():
    # Recibo los datos del láser de la escena de test
    datos_laser, _, _ = obtener_datos_laser_simulador()

    # Realizo todo el proceso de clustering y clasificación de los
    # puntos del láser
    
    # Parámetros para el algoritmo de salto
    min_puntos_cluster = 3
    max_puntos_cluster = 50
    umbral_distancia = 0.04
    
    clusters_dict, y_pred = clusterizar_y_clasificar([datos_laser],
                             min_puntos_cluster,
                             max_puntos_cluster, umbral_distancia,
                             'clasificador.pkl', 'piernasDataset.csv')
    
    # Dibujo los clusters obtenidos según su clase
    dibujar_clusteres_clasificados(clusters_dict, y_pred)
    
