# -*- coding: utf-8 -*-

import csv
import funciones as fun

def main():
    #Primero eliminamos la información que no nos sirve
    
    #Leemos en un string el fichero entero codificando a utf-8
    ficheroInicial=open("entradas/poblacionProvinciasHM2010-17.csv","r", encoding="utf8")
    contenido = ficheroInicial.read()
    ficheroInicial.close()
    
    #Buscamos los puntos ente los que nos interesa cortar la información
    primero=contenido.rfind("Total")   #Usamos rfind() porque necesitamos la segunda instancia
    ultimo=contenido.find("Notas")    
    contenido_util = contenido[primero:ultimo]
    
    #Creamos cabecera para ayudar a distinguir los datos y los escribimos
    cabecera="Provincia;2017;2016;2015;2014;2013;2012;2011;2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011;H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010"
    ficheroFinal=open("entradas/archivosAuxiliares/poblacionProvincias_aux.csv", "w",encoding="utf8")
    ficheroFinal.write(cabecera +'\n' + contenido_util)
    ficheroFinal.close()
    
    
    #Leemos el csv resultante y lo guardamos en un diccionario
    csvfile =  open("entradas/archivosAuxiliares/poblacionProvincias_aux.csv", encoding="utf8")
    dic = csv.DictReader(csvfile,delimiter=';')  
    
    
    
    #Creamos el css para nuestra tabla
    fileEstilo=open("entradas/archivosAuxiliares/estilo.css","w", encoding="utf8")
    
    estilo="""table, th, td {
                    border-collapse: collapse;    
                    border:1px solid black;
                    font-family: Arial, Helvetica, sans-serif;
                    padding: 8px;
                    
                }  """
    
    fileEstilo.write(estilo)
    fileEstilo.close()
    
    #Creamos archivo html donde irá nuestra tabla
    f = open('resultados/variacionProvincias.html','w', encoding="utf8" )
    
    #Añadimos la cabecera
    paginaPob = """<!DOCTYPE HTML5><html>
    <head><title>variacionProvincias</title>
    <link rel="stylesheet" href="../entradas/archivosAuxiliares/estilo.css">
    <meta charset="utf8"></head>
    <body><h1>Variación de la población por provincias</h1>"""
    
    #Preparamos los campos de nuestra tabla(años y medidas estadísticas)
    cabecera_2 = "Provincia;2017;2016;2015;2014;2013;2012;2011;2017;2016;2015;2014;2013;2012;2011"
    cabecera_2=cabecera_2.split(';')
    
    
    paginaPob+= """<table>
    <tr>
    <th></th>
    <th colspan="7">Variacion absoluta</th>
    <th colspan="7">Variacion relativa</th>
    </tr>"""
    
    paginaPob+="<tr>"
    for nomColumna in cabecera_2:
        paginaPob+="<th>%s</th>" % (nomColumna)
    
    paginaPob+="</tr>"
    
    #Una vez tenemos el armazón rellenamos los datos de la tabla
    
    #Para cada fila de nuestro objeto dicReader que es un diccionario
    for fila in dic:
        #Pintamos el nombre de la comunidad
        paginaPob+="<tr><th>%s</th>" % (fila['Provincia'])
        
        #Añadimos los datos calculados por años
        for i in range(2017,2010,-1):
            #variación absoluta 2017=población 2017 – población 2016
            num = float(fila[str(i)])-float(fila[str(i-1)])
            num =  fun.separador_miles(num,'i')
            paginaPob+="<td>%s</td>" % (str(num))
        for i in range(2017,2010,-1):
            #variación relativa 2017=(variación absoluta 2017 / población 2016) * 100
            num = float(fila[str(i)])-float(fila[str(i-1)])
            num = (num / float(fila[str(i-1)]))*100
            num =  fun.separador_miles(num)
            paginaPob+="<td>%s</td>" % (str(num))
    
    paginaPob+="</tr>"
    paginaPob+="</body></html>"
    
    f.write(paginaPob)
    f.close()
    csvfile.close()   
