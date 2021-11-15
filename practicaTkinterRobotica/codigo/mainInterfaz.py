from tkinter import *
import os
import vrep
import capturar as c
import agrupar as a
import caracteristicas as e
import clasificarSVM as t
import predecir as p

# VARIABLES 
CONEXION = False
WINDOW_TITLE = "Práctica PTC Tkinter Robótica"
P1=50
P2=0.5
P3=1.5
P4=2.5
P5=0
P6=0
P7=0.0
clientID=-1


# Condicion capturados False si tienes que tomar los datos por primera vez
capture = [True for i in  range(0,12)]

# Creamos ventana con titulo y fijamos tamaño
window = Tk()
window.geometry('700x300')
window.title(WINDOW_TITLE)



# =============================================================================
# MAIN
# =============================================================================

# Creamos directorios positivo1-6 y negativo1-6 si no existen
nuevoDir="positivo"
for i in range(6):
    nuevoDir+= str(i+1)
    if (os.path.isdir(nuevoDir)):
        print("Error: ya existe el directorio "+ nuevoDir)
    else:
        os.mkdir(nuevoDir)
    nuevoDir="positivo"
        
nuevoDir="negativo"
for i in range(6):
    nuevoDir+= str(i+1)
    if (os.path.isdir(nuevoDir)):
        print("Error: ya existe el directorio "+ nuevoDir)
    else:
        os.mkdir(nuevoDir)
    nuevoDir="negativo"

if (os.path.isdir("prediccion")):
    print("Error: ya existe el directorio prediccion")
else:
    os.mkdir("prediccion")



# =============================================================================
# INTERFAZ
# =============================================================================


# =============================================================================
# COLUMNA 0 
# =============================================================================

# Creamos labes y botones y fijamos su ubicacion con grid
lbl_1 = Label(window, text="Es necesario ejecutar el simulador VREP")
lbl_1.grid(column=0, row=0)

def conectar():
    vrep.simxFinish(-1) #Terminar todas las conexiones
    global clientID
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) #Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)
    clientID=0
    if clientID!=-1:
        print ('Conexion establecida')
        global CONEXION
        CONEXION=True
        p= messagebox.showinfo(message="Conexión con VREP establecida",title=WINDOW_TITLE) 
        btn_2['state'] = 'normal'
        btn_3['state'] = 'normal'
        lbl_2.config(text="Estado: Conectado a VREP")
        
               
    else:
        messagebox.showerror(message="Debe iniciar el simulador",title=WINDOW_TITLE) 
        print("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.") #Terminar este script

     
btn_1 = Button(window, text="Conectar con VREP", padx=10,command=conectar)
btn_1.grid(column=0, row=1)

def desconectar(): 
    # Detiene la simulacion y cierra conexión
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    vrep.simxFinish(clientID)
    global CONEXION
    CONEXION=False
    #cerramos las ventanas
    #cv2.destroyAllWindows()
    
    # Deshabilita botones capturar,desconectar y el resto
    btn_2['state'] = 'disabled'
    btn_3['state'] = 'disabled'
    btn_4['state'] = 'disabled'
    btn_5['state'] = 'disabled'
    btn_6['state'] = 'disabled'
    btn_7['state'] = 'disabled'
    lbl_2.config(text="Estado: No conectado a VREP")
    messagebox.showinfo(message="Se ha desconectado de VREP",title=WINDOW_TITLE) 
    
    
btn_2 = Button(window, text="Detener y desconectar VREP", padx=10,state=DISABLED,command=desconectar)
btn_2.grid(column=0, row=2)

lbl_2 = Label(window, text="Estado: No conectado a VREP")
lbl_2.grid(column=0, row=3)


def capturar(): 
    
    tuple=()
    eleccion=list.curselection()
    
    # Si se elige un fichero de la lista
    if eleccion!=tuple:
        fichero =list.get(eleccion)
        # Se mira si ya existe o no
        existe = os.path.isfile(fichero)
        # Si existe
        if existe:
            p= messagebox.askyesno(message="El fichero:{} Ya existe. Se creará de nuevo. ¿Está segur0?".format(fichero),title=WINDOW_TITLE) 
            if p:
                file = open(fichero, "w")
                file.close()
        # Si no existe
        else:
            p=messagebox.askyesno(message="Se va a crear el fichero:{} ¿Está seguro?".format(fichero),title=WINDOW_TITLE)
            if p:
                file = open(fichero, "w")
                file.close()
    # Si no se ha elegido fichero de la lista
    else:
        messagebox.showwarning(message="Debe elegir un fichero de la lista",title=WINDOW_TITLE) 
    
    # Llamada del script capturar.py
    print(fichero)
    
    c.captura(fichero,P1,clientID)
    capture[eleccion[0]]=True
    # Si se han capturado los 12 fichero habilitamos boton agrupar
    if False in capture:
        print("Faltan ficheros por capturar")
    else:
        btn_4['state'] = 'normal'
        
