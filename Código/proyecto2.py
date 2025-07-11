#importacion de librerias
from tkinter import *
import random
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
ruta1 = "base"
pieza_actual = None
posicion_pieza = [4,0]
tablero = []
puntaje = 0
juego_terminado = False
nombre_jugador = ""
contador_juegos = 0

    
#funciones principales
#funcion donde se carga el contenido de tablero desde la ruta de un archivo
def cargar_tablero(ruta):
    with open(ruta,"r") as archivo:
        lineas = archivo.readlines()
    tablero = []
    for linea in lineas:
        linea = linea.strip()
        fila = list(linea)
        tablero += [fila]
    return tablero

#aqui se lee el contenido del tablero 
def nuevo_juego():
    global ruta 
    global tablero
    ruta = f"{ruta1}.txt"
    tablero = cargar_tablero(ruta)
    dibujar_tablero(canvas, tablero)
    
#funcion para gurdar el juego actual, aqui se guarda el tablero, la pieza_actual, la posicion de la pieza, nombre jugador, puntaje que lleva actualmente, y un mensaje para identificar
#donde queda la posicion_pieza y ya el contenido del tablero 
def guardar_juego():
    global contador_juegos
    global tablero
    global posicion_pieza
    global pieza_actual
    global puntaje
    global nombre_jugador
    contador_juegos += 1
    copia = []
    for fila in tablero:
        copia.append(fila[:])
        
    ruta = f"{ruta1}{contador_juegos}.txt"
    with open (ruta,"w") as archivo:
        archivo.write(f"{puntaje}\n")
        archivo.write(f"{nombre_jugador}\n")
        
        for fila in pieza_actual:
            for elemento in fila:
                pieza = ",".join(str(elemento) )
                archivo.write(pieza + "\n")
        archivo.write("FIN_PIEZA\n")
        archivo.write(f"{posicion_pieza[0]},{posicion_pieza[1]}\n")
        for fila in copia:
            archivo.write(''.join(fila) + '\n')
#aqui es donde ya se carga la partida(si es que hay una guardada) se lee todo lo necesario se cargan los datos y se muestran en el canvas, listo para funcionar (creo)            
def cargar_juego():
    global tablero
    global puntaje
    global nombre_jugador
    global posicion_pieza
    global pieza_actual
    try:
        opcion = simpledialog.askstring("Opción", "Elige el número del archivo que quieres cargar:")
        if opcion is None:
            return
        opcion = int(opcion)
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar un valor entero.")
        return

    ruta_archivo = f"{ruta1}{opcion}.txt"
    try:
        with open(ruta_archivo, "r") as archivo:
            lineas1 = archivo.readlines()
            for linea in lineas1:
                lineas += [linea.strip()]

        puntaje = int(lineas[0])
        nombre_jugador = lineas[1]

        pieza_actual = []
        i = 2
        while lineas[i] != "FIN_PIEZA":
            fila = []
            for x in lineas[i].split(","):
                fila.append(int(x))
            pieza_actual.append(fila)
            i += 1
        i += 1
        posicion_pieza = []
        for x in lineas[i].split(","):
            posicion_pieza.append(int(x))
        i += 1
        
        tablero = []
        while i < len(lineas):
            fila = list(lineas[i])
            tablero.append(fila)
            i += 1
        canvas.delete("all")
        dibujar_tablero(canvas, tablero)
        dibujar_pieza()
        mover_pieza_hacia_abajo()
        
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado.")
#aqui es la estadistica dependiendo de la eleccion del usuario 1, 2 o 3 se le muestran diferentes cosas
def estadisticas ():
    global nombre_jugador
    global puntaje
    try:
        opcion = simpledialog.askstring("Opción", "Elige tu opción (1 al 3):\n 1. Ver nombre del jugador\n 2. Ver puntaje del jugador\n 3. Mostrar ranking (top 10)")
        if opcion == None:
            return
        opcion = int(opcion)
        
        if opcion == 1:
            messagebox.showinfo("Nombre del jugador", f"Nombre: {nombre_jugador}")
        elif opcion == 2:
            messagebox.showinfo("Puntaje del jugador", f"Puntaje obtenido: {puntaje}")
        elif opcion == 3:
            try:
                with open("estadisticas.txt", "r") as archivo:
                    jugadores = []
                    for linea in archivo:
                        datos = linea.strip().split(",")
                        nombre = datos[0]
                        try:
                            puntos = int(datos[1])
                            jugadores.append((nombre, puntos))
                        except ValueError:
                            continue  
                    
                    n = len(jugadores)
                    for vuelta in range(n - 1):
                        for indice in range(n - 1 - vuelta):
                            puntaje_actual = jugadores[indice][1]
                            puntaje_siguiente = jugadores[indice + 1][1]
                            if puntaje_actual < puntaje_siguiente:
                                jugadores[indice], jugadores[indice + 1] = jugadores[indice + 1], jugadores[indice]

                    top_10 = jugadores[:10]

                    mensaje = " Top 10 Jugadores \n\n"
                    for i, (nombre, puntos) in enumerate(top_10, 1):
                        mensaje += f"{i}. {nombre} - {puntos} puntos\n"
                    messagebox.showinfo("Top 10", mensaje)

            except FileNotFoundError:
                messagebox.showerror("Error", "No hay estadísticas registradas.")
        else:
            messagebox.showerror("Error", "Opción inválida, solo se admite\n 1 = Ver nombre del jugador\n 2 = Ver puntaje\n 3 = Mostrar ranking (top 10)")
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar un valor de opcion del tipo entero(del 1 al 3)")

