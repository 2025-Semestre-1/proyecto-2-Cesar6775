from tkinter import *
import random

#
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

#
#ventana principal 
ventana =Tk()
ventana.title("Tetris")
canvas = Canvas(ventana, width=700, height=800, bg='lightgray')
canvas.pack()

TAM_CELDA = 30
EXTRA = 30 
ruta = ""

    
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
    ruta = "base.txt"
    dibujar_tablero(canvas, ruta) 

def cargar_juego():
    print()

def guardar_juego():
    print()

def estadisticas ():
    print ("a Nombre del jugador")
    print ("b Puntaje Obtenido")
    print ("c Mostrar el Ranking o posición con respecto a otros jugadores (Top 10)")


def dibujar_tablero(canvas, ruta):
    global TAM_CELDA
    
    filas = 22
    columnas = 12
    tablero = cargar_tablero(ruta)
    canvas.delete("all")
    
    for i in range(filas):
        for j in range(columnas):
            x1 = j * TAM_CELDA
            y1 = i * TAM_CELDA
            x2 = x1 + TAM_CELDA
            y2 = y1 + TAM_CELDA
            
            celda = tablero[i][j]
            if celda == '+':
                color = "gray30"
            elif celda == '0':
                color = "white"
            else:
                color = "blue"
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    
nuevo_juego()
ventana.mainloop()