# -*- coding: utf-8 -*- 

import vrep
import sys
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import json
import os
import glob


def captura(nom_fich,num_ciclos,clientID):
    tiempo_espera=0.5
        
    # Abrimos fichero JSON y escribimos los datos
    cabecera={"TiempoSleep":tiempo_espera,
              "MaxIteraciones":num_ciclos}
    
    ficheroLaser=open(nom_fich, "w")
    
    ficheroLaser.write(json.dumps(cabecera)+'\n')
      
    
    # Obtenemos los datos de la simulación y los vamos guardando
    
    #Guardar la referencia al robot
    _, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
            
    #Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
     
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    
     
    #Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    
    
    plt.axis('equal')
    plt.axis([0, 4, -2, 2]) 
    
    iteracion=0 
    seguir=True
 
 
    while(iteracion<num_ciclos and seguir):
        puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
        puntosy=[]
        puntosz=[]
        returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
        time.sleep(tiempo_espera) #esperamos un tiempo para que el ciclo de lectura de datos no sea muy rápido
        datosLaser=vrep.simxUnpackFloats(signalValue)
        for indice in range(0,len(datosLaser),3):
            puntosx.append(datosLaser[indice+1])
            puntosy.append(datosLaser[indice+2])
            puntosz.append(datosLaser[indice])
        
        print("Iteración: ", iteracion)        
        plt.clf()    
        plt.plot(puntosx, puntosy, 'r.')
        plt.show()
        
        #Guardamos los puntosx, puntosy en el fichero JSON
        lectura={"Iteracion":iteracion, "PuntosX":puntosx, "PuntosY":puntosy}
        #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
        ficheroLaser.write(json.dumps(lectura)+'\n')
         
        
        #Guardar frame de la camara, rotarlo y convertirlo a BGR
        _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype = np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        img = np.rot90(img,2)
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
     
        print(resolution)
     
         
        #Convertir img a hsv y detectar colores
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        verde_bajos = np.array([49,50,50], dtype=np.uint8)
        verde_altos = np.array([80, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, verde_bajos, verde_altos) #Crear mascara
     
        #Limpiar mascara y buscar centro del objeto verde
        moments = cv2.moments(mask)
        area = moments['m00']
        if(area > 200):
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])
            cv2.rectangle(img, (x, y), (x+2, y+2),(0,0,255), 2)
          
        #Mostrar frame y salir con "ESC"
        cv2.imshow('Image', img)
        cv2.imshow('Mask', mask)
        
        # Guardo en disco la imagen si es la primera o última iteración
        if iteracion == 0 or iteracion == num_ciclos-1:
            cv2.imwrite(nom_fich+str(iteracion)+'.jpg', img)
    
        
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            seguir=False
        
        iteracion=iteracion+1
       
    
    time.sleep(1)
    

    
    #cerramos las ventanas
    cv2.destroyAllWindows()
    
    finFichero={"Iteraciones totales":iteracion}
    ficheroLaser.write(json.dumps(finFichero)+'\n')
    ficheroLaser.close()