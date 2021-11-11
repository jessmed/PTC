# -*- coding: utf-8 -*-

import locale
#Funcion que pone los puntos de miles y devuelve un int o float segun el parametro t
def separador_miles(num,t='f'):

    locale.setlocale(locale.LC_ALL,'')
    if t=='i':
        return(locale.format_string('%.0f', num, grouping=True))
    else:
        return(locale.format_string('%.2f', num, grouping=True))


def convierte(num):
    l = num.split('.')
    cadena =''
    for i in l:
        cadena+=i
        
    return(cadena)