btn_3 = Button(window, text="Capturar", padx=10,state=DISABLED,command=capturar)
btn_3.grid(column=0, row=4)

def agrupar(): 
    # Llama al script agrupar.py
    # Genera ficheros con los clusters positivos y negrativos
    # Habilita boton Extraer caracteristicas
    btn_5['state'] = 'normal'
    a.main(P5,P6,P7)
    
btn_4 = Button(window, text="Agrupar", padx=10,command=agrupar)
btn_4.grid(column=0, row=5)

def extraer(): 
    # Llama al script caracteristicas.py
    e.main()
    # Habilita boton Extraer caracteristicas
    btn_6['state'] = 'normal'
btn_5 = Button(window, text="Extraer características", padx=10,command=extraer)
btn_5.grid(column=0, row=6)


def entrenar(): 
    # Llama al script entrenar.py
    t.main()
    # Habilita boton predecir
    btn_7['state'] = 'normal'
btn_6 = Button(window, text="Entrenar clasificador", padx=10,command=entrenar)
btn_6.grid(column=0, row=7)

def predecir(): 
    # Llama al script predecir.py
    p.main()
btn_7 = Button(window, text="Predecir", padx=10,command=predecir)
btn_7.grid(column=0, row=8)


def close_window(): 
    if CONEXION:
        messagebox.showwarning(message="Antes de salir debe desconectar",title=WINDOW_TITLE) 
    else:
        p= messagebox.askyesno(message="¿Está seguro de que desea salir?",title=WINDOW_TITLE) 
        if p:
            window.destroy()
        


btn_8 = Button(window, text="Salir", padx=10,command=close_window)
btn_8.grid(column=0, row=9)

# =============================================================================
# COLUMNA 1
# =============================================================================

lbl_3 = Label(window, text="Parámetros")
lbl_3.grid(column=1, row=1)

lbl_4 = Label(window, text="Interacciones:")
lbl_4.grid(column=1, row=2)

lbl_5 = Label(window, text="Cerca:")
lbl_5.grid(column=1, row=3)
lbl_6 = Label(window, text="Media:")
lbl_6.grid(column=1, row=4)
lbl_7 = Label(window, text="Lejos:")
lbl_7.grid(column=1, row=5)
lbl_7 = Label(window, text="MinPuntos:")
lbl_7.grid(column=1, row=6)
lbl_7 = Label(window, text="MaxPuntos:")
lbl_7.grid(column=1, row=7)
lbl_7 = Label(window, text="UmbralDistancia:")
lbl_7.grid(column=1, row=8)


def cambiar():
    global P1,P2,P3,P4,P5,P6,P7
    P1=txt_0.get()
    P2=txt_1.get()
    P3=txt_2.get()
    P4=txt_3.get()
    P5=txt_4.get()
    P6=txt_5.get()
    P7=txt_6.get()
    print("""PARAMETROS
          Interaciones:{}
          Cerca:{}
          Media:{}
          Lejos:{}
          MinPuntos:{}
          MaxPuntos:{}
          UmbralDistancia:{}
          """.format(P1,P2,P3,P4,P5,P6,P7))
    

btn_9 = Button(window, text="Cambiar", padx=10,command=cambiar)
btn_9.grid(column=1, row=9)


# =============================================================================
# COLUMNA 2
# =============================================================================
txt_0 = Entry(window,width=8)
txt_0.insert(0, P1)
txt_0.grid(column=2, row=2)
txt_1 = Entry(window,width=8)
txt_1.insert(0, P2)
txt_1.grid(column=2, row=3)
txt_2 = Entry(window,width=8)
txt_2.insert(0, P3)
txt_2.grid(column=2, row=4)
txt_3 = Entry(window,width=8)
txt_3.insert(0, P4)
txt_3.grid(column=2, row=5)
txt_4 = Entry(window,width=8)
txt_4.insert(0, P5)
txt_4.grid(column=2, row=6)
txt_5 = Entry(window,width=8)
txt_5.insert(0, P6)
txt_5.grid(column=2, row=7)
txt_6 = Entry(window,width=8)
txt_6.insert(0, P7)
txt_6.grid(column=2, row=8)
# =============================================================================
# COLUMNA 3
# =============================================================================
lbl_11 = Label(window, text="Fichero para la captura")
lbl_11.grid(column=3, row=1)


items = (
            "positivo1/enPieCerca.json",
            "positivo2/enPieMedia.json",
            "positivo3/enPieLejos.json",
            "positivo4/sentadoCerca.json",
            "positivo5/sentadoMedia.json",
            "positivo6/sentadoLejos.json",
            "negativo1/cilindroMenorCerca.json",
            "negativo2/cilindroMenorMedia.json",
            "negativo3/cilindroMenorLejos.json",
            "negativo4/cilindroMayorCerca.json",
            "negativo5/cilindroMayorMedia.json",
            "negativo6/cilindroMayorLejos.json",
        )
list = Listbox(window, width=35, height=12)
list.insert(0, *items)
list.grid(column=3,row=3,rowspan=6)


window.mainloop()


        
        