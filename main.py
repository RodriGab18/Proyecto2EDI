import tkinter as tk
import pygame
import time

def mostrar_acerca_de():
    frame_inicio.pack_forget()
    frame_acerca_de.pack(pady=20)

def regresar_inicio():
    frame_acerca_de.pack_forget()
    frame_inicio.pack(pady=20)

ventana = tk.Tk()
ventana.title("Reproductor de música")
ventana.geometry("800x600")

frame_inicio = tk.Frame(ventana)
etiqueta = tk.Label(frame_inicio, text="¡Bienvenido, seleccione la opción que requiera!.")
etiqueta.pack(pady=20)

button_cargar = tk.Button(frame_inicio, text="Cargar canciones a la lista de reproducción")
button_cargar.pack(pady=10)

button_mostrar = tk.Button(frame_inicio, text="Mostrar canciones agregadas")
button_mostrar.pack(pady=10)

button_acerca = tk.Button(frame_inicio, text="Acerca de", command=mostrar_acerca_de)
button_acerca.pack(pady=10)

frame_acerca_de = tk.Frame(ventana)
etiqueta_acerca = tk.Label(frame_acerca_de, text="Reproductor de música - Estructura de datos.\nVersión 0.4\nDesarrollado por Rodrigo Gabriel Pérez Vásquez, carnet 1576224\nLink de repositorio en Github: https://github.com/RodriGab18/Proyecto2EDI")
etiqueta_acerca.pack(pady=20)

button_regresar = tk.Button(frame_acerca_de, text="Regresar al inicio", command=regresar_inicio)
button_regresar.pack(pady=10)

frame_inicio.pack(pady=20)

ventana.mainloop()