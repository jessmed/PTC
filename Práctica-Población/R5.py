import numpy as np
import matplotlib.pyplot as plt
import R4 as r4
import R3 as r3
import R2 as r2

def creaGraficoR5(comunidades,datos,years):

    #Obtenemos la posicion de cada etiqueta en el eje de X
    x = np.arange(len(years))
    y_0 = datos[0]
    y_1 = datos[1]
    y_2 = datos[2]
    y_3 = datos[3]
    y_4 = datos[4]
    y_5 = datos[5]
    y_6 = datos[6]
    y_7 = datos[7]
    y_8 = datos[8]
    y_9 = datos[9]
    
    plt.plot(x,y_0,label=comunidades[0])
    plt.plot(x,y_1,label=comunidades[1])
    plt.plot(x,y_2,label=comunidades[2])
    plt.plot(x,y_3,label=comunidades[3])
    plt.plot(x,y_4,label=comunidades[4])
    plt.plot(x,y_5,label=comunidades[5])
    plt.plot(x,y_6,label=comunidades[6])
    plt.plot(x,y_7,label=comunidades[7])
    plt.plot(x,y_8,label=comunidades[8])
    plt.plot(x,y_9,label=comunidades[9])
    
    plt.xticks(x,years)
    
    plt.title("Evolución poblacion comunidades 2017-2010")
    plt.xlabel("Años")
    plt.ylabel("Millones de habitantes")
    lg=plt.legend(bbox_to_anchor=(1.05, 1))
 
    
    plt.savefig('imagenes/R5.png',
                dpi=180,
                bbox_extra_artists=(lg,), 
                bbox_inches='tight')
    

def main():
    #Obtenemos lista 10 comunidades más pobladas
    comunidades,h,m = r3.hallaComunidadesMas('entradas/comunidadesAutonomas.htm','resultados/poblacionComAutonomas.html')
    #NpArray de años a muestrear
    years = np.arange(2017,2009,-1)
    #Matriz nparray cada fila una comunidad
    DB = r2.R2_func('entradas/comunidadesAutonomas.htm','entradas/comunidadAutonoma-Provincia.htm',"entradas/poblacionProvinciasHM2010-17.csv","entradas/archivosAuxiliares/poblacionProvincias_aux.csv",'resultados/poblacionComAutonomas.html','../imagenes/R3.png')
    datos = np.zeros((10,8))
    cont=0
    
    #Para cada comunidad de forma ordenada
    for c in comunidades:
        for i in DB:
            if i == c:
                l = DB[i]
                datos[cont] = l[0:8]
                cont+=1
                  
    #Creamos gráfico
    creaGraficoR5(comunidades,datos, years)
    #Incluimos grafico en el documento hecho en el apartado anterior
    r4.main('../imagenes/R5.png')

    
