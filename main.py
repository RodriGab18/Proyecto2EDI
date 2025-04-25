from ListaReproduccion import ListaCircularDoble
from NodoCancion import NodoCancion
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import os

# Lógica sobre reproducción

def obtenerMetadata(ruta):
    """Extrae metadatos de archivos MP3 usando mutagen."""
    try:
        audio = MP3(ruta)
        nombre = os.path.splitext(os.path.basename(ruta))[0]
        artista = audio.get('TPE1', ['Desconocido'])[0]
        duracion = str(int(audio.info.length // 60)) + ":" + str(int(audio.info.length % 60)).zfill(2)
        return NodoCancion(nombre, artista, duracion, ruta)
    except:
        return NodoCancion(os.path.basename(ruta), "Desconocido", "0:00", ruta)

pygame.init()
pygame.mixer.init()
listaReproduccion = ListaCircularDoble()

def mostrarReproductor():
    frameInicio.pack_forget()
    frameReproductor.pack(pady=20)
    actualizarInfoCancion()

def regresarInicio():
    frameReproductor.pack_forget()
    frameAcercaDe.pack_forget()
    frameInicio.pack(pady=20)

def cargarCanciones():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta de canciones")
    if not carpeta:
        return
    
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.mp3'):
            ruta = os.path.join(carpeta, archivo)
            cancion = obtenerMetadata(ruta)
            listaReproduccion.agregar(cancion)
    
    etiquetaEstado.config(text=f"{len(os.listdir(carpeta))} canciones cargadas")

def actualizarInfoCancion():
    if listaReproduccion.actual:
        cancion = listaReproduccion.actual.dato
        texto = f"{cancion.nombreCancion}\nArtista: {cancion.artista}\nDuración: {cancion.duracion}"
        etiquetaCancion.config(text=texto)

def reproducirCancion():
    if listaReproduccion.actual:
        pygame.mixer.music.load(listaReproduccion.actual.dato.rutaArchivo)
        pygame.mixer.music.play()
        actualizarInfoCancion()

def pausarCancion():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def cancionAnterior():
    if listaReproduccion.actual:
        listaReproduccion.actual = listaReproduccion.actual.anterior
        reproducirCancion()

def cancionSiguiente():
    if listaReproduccion.actual:
        listaReproduccion.actual = listaReproduccion.actual.siguiente
        reproducirCancion()






# Interfaz gráfica del reproductor

ventana = tk.Tk()
ventana.title("Reproductor de Música Avanzado")
ventana.geometry("900x600")

frameInicio = tk.Frame(ventana)
tk.Label(frameInicio, text="Reproductor Musical", font=('Arial', 14)).pack(pady=20)

tk.Button(frameInicio, text="Cargar Canciones", command=cargarCanciones, width=20).pack(pady=10)
tk.Button(frameInicio, text="Ir al Reproductor", command=mostrarReproductor, width=20).pack(pady=10)
etiquetaEstado = tk.Label(frameInicio, text="")
etiquetaEstado.pack(pady=10)

frameReproductor = tk.Frame(ventana)
etiquetaCancion = tk.Label(frameReproductor, text="No hay canción seleccionada", font=('Arial', 12), justify=tk.LEFT)
etiquetaCancion.pack(pady=20)

frameControles = tk.Frame(frameReproductor)
frameControles.pack(pady=15)

tk.Button(frameControles, text="⏮ Anterior", command=cancionAnterior, width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frameControles, text="⏯ Play/Pause", command=pausarCancion, width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frameControles, text="⏭ Siguiente", command=cancionSiguiente, width=12).pack(side=tk.LEFT, padx=5)

tk.Button(frameReproductor, text="Regresar", command=regresarInicio).pack(pady=20)

frameAcercaDe = tk.Frame(ventana)
etiquetaAcerca = tk.Label(
    frameAcercaDe, 
    text="Reproductor de música - Estructura de datos.\nVersión 0.5.1\n"
         "Desarrollado por Rodrigo Gabriel Pérez Vásquez, carnet 1576224\n"
         "Link de repositorio en Github: https://github.com/RodriGab18/Proyecto2EDI"
)
etiquetaAcerca.pack(pady=20)

buttonRegresar = tk.Button(frameAcercaDe, text="Regresar al inicio", command=regresarInicio)
buttonRegresar.pack(pady=10)

frameInicio.pack()
ventana.mainloop()