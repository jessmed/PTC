# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

import funciones as fun
import operator
from bs4 import BeautifulSoup
import R2

#*****************************************************************************
#Función que devuelve un gráfico de barras de hombres y mujeres
#dado un vector de hombres,mujeres y los años a estudiar
def creaGraficoR3(men_means,women_means,asistencia):
    #Obtenemos la posicion de cada etiqueta en el eje de X
    x = np.arange(len(asistencia))
    #tamaño de cada barra
    width = 0.50
    
    fig, ax = plt.subplots()
    
    #Generamos las barras para el conjunto de hombres
    rects1 = ax.bar(x - width/2, men_means, width, label='Hombres')
    #Generamos las barras para el conjunto de mujeres
    rects2 = ax.bar(x + width/2, women_means, width, label='Mujeres')
    
    #Añadimos las etiquetas de identificacion de valores en el grafico
    ax.set_ylabel('Poblacion en millones')
    ax.set_title('Población 2017 de las 10 comunidades con más población media')
    ax.set_xticks(x)
    ax.set_xticklabels(asistencia)
    #Añadimos un legen() esto permite mmostrar con colores a que pertence cada valor.
    ax.legend()
    plt.xticks(rotation=90)
    
    fig.tight_layout()
    plt.savefig('imagenes/R3.png',dpi=150)
    plt.clf()

    return()

#*****************************************************************************
def hallaComunidadesMas(path_0,path_1):
    #Creamos diccionario Comunidad:Poblacion media 2017-2010
    #Extraemos información de poblacionComAutonomas y hacemos media de cada comunidad
    
    #Sacamos lista con comunidades autónomas de comunidadesAutonomas.html
    comunidadesFich=open(path_0, 'r', encoding="utf8")
    
    comString=comunidadesFich.read()
    soup = BeautifulSoup(comString, 'html.parser')
    
    celdas=soup.find_all('td')
    
    lista=[]
    aux = 0
    for celda in celdas:
        if aux==1:
            lista.append(celda.get_text())
            aux=0
        else:
            aux = 1
            
    comunidadesFich.close()
    
    #Creo el diccionario con cada comunidad y una lista de provincias vacias
    lista[7]='Castilla-La Mancha'
    comunidades={}
    hombres={}
    mujeres={}
    
    for i in lista:
        comunidades[i]=0
        hombres[i]=0
        mujeres[i]=0
    mediaCom=open(path_1, 'r', encoding="utf8")
    
    comString=mediaCom.read()
    soup = BeautifulSoup(comString, 'html.parser')
    celdas_p=soup.find_all('td')
    cont=0
    aux=-1
    
    #Summamos cada año en cada comunidad
    for celda in celdas_p:
        if cont == 0:
            aux+=1
            
        elif cont < 8:
            suma = comunidades[lista[aux]] + float(fun.convierte(celda.get_text()))
            comunidades[lista[aux]]=suma
        elif cont == 8:
            hombres[lista[aux]]=float(fun.convierte(celda.get_text()))
        elif cont == 16:
            mujeres[lista[aux]]=float(fun.convierte(celda.get_text()))
            
        cont+=1
        cont = cont % 24
    
    #Calculamos la media
    for r in comunidades:
        comunidades[r]=(comunidades[r]/8)
    
    
    #Ordenamos de mayor a menor media
    mayorMedia = sorted(comunidades.items(),key=operator.itemgetter(1),reverse=True)
    
    #Guardamos lista con comunidades más pobladas
    comunidadMas = []
    m=0
    
    for b in mayorMedia:
        comunidadMas.append(b[0])
        m+=1
        if m >9:
            break;
    return(comunidadMas,hombres,mujeres)


#*****************************************************************************

def main():
 
    #---------------------------------------------------------------------------
    #Hallamos lista de las 10 comunidades con más poblacion media
    
    comunidadMas,hombres,mujeres = hallaComunidadesMas('entradas/comunidadesAutonomas.htm','resultados/poblacionComAutonomas.html')
    
    
    #Lista de poblacion en 2017 de hombres y mujeres
    h_2017=[]
    m_2017=[]
    
    for i in comunidadMas:
        m_2017.append(int(mujeres[i]))
        h_2017.append(int(hombres[i]))  
    
    
    
    #Creamos gráfico de la poblacion de hombres y mujeres de 2017 de las comunidades seleccionadas
    creaGraficoR3(m_2017,m_2017,comunidadMas)
    
    
    #Agregamos gráfico a poblacionCOmAutonomas.html
    m=R2.main("../imagenes/R3.png")
    
    


