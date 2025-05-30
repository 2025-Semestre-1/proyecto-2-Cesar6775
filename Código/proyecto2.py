from tkinter import *
import random

#ventana principal 
ventana =Tk()
ventana.title("Tetris")

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
    print ()

def cargar_juego():
    print()

def guardar_juego():
    print()

def estadisticas ():
    print ("a Nombre del jugador")
    print ("b Puntaje Obtenido")
    print ("c Mostrar el Ranking o posición con respecto a otros jugadores (Top 10)")