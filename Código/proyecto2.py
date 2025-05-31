#importacion de librerias
from tkinter import *
import random
import time

#creacion de piezas
pieza_O = [[1, 1],[1, 1]]

pieza_I = [[2],[2],[2],[2]]

pieza_L = [[3, 0],[3, 0],[3, 3]]

pieza_J = [[0, 4],[0, 4],[4, 4]]

pieza_T = [[5, 5, 5],[0, 5, 0]]

pieza_Z = [[6, 6, 0],[0, 6, 6]]

pieza_U = [[7, 0, 7],[7, 7, 7]]

pieza_mas = [[0, 8, 0],[8, 8, 8],[0, 8, 0]]

todas_las_piezas = [pieza_O, pieza_I, pieza_L, pieza_J, pieza_T, pieza_Z, pieza_U, pieza_mas]


#ventana principal 
ventana =Tk()
ventana.title("Tetris")
canvas = Canvas(ventana, width=700, height=800, bg="lightgray")
canvas.pack()

#funciones globales 
TAM_CELDA = 30
EXTRA = 10 
ruta = ""
pieza_actual = None
posicion_pieza = [4,0]
tablero = []

    
#funciones principales
def cargar_tablero(ruta):
    with open(ruta,"r") as archivo:
        lineas = archivo.readlines()
    tablero = []
    for linea in lineas:
        linea = linea.strip()
        fila = list(linea)
        tablero += [fila]
    return tablero

def nuevo_juego():
    global ruta 
    global tablero
    ruta = "base.txt"
    tablero = cargar_tablero(ruta)
    dibujar_tablero(canvas, tablero)

def cargar_juego():
    print()

def guardar_juego():
    print()

def estadisticas ():
    print ("a Nombre del jugador")
    print ("b Puntaje Obtenido")
    print ("c Mostrar el Ranking o posición con respecto a otros jugadores (Top 10)")


def dibujar_tablero(canvas, tablero):
    global TAM_CELDA
    global EXTRA
    
    filas = 22
    columnas = 12
    #tablero = cargar_tablero(ruta)
    canvas.delete("all")
    
    for i in range(filas):
        for j in range(columnas):
            x1 = j * TAM_CELDA + EXTRA
            y1 = i * TAM_CELDA + EXTRA
            x2 = x1 + TAM_CELDA 
            y2 = y1 + TAM_CELDA 
            
            celda = tablero[i][j]
            if celda == "+":
                color = "gray"
            elif celda == "0":
                color = "white"
            elif celda == "1":
                color = "blue"
            elif celda == "2":
                color = "Red"
            elif celda == "3":
                color = "Black"
            elif celda == "4":
                color = "Green"
            elif celda == "5":
                color = "Orange"
            elif celda == "6":
                color = "Purple"
            elif celda == "7":
                color = "Brown"
            else:
                color = "Yellow"
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
 
 
#funcion de creacion de pieza
 
def generar_pieza():
    global pieza_actual
    global posicion_pieza
    pieza_actual = random.choice(todas_las_piezas)  
    posicion_pieza = [4, 0]  

def dibujar_pieza():
    global pieza_actual, posicion_pieza
    if pieza_actual is not None:
        for i in range(len(pieza_actual)):
            fila = pieza_actual[i]
            for j in range(len(fila)):
                celda = fila[j]
                if celda > 0:
                    x1 = (posicion_pieza[0] + j) * TAM_CELDA + EXTRA
                    y1 = (posicion_pieza[1] + i) * TAM_CELDA + EXTRA
                    x2 = x1 + TAM_CELDA
                    y2 = y1 + TAM_CELDA
                    
                    if celda == 1:
                        color = "blue"
                    elif celda == 2:
                        color = "Red"
                    elif celda == 3:
                        color = "Black"
                    elif celda == 4:
                        color = "Green"
                    elif celda == 5:
                        color = "Orange"
                    elif celda == 6:
                        color = "Purple"
                    elif celda == 7:
                        color = "Brown"
                    else:
                        color = "Yellow"
                    
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def mover_pieza_hacia_abajo():
    global posicion_pieza
    posicion_pieza[1] += 1  # Mueve la pieza hacia abajo
    canvas.delete("all")  # Limpia el tablero antes de dibujar
    dibujar_tablero(canvas, tablero)  # Dibuja el tablero
    dibujar_pieza()  # Dibuja la pieza en la nueva posición
    ventana.after(500, mover_pieza_hacia_abajo)  # Llama a la función cada 500ms

#mover la pieza
def mover_izquierda(event=None):
    global posicion_pieza
    posicion_pieza[0] -= 1
    redibujar()

def mover_derecha(event=None):
    global posicion_pieza
    posicion_pieza[0] += 1
    redibujar()

def mover_abajo(event=None):
    global posicion_pieza
    posicion_pieza[1] += 1
    redibujar()
    
#se rebibula la posicion de la pieza
def redibujar():
    dibujar_tablero(canvas, tablero)
    dibujar_pieza()

def iniciar_juego():
    generar_pieza()
    dibujar_pieza()
    mover_pieza_hacia_abajo()  


    
    

 
##################################################################################
 
 
 
#boton de iniciar 
boton_iniciar = Button(ventana, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.place(x=500, y=50)

#teclas de movimiento
ventana.bind("<Left>", mover_izquierda)
ventana.bind("<Right>", mover_derecha)
ventana.bind("<Down>", mover_abajo)
    
nuevo_juego()
ventana.mainloop()