#aqui es donde se dibuja el tablero(canvas) para ya representarlo graficamente 
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
    canvas.create_text(532, 250, text=f"Puntaje: {puntaje}", font=("Arial", 12), fill="red")
 
 
#funcion de creacion de pieza
#esta funcion crea una pieza nueva, y guarda su valor
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
                    juego_terminado = True
                    mensaje_game_over()
                    return False
    return True
#con esta funcion representamos la pieza de manera grafica en el codigo 
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
                
#con esta funcion determinamos que los limites del tablero y se obtiene un valor booleano si la pieza choca con algo y tampoco deja que la pieza traspase otras piezas
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
#en esta funcion cuando una pieza no puede seguir cayendo la fijamos en el tablero, para de esta manera poder borrar lineas mas adelante en el codigo
def fijar_pieza_en_tablero():
    global posicion_pieza
    global pieza_actual
    global tablero
    
    for i in range(len(pieza_actual)):
        fila = pieza_actual[i]
        for j in range(len(fila)):
            celda = fila[j]
            if celda > 0:
                x = posicion_pieza[0] + j
                y = posicion_pieza[1] + i
                tablero[y][x] = str(celda) 

#en esta funcion detecta si la fila es eliminable o no, y dependiendo del resultado se elimina la linea, y se bajan las piezas de arriba, pero los obstaculos se mantienen en el mismo lugar
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
    puntaje += lineas_eliminadas * 100
    return lineas_eliminadas
#esta funcion fue la implementada para rotar la pieza, se utiliza con la tecla "up"
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
#en esta funcion se verifica si la tecla puede rotar o no, esta para que no hayan errores inesperados cuando se rote una pieza, funciona de manera que las columnas las vuelve filas 
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

#con esta funcion la pieza cae automaticamente, y tambien aumenta la velocidad de la caida, pero no se nota tanto
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
        mover = generar_pieza()
        if mover== True:
            canvas.delete("all")
            dibujar_tablero(canvas, tablero)
            dibujar_pieza()
            if puntaje < 300:
                ventana.after(500, mover_pieza_hacia_abajo)
            elif puntaje < 500:
                ventana.after(400, mover_pieza_hacia_abajo)
            elif puntaje < 700:
                ventana.after(300, mover_pieza_hacia_abajo)
            else:
                ventana.after(200, mover_pieza_hacia_abajo)
            
        
#mover la pieza hacia la izquierda
def mover_izquierda(event=None):
    global posicion_pieza
    colision = hay_colision("izquierda")
    if colision == False:
        posicion_pieza[0] -= 1
        redibujar()
#mover la pieza hacia la derecha        
def mover_derecha(event=None):
    global posicion_pieza
    global pieza_actual
    colision = hay_colision("derecha")
    if colision == False:
        posicion_pieza[0] += 1
        redibujar()
#mover la pieza hacia abajo de manera manual         
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
#una de las funciones pricipales donde se inicia el nuevo juego, tambien se reinician las funciones globales
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
    if nombre_jugador and nombre_jugador.strip():
        verdadero = generar_pieza()
        if verdadero == True:
            dibujar_pieza()
            mover_pieza_hacia_abajo()
        boton_iniciar.config(state=DISABLED)
    else:
        messagebox.showwarning("Aviso", "No se inicio el juego porque no se ingreso un nombre")
#mensaje donde se muestra "game over" solo que con este tengo un problema aveces muestra el mensaje y aveces no, creo que ya esta bueno, pero aveces no se muestra       
def mensaje_game_over():
    global juego_terminado
    global nombre_jugador
    global puntaje
    juego_terminado = True
    canvas.delete("all")
    dibujar_tablero(canvas, tablero)
    canvas.create_text(360, 350, text="GAME OVER", fill="red", font=("Arial", 30, "bold"))
    with open("estadisticas.txt", "a") as estadisticas:
        estadisticas.write(f"{nombre_jugador},{puntaje}\n")
    boton_iniciar.config(state=NORMAL)
#botones principales 
#boton de iniciar 
boton_iniciar = Button(ventana, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.place(x=500, y=50)
#boton guardar
boton_Guardar = Button(ventana, text="Guardar Juego", command=guardar_juego)
boton_Guardar.place(x=500, y=100)
#boton cargar
boton_Cargar = Button(ventana, text="Cargar Juego", command=cargar_juego)
boton_Cargar.place(x=500, y=150)
#boton estadistica 
boton_estadistica = Button(ventana, text="estadistica", command=estadisticas)
boton_estadistica.place(x=500, y=200)

#teclas de movimiento
ventana.bind("<Left>", mover_izquierda)
ventana.bind("<Right>", mover_derecha)
ventana.bind("<Down>", mover_abajo)
ventana.bind("<Up>", rotar)
    
nuevo_juego()
ventana.mainloop()