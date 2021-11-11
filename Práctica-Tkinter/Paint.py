# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 02:42:09 2020

@author: Jesús Medina Taboada
"""
from tkinter import *
from tkinter.colorchooser import askcolor


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        
        # Creamos ventana y le ponemos nombre
        self.root = Tk()
        self.root.title("Paint")
        
        # Operación a realizar
        self.operacion=""
        
        self.etiqueta = Label(self.root,text="Herramientas")
        self.etiqueta.grid(row=0,column=0)
        
        # Creamos botones y canvas para pintar y definimos su lugar
        
        # PUNTO
        self.punto_button = Button(self.root, text='Punto', command=self.use_punto)
        self.punto_button.grid(row=1, column=0)

        # LINEA
        self.linea_button = Button(self.root, text='Linea', command=self.use_linea)
        self.linea_button.grid(row=1, column=1)
        
        # CUADRADO
        self.cuadrado_button = Button(self.root, text='Cuadrado', command=self.use_cuadrado)
        self.cuadrado_button.grid(row=1, column=2)

        # ELEGIR COLOR
        self.color_button = Button(self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=1, column=3)

        # BORRAR CANVAS
        self.borra_button = Button(self.root, text='Borrar', command=self.borraPantalla)
        self.borra_button.grid(row=1, column=4)

        # ELEGIR TAMAÑO
        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=1, column=5)

        # CANVAS PARA DIBUJAR
        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=2, columnspan=6)

        self.setup()
        self.root.mainloop()

    # Inicializamos estado de la aplicacion con posiciones,color,tamaño
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.active_button = self.punto_button

        
        
        
    ########################################################################
    # Funciones para elegir funcionalidad
    
    def use_punto(self):
        self.activate_button(self.punto_button)
        self.operacion="punto"
        self.c.bind('<Button-1>',self.pinta_punto)
        

    def use_linea(self):
        self.activate_button(self.linea_button)
        self.operacion="linea"
        self.c.bind('<B1-Motion>', self.pinta_linea)
        self.c.bind('<ButtonRelease-1>', self.reset)
        
    def use_cuadrado(self):
        self.activate_button(self.cuadrado_button)
        self.operacion="cuadrado"
        self.c.bind('<Button-3>',self.pinta_cuadrado)
        

    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

    def activate_button(self, some_button):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        
    ###########################################################################
    # Métodos que usan los botones para pintar
    
    # Método para pintar una linea
    def pinta_linea(self, event):
        if self.operacion == "linea":
            
            self.line_width = self.choose_size_button.get()
            paint_color = self.color
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.old_x = event.x
            self.old_y = event.y
    
    # Método para resetear los valores de x e y
    def reset(self, event):
        self.old_x, self.old_y = None, None
        
        
    # Método para pintar un punto
    def pinta_punto(self, event):
        if self.operacion == "punto":
            
            self.line_width = self.choose_size_button.get()
            paint_color = self.color
            
        
            self.c.create_oval(event.x, event.y, event.x, event.y,
                               width=self.line_width, fill=paint_color, outline=paint_color)

                

    # Método para pintar un cuadrado      
    def pinta_cuadrado(self, event):
        if self.operacion == "cuadrado":
            
            self.line_width = self.choose_size_button.get()
            paint_color = self.color
            
            if self.old_x and self.old_y:
                self.c.create_rectangle(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color, outline=paint_color)
                self.old_x = None
                self.old_y = None
            else:
                self.old_x = event.x
                self.old_y = event.y
    

     
    
    # Borra el contenido de la pantalla 
    def borraPantalla(self):
        self.c.delete(ALL)
        self.old_x = None
        self.old_y = None
    
        return


if __name__ == '__main__':
    Paint()