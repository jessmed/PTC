# -*- coding: utf-8 -*-

import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as sn
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import joblib

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

semilla = 45237 # Semilla a usar para permitir repetibilidad de los resultados

def mostrar_matriz_confusion(y_test, y_pred):
    """
    Muestra la matriz de confusión a partir de @y_test y @y_pred haciendo
    uso de sn.heatmap().
    """
    # Obtengo los valores de la matriz de confusión
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Los paso a dataframe
    conf_matrix = pd.DataFrame(conf_matrix, index=['No Pierna', 'Pierna'],
                               columns=['No Pierna', 'Pierna'])
    
    # Los represento usando sn.heatmap
    plt.figure(figsize = (7,5)) # Tamaño de la gráfica
    ax = sn.heatmap(conf_matrix, vmin=0, annot=True, fmt="d", linewidths=2)
    
    # Establezco los límites de la gráfica de forma manual para solucionar
    # el siguiente bug de seaborn: https://github.com/matplotlib/matplotlib/issues/14675
    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)
    
    # Nombre de los ejes
    ax.set_ylabel('Clase Verdadera')
    ax.set_xlabel('Clase Predicha')
    
    plt.show()
    

def entrenar_SVM(kernel, X, y, X_train, y_train, X_test, y_test, param_grid):
    """
    Entrena un SVM del tipo dado por @kernel. Según el tipo de @kernel usado,
    usa 5-CV para elegir los mejores valores de los parámetros a usar, según
    @param_grid.
    """
    
    # Calculo los mejores valores de los hiperparámetros a usar según
    # el tipo de kernel
    
    if kernel=='linear':
        # Uso gridSearchCV para elegir el mejor valor de C sobre el 
        # conjunto de training
        
        # Uso refit=False porque solo quiero obtener los mejores valores
        # de los parámetros
        clf=GridSearchCV(SVC(kernel='linear'), param_grid, cv=5, refit=False)
        clf=clf.fit(X_train, y_train)
        
        mejor_C = clf.best_params_['C']
        
        print("\nMejor valor de C:", mejor_C)
        
        # Uso la SVM con el C elegido usando gridSearchCV
        mejor_svc = SVC(kernel='linear', C=mejor_C)
    
    elif kernel=='poly':
        # Uso gridSearchCV para elegir el mejor valor de C y degree sobre el conjunto de training
        
        # Uso refit=False porque solo quiero obtener los mejores valores
        # de los parámetros
        clf=GridSearchCV(SVC(kernel='poly'), param_grid, cv=5, refit=False)
        clf=clf.fit(X_train, y_train)
        
        mejor_C = clf.best_params_['C']
        mejor_grado = clf.best_params_['degree']
        
        print("\nMejor valor de C:", mejor_C)
        print("Mejor valor del grado:", mejor_grado)
        
        # Uso la SVM con el C y degree elegidos usando gridSearchCV
        mejor_svc = SVC(kernel='poly', C=mejor_C, degree=mejor_grado)
        
    elif kernel=='rbf':
        # Uso gridSearchCV para elegir el mejor valor de C y gamma sobre el 
        # conjunto de training
        
        # Uso refit=False porque solo quiero obtener los mejores valores
        # de los parámetros
        clf=GridSearchCV(SVC(kernel='rbf'), param_grid, cv=5, refit=False)
        clf=clf.fit(X_train, y_train)
        
        mejor_C = clf.best_params_['C']
        mejor_gamma = clf.best_params_['gamma']
        
        print("\nMejor valor de C:", mejor_C)
        print("Mejor valor de gamma:", mejor_gamma)
        
        # Uso la SVM con el C y gamma elegidos usando gridSearchCV
        mejor_svc = SVC(kernel='rbf', C=mejor_C, gamma=mejor_gamma)
        
    else: # El kernel no es válido: lanzo una excepción
        raise ValueError("El parámetro kernel debe ser \
                         'linear', 'poly' o 'rbf'")
        
        
    # Uso la SVM con los parámetros elegidos con gridSearchCV sobre
    # training
        
    # La entreno sobre training
    mejor_svc.fit(X_train, y_train)
    
    # La uso para predecir sobre test
    y_pred = mejor_svc.predict(X_test)
    
    # Obtengo la accuracy sobre test
    acc_test = accuracy_score(y_test, y_pred)
    print("\nAcc_test: %0.4f" % acc_test)
    
    # Obtengo distintas métricas sobre test
    print("\nMétricas sobre test:")
    print(classification_report(y_test, y_pred))
    
    # Pinto la matriz de confusión sobre test
    print("\nMatriz de confusión sobre test:")
    mostrar_matriz_confusion(y_test, y_pred)
     
    # Obtengo el score sobre test usando validación cruzada
    # para asegurarme de que el conjunto de test usando
    # anteriormente es representativo
    
    # Uso la SVM con el C elegido usando gridSearchCV
    scores = cross_val_score(mejor_svc, X, y, cv=5)
    
    # Exactitud media con intervalo de confianza del 95%
    print("\nAcc_test 5-CV: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
    
    # Devuelvo el modelo entrenado
    return mejor_svc
    
        
def main():
    # Cargo y divido el dataset
    
    # Leo el fichero csv conteniendo los datos
    datos = np.genfromtxt('piernasDataset.csv', delimiter=',') # Me formatea los contenidos del fichero en un numpy array
    
    # Separo los atributos de las etiquetas
    X_ori = datos[:,:-1] # Atributos
    y = datos[:, -1] # Etiquetas
    
    # Normalizo los datos para que cada característica tenga media 0
    # y desviación típica 1
        
    medias = np.average(X_ori, axis=0) # Media de cada característica
    desv_tipicas = np.std(X_ori, axis=0) # Desviación típica de cada característica
    X_norm = (X_ori - medias) / desv_tipicas # dataset normalizado
    
    # Repito dos experimentos dos veces: una con los datos "tal cual"
    # y otra con los datos normalizados
    
    modelos = [] # Array con los 6 modelos entrenados
    
    for X, mensaje_print in [(X_ori, '\n\nDataset sin normalizar\n\n'),
                             (X_norm, '\n\nDataset normalizado\n\n')]:
        
        print(mensaje_print)
        
        # Guardo un 20% de los datos para test
        # Uso el parámetro stratify para que las clases estén balanceadas
        # en los conjuntos de training y test (la proporción entre ejemplos
        # positivos y negativos sea aprox. la misma en ambos conjuntos)
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                           test_size = 0.20,
                                           random_state=semilla, stratify=y)
    
        # Entreno distintos tipos de SVM y veo cuál es mejor
        
        # Kernel Lineal
        
        # Valores a probar para C
        param_grid={'C':[0.1,1,10,100,1000, 10000]}
        
        print("\n<Kernel Lineal>\n")
        modelo = entrenar_SVM('linear', X, y, X_train, y_train, X_test, y_test, param_grid)
        
        modelos.append(modelo) # Guardo el modelo entrenado
        
        # Kernel Poly
        
        # Valores a probar para C y el grado del polinomio
        param_grid={'C':[0.1,1,10], 'degree':[2,3,4,5]}
        
        print("\n\n<Kernel Polinomial>\n")
        modelo = entrenar_SVM('poly', X, y, X_train, y_train, X_test, y_test, param_grid)
        
        modelos.append(modelo) # Guardo el modelo entrenado
        
        # Kernel rbf
        
        # Valores a probar para C y el valor de gamma
        param_grid={'C':[0.1,1,10,100,1000, 10000], 'gamma':[0.001, 0.005, 0.01, 0.1]}
        
        print("\n\n<Kernel de base radial>\n")
        modelo = entrenar_SVM('rbf', X, y, X_train, y_train, X_test, y_test, param_grid)
        
        modelos.append(modelo) # Guardo el modelo entrenado
  
    # Guardo a disco el mejor modelo de todos
    
    mejor_modelo = modelos[5]
    
    # Lo guardo usando joblib
    joblib.dump(mejor_modelo, 'clasificador.pkl')
    print("Entrenamiento del clasificador completado")