# -*- coding: utf-8 -*-

import csv
import funciones as fun
from bs4 import BeautifulSoup


"""   
    1)EXTRAEMOS LA INFORMACIÓN:
    -Listado de comunidades autónomas(comunidadesAutonomas.html)
    -Provincias de cada comunidad autónoma(comunidadesAutónomas-Provincia.html)
    -Datos por año y por género de la poblacion(poblacionProvinciasHM2010-2017.csv)
    
    2)CREAMOS EL ARCHIVO HTML FINAL
"""

def R2_func(path_1,path_2,path_3,path_4,path_5,path_6):
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
    
    #------------------------------------------------------------------------------------
    
    #Sacamos diccionario con provincias de cada comunidad autónoma
    comunidadesProv=open(path_2, 'r', encoding="utf8")
    
    proString=comunidadesProv.read()
    soup = BeautifulSoup(proString, 'html.parser')
    
    celdas_p=soup.find_all('td')
    
    #Creo el diccionario con cada comunidad y una lista de provincias vacias
    lista[7]='Castilla-La Mancha'
    provincias={}
    listas=[]
    for i in lista:
        provincias[i]=[]
        
    #Recorro los datos extraidos de la web y los clasifico según su comunidad
    for celda in celdas_p:
        if len(celda.get_text())<3 or celda.get_text()=='Ciudades    Autónomas:':
            pass
        else:
            listas.append(celda.get_text())
    
    p=0
    while p < len(listas):
        l_2 = provincias[listas[p]]
        l_2.append(listas[p+1])
        provincias[listas[p]]=l_2
        p+=2
    
    
        
    comunidadesProv.close()
    
    #------------------------------------------------------------------------------------
    
    #Obtenemos datos de población según provincia, sexo y años
    #Primero eliminamos la información que no nos sirve
    #Leemos en un string el fichero entero codificando a utf-8
    ficheroInicial=open(path_3,"r", encoding="utf8")
    contenido = ficheroInicial.read()
    ficheroInicial.close()
    
    #Buscamos los puntos ente los que nos interesa cortar la información
    primero=contenido.rfind("Total")   #Usamos rfind() porque necesitamos la segunda instancia
    ultimo=contenido.find("Notas")    
    contenido_util = contenido[primero:ultimo]
    
    #Creamos cabecera para ayudar a distinguir los datos y los escribimos
    cabecera="Comunidad;2017;2016;2015;2014;2013;2012;2011;2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011;H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010"
    ficheroFinal=open(path_4, "w",encoding="utf8")
    ficheroFinal.write(cabecera +'\n' + contenido_util)
    ficheroFinal.close()
    
    
    #------------------------------------------------------------------------------------
    
    #Creamos archivo html donde irá nuestra tabla
    f = open(path_5,'w', encoding="utf8" )
    
    #Añadimos la cabecera
    paginaPob = """<!DOCTYPE HTML5><html>
    <head><title>variacionComunidades</title>
    <link rel="stylesheet" href="../entradas/archivosAuxiliares/estilo.css">
    <meta charset="utf8"></head>
    <body><h1>Población por comunidades autónomas</h1>"""
    
    #Preparamos los campos de nuestra tabla(años y medidas estadísticas)
    cabecera=cabecera.split(';')
    
    
    paginaPob+= """<table>
    <tr>
    <th></th>
    <th colspan="8">Total</th>
    <th colspan="8">Hombres</th>
    <th colspan="8">Mujeres</th>
    </tr>"""
    
    paginaPob+="<tr>"
    for nomColumna in cabecera:
        paginaPob+="<th>%s</th>" % (nomColumna)
    
    paginaPob+="</tr>"
    
    
    #Creamos diccionario final con la información que queremos
    DB={}
    for com in  lista:
        DB[com]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
     
    labels="2017;2016;2015;2014;2013;2012;2011;2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011;H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010"
    labels = labels.split(';')
    #Leemos el csv resultante y lo guardamos en un diccionario
    csvfile =  open(path_4, encoding="utf8")
    di = csv.DictReader(csvfile,delimiter=';')  
    dic=[]
    
    #Copiamos resultado del dicreader a una lista de diccionarios por el error de que no deja recorrerlo
    for r in di:
        dic.append(r)
    
    
    for c in provincias:     #para cada comunidad
        
        lista_provincias = provincias[c]   #guardamos en una variable la lista de provincias que la componen
        
        for row in dic:      #para cada provincia guardada en el diccionario   
           
            st = row['Comunidad'] 
            s=st[3:]
            
            if s in lista_provincias:
                x=0
                for j in labels:
                    t = DB[c]   #Lista de comunidad
                    t[x] += float(row[j])
                    DB[c]=t
                    x+=1
            
    
    
    #Una vez tenemos nuestra base de datos rellenamos la tabla
    for d in DB:
        paginaPob+="<tr><th>%s</th>" % (d)
        for a in DB[d]:
            num =  fun.separador_miles(a,'i')
            paginaPob+="<td>%s</td>" % (str(num))
    
    
    
    
    
    paginaPob+="</tr>"
    
    if path_6 != '':
        paginaPob+="<img src=%s>" % (path_6)
    paginaPob+="</body></html>"
    
    f.write(paginaPob)
    f.close()
    csvfile.close()   
    
    return(DB)

def main(s=''):
    #Ejecucion
    DB = R2_func('entradas/comunidadesAutonomas.htm','entradas/comunidadAutonoma-Provincia.htm',"entradas/poblacionProvinciasHM2010-17.csv","entradas/archivosAuxiliares/poblacionProvincias_aux.csv",'resultados/poblacionComAutonomas.html',s)
    