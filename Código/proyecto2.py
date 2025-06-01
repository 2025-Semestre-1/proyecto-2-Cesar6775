#importacion de librerias
from tkinter import *
import random
import time
from tkinter import messagebox
from tkinter import simpledialog

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
puntaje = 0
juego_terminado = False
nombre_jugador = ""

    
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
    canvas.delete("all")
    
    for i in range(filas):
        for j in range(columnas):
            x1 = j * TAM_CELDA + EXTRA
            y1 = i * TAM_CELDA + EXTRA
            x2 = x1 + TAM_CELDA 
            y2 = y1 + TAM_CELDA 
            
            celda = tablero[i][j]
            if celda == "+":
                color = "Black"
            elif celda == "0":
                color = "Gray"
            elif celda == "1":
                color = "blue"
            elif celda == "2":
                color = "Red"
            elif celda == "3":
                color = "White"
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
    canvas.create_text(500, 100, text=f"Puntaje: {puntaje}", font=("Arial", 15), fill="red")
 
 
#funcion de creacion de pieza
 
def generar_pieza():
    global pieza_actual
    global posicion_pieza
    global juego_terminado
    pieza_actual = random.choice(todas_las_piezas)  
    posicion_pieza = [4, 1]
    
    for i in range(len(pieza_actual)):
        for j in range(len(pieza_actual[0])):
            if pieza_actual[i][j] > 0:
                x = posicion_pieza[0] + j
                y = posicion_pieza[1] + i
                if tablero[y][x] != "0":
                    mensaje_game_over()
                    juego_terminado = True
                    return False
    return True

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
                        color = "White"
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
                
##############################################################################################################################

def hay_colision(direccion):
    global posicion_pieza, pieza_actual, tablero
    
    filas_tablero = len(tablero)
    
    for i in range(len(pieza_actual)):
        fila = pieza_actual[i]
        for j in range(len(fila)):
            celda = fila[j]
            if celda > 0:
                x = posicion_pieza[0] + j
                y = posicion_pieza[1] + i
                
                if direccion == "abajo":
                    if y + 1 >= filas_tablero or tablero[y + 1][x] != "0":
                        return True
                
                elif direccion == "izquierda":
                    if x - 1 < 1 or tablero[y][x - 1] != "0":
                        return True
                elif direccion == "derecha":
                    if x + 1 >= len(tablero[0]) - 1 or tablero[y][x + 1] != "0":
                        return True
    return False

def fijar_pieza_en_tablero():
    global posicion_pieza, pieza_actual, tablero
    
    for i in range(len(pieza_actual)):
        fila = pieza_actual[i]
        for j in range(len(fila)):
            celda = fila[j]
            if celda > 0:
                x = posicion_pieza[0] + j
                y = posicion_pieza[1] + i
                tablero[y][x] = str(celda) 

###############################################################################################################################



def eliminar_lineas_completas():
    global tablero
    global puntaje
    lineas_eliminadas = 0
    i = len(tablero) - 2 

    while i > 0:
        j = 1
        linea_completa = True

        while j < len(tablero[i]) - 1:  
            if tablero[i][j] == "0" or tablero[i][j] == "+":
                linea_completa = False
            j += 1

        if linea_completa == True:
            k = i
            while k > 1:
                if "+" not in tablero[k - 1][1:11]:
                    tablero[k] = tablero[k - 1][:]
                else:
                    break
                k -= 1
            nueva_fila = []
            m = 0
            while m < 12:
                if m == 0 or m == 11:
                    nueva_fila.append("+")
                else:
                    nueva_fila.append("0")
                m += 1
            tablero[1] = nueva_fila

            lineas_eliminadas += 1
        else:
            i -= 1
    print (lineas_eliminadas)
    puntaje += lineas_eliminadas * 100
    return lineas_eliminadas

def rotar_pieza(pieza):
    filas = len(pieza)
    columnas = len(pieza[0])

    nueva_pieza = []

    col = 0
    while col < columnas:
        nueva_fila = []
        fila = filas - 1
        while fila >= 0:
            nuevo_valor = pieza[fila][col]
            nueva_fila.append(nuevo_valor)
            fila -= 1
        nueva_pieza.append(nueva_fila)
        col += 1

    return nueva_pieza

