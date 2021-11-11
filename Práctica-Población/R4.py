# -*- coding: utf-8 -*-

import numpy as np
import funciones as fun
from bs4 import BeautifulSoup

def R4_func(path_1,path_2,path_3,image):
    #Sacamos lista con comunidades autónomas de comunidadesAutonomas.html
    comunidadesFich=open(path_1, 'r', encoding="utf8")
    
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
    
    #Creo el diccionario con cada comunidad
    lista[7]='Castilla-La Mancha'
    comunidades={}
    
    for i in lista:
        comunidades[i]=[]
    
    
    #Reutilizaremos la tabla que hicimos en el apartado anterior
    mediaCom=open(path_2, 'r', encoding="utf8")
    
    comString=mediaCom.read()
    soup = BeautifulSoup(comString, 'html.parser')
    celdas_p=soup.find_all('td')
    
    cont=0
    aux=-1
    #Summamos cada año en cada comunidad
    for celda in celdas_p:  
        if cont == 0:
            aux+=1
        if cont > 7:
            l = comunidades[lista[aux]]
            l.append(float(fun.convierte(celda.get_text())))
            comunidades[lista[aux]]=l
            
        cont+=1
        cont = cont % 24
    
    #Usamos el css que ya tenemos
    
    
    #Creamos archivo html donde irá nuestra tabla
    f = open(path_3,'w', encoding="utf8" )
    
    #Añadimos la cabecera
    paginaPob = """<!DOCTYPE HTML5><html>
    <head><title>Variacion Com.Autnomas</title>
    <link rel="stylesheet" href="../entradas/archivosAuxiliares/estilo.css">
    <meta charset="utf8"></head>
    <body><h1>Variación de la población  por comunidades autónomas</h1>"""
    
    #Preparamos los campos de nuestra tabla(años y medidas estadísticas)
    cabecera_2 = "Comunidades;2017;2016;2015;2014;2013;2012;2011;2017;2016;2015;2014;2013;2012;2011;2017;2016;2015;2014;2013;2012;2011;2017;2016;2015;2014;2013;2012;2011"
    cabecera_2=cabecera_2.split(';')
    
    
    paginaPob+= """<table>
    <tr>
    <th></th>
    <th colspan="14">Variacion absoluta</th>
    <th colspan="14">Variacion relativa</th>
    </tr>
    <tr>
    <th></th>
    <th colspan="7">HOMBRES</th>
    <th colspan="7">MUJERES</th>
    <th colspan="7">HOMBRES</th>
    <th colspan="7">MUJERES</th>
    </tr>"""
    
    paginaPob+="<tr>"
    for nomColumna in cabecera_2:
        paginaPob+="<th>%s</th>" % (nomColumna)
    
    paginaPob+="</tr>"
    
    #Una vez tenemos el armazón rellenamos los datos de la tabla
    
    #Para cada fila de nuestro objeto dicReader que es un diccionario
    for fila in comunidades:
        #Pintamos el nombre de la comunidad
        paginaPob+="<tr><th>%s</th>" % (fila)
        
        #Añadimos los datos calculados por años
        L=comunidades[fila]
    
        for i in range(14):
            #variación absoluta 2017=población 2017 – población 2016
            
            num = L[i]-L[i+1]
            num =  fun.separador_miles(num,'i')
            paginaPob+="<td>%s</td>" % (str(num))
        for j in range(14):
            #variación relativa 2017=(variación absoluta 2017 / población 2016) * 100
    
            num = L[j]-L[j+1]
            num = (num / L[j+1])*100
            num =  fun.separador_miles(num)
            paginaPob+="<td>%s</td>" % (str(num))
    
    paginaPob+="</tr>"
    if image != '':
        paginaPob+="<img src=%s>" % (image)
    paginaPob+="</body></html>"
    
    f.write(paginaPob)
    f.close()
    
def main(s=''):
    #Ejecucion
    R4_func('entradas/comunidadesAutonomas.htm','resultados/poblacionComAutonomas.html','resultados/variacionComAutonomas.html',s)