def puede_rotar():
    global pieza_actual, posicion_pieza, tablero

    pieza_rotada = rotar_pieza(pieza_actual)

    for i in range(len(pieza_rotada)):
        for j in range(len(pieza_rotada[0])):
            if pieza_rotada[i][j] > 0:
                x = posicion_pieza[0] + j
                y = posicion_pieza[1] + i

                if x < 1 or x >= len(tablero[0]) - 1 or  y >= len(tablero) or tablero[y][x] != "0":
                    return False
    return True 


def mover_pieza_hacia_abajo():
    global posicion_pieza
    global puntaje
    if juego_terminado == True:
        return
    colision = hay_colision("abajo")
    if colision == False:
        posicion_pieza[1] += 1  
        canvas.delete("all")  
        dibujar_tablero(canvas, tablero)  
        dibujar_pieza()
        ventana.after(500, mover_pieza_hacia_abajo)  
    else:
        fijar_pieza_en_tablero()
        eliminar_lineas_completas()
        generar_pieza()
        mover = generar_pieza()
        if mover== True:
            canvas.delete("all")
            dibujar_tablero(canvas, tablero)
            dibujar_pieza()
            if puntaje > 300:
                ventana.after(500, mover_pieza_hacia_abajo)
            elif puntaje > 500:
                ventana.after(400, mover_pieza_hacia_abajo)
            elif puntaje > 700:
                ventana.after(300, mover_pieza_hacia_abajo)
            else:
                ventana.after(200, mover_pieza_hacia_abajo)
            
        
#mover la pieza
def mover_izquierda(event=None):
    global posicion_pieza
    colision = hay_colision("izquierda")
    if colision == False:
        posicion_pieza[0] -= 1
        redibujar()
        
def mover_derecha(event=None):
    global posicion_pieza, pieza_actual
    colision = hay_colision("derecha")
    if colision == False:
        posicion_pieza[0] += 1
        redibujar()
        
def mover_abajo(event=None):
    global posicion_pieza
    global juego_terminado
    if juego_terminado == True:
        return
    colision = hay_colision("abajo")
    if not colision:
        posicion_pieza[1] += 1
    else:
        fijar_pieza_en_tablero()
        eliminar_lineas_completas()
        generar_pieza()
    redibujar()
    
def rotar(event=None):
    global pieza_actual
    
    if puede_rotar():
        pieza_actual = rotar_pieza(pieza_actual)
        redibujar()
        
    
#se redibuja la posicion de la pieza
def redibujar():
    dibujar_tablero(canvas, tablero)
    dibujar_pieza()

def iniciar_juego():
    global puntaje
    global juego_terminado
    global pieza_actual
    global posicion_pieza
    global nombre_jugador
    puntaje = 0
    juego_terminado = False
    pieza_actual = None
    posicion_pieza = [4, 0]
    nombre_jugador = ""
    nuevo_juego() 
    nombre_jugador = simpledialog.askstring("Nuevo juego", "Ingresa tu nombre:")
    if nombre_jugador != None:
        verdadero = generar_pieza()
        if verdadero == True:
            dibujar_pieza()
            mover_pieza_hacia_abajo()
    else:
        messagebox.showwarning("Aviso", "No se inicio el juego porque no se ingreso un nombre")
        
def mensaje_game_over():
    global juego_terminado
    juego_terminado = True
    canvas.delete("all")
    dibujar_tablero(canvas, tablero)
    canvas.create_text(360, 350, text="GAME OVER", fill="red", font=("Arial", 30, "bold"))
##################################################################################
 
#boton de iniciar 
boton_iniciar = Button(ventana, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.place(x=500, y=50)

#teclas de movimiento
ventana.bind("<Left>", mover_izquierda)
ventana.bind("<Right>", mover_derecha)
ventana.bind("<Down>", mover_abajo)
ventana.bind("<Up>", rotar)
    
nuevo_juego()
ventana.mainloop()