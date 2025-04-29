from ListaReproduccion import ListaCircularDoble
from NodoCancion import NodoCancion
import tkinter as tk
from tkinter import ttk
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


# Funciones sobre el funcionamiento de la UI.
def mostrarReproductor():
    frameInicio.pack_forget()
    frameReproductor.pack(pady=20)
    actualizarInfoCancion()

def mostrarCancionesIngresadas():
    frameInicio.pack_forget()

def mostrarListaCanciones():
    ventanaLista = tk.Toplevel(ventana)
    ventanaLista.title("Lista Completa de Canciones")
    ventanaLista.geometry("900x600")
    
    framePrincipal = tk.Frame(ventanaLista)
    framePrincipal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    frameControladores = tk.Frame(framePrincipal)
    frameControladores.pack(fill=tk.X, pady=(0, 10))
    
    tk.Button(frameControladores, text="Cerrar", command=ventanaLista.destroy).pack(side=tk.RIGHT)
    
    tree = ttk.Treeview(
        framePrincipal,
        columns=('nombre', 'artista', 'duracion', 'acciones'),
        show='headings',
        selectmode='browse'
    )
    
    tree.heading('nombre', text='Canción')
    tree.heading('artista', text='Artista')
    tree.heading('duracion', text='Duración')
    tree.heading('acciones', text='Acciones')
    
    tree.column('nombre', width=250)
    tree.column('artista', width=200)
    tree.column('duracion', width=100)
    tree.column('acciones', width=100)
    
    scrollbar = ttk.Scrollbar(framePrincipal, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)
    
    itemANodo = {}
    
    if listaReproduccion.inicio:
        nodo = listaReproduccion.inicio
        while True:
            cancion = nodo.dato
            item = tree.insert('', tk.END,
                             values=(cancion.nombreCancion, 
                                     cancion.artista, 
                                     cancion.duracion,
                                     "Eliminar"))
            itemANodo[item] = nodo
            nodo = nodo.siguiente
            if nodo == listaReproduccion.inicio:
                break
    
    def eliminarCancion():
        seleccionado = tree.focus()
        if seleccionado:
            nodo = itemANodo[seleccionado]
            
            if listaReproduccion.actual == nodo:
                pygame.mixer.music.stop()
                listaReproduccion.actual = None
            
            listaReproduccion.eliminar(nodo)
            
            tree.delete(seleccionado)
            del itemANodo[seleccionado]
            
            etiquetaEstado.config(text=f"Canción eliminada: {nodo.dato.nombreCancion}")
    
    def reproducirSeleccion(event):
        seleccionado = tree.focus()
        if seleccionado:
            nodo = itemANodo[seleccionado]
            listaReproduccion.actual = nodo
            reproducirCancion()
    
    btn_eliminar = tk.Button(
        frameControladores,
        text="Eliminar Selección",
        command=eliminarCancion,
        bg='#dc3545',
        fg='white'
    )
    btn_eliminar.pack(side=tk.LEFT)
    
    tree.bind('<Double-1>', reproducirSeleccion)
    
    ventanaLista.update_idletasks()
    ancho = ventanaLista.winfo_width()
    alto = ventanaLista.winfo_height()
    x = (ventanaLista.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventanaLista.winfo_screenheight() // 2) - (alto // 2)
    ventanaLista.geometry(f'+{x}+{y}')

def regresarInicio():
    frameReproductor.pack_forget()
    frameAcercaDe.pack_forget()
    frameInicio.pack(pady=20)

def mostrarAcercaDe():
    frameInicio.pack_forget()
    frameAcercaDe.pack(pady=20)

# Funciones sobre el funcioamiento del reproductor.

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

# Frame Inicio
frameInicio = tk.Frame(ventana)
tk.Label(frameInicio, text="Reproductor de música", font=('Arial', 14)).pack(pady=20)

tk.Button(frameInicio, text="Cargar Canciones", command=cargarCanciones, width=20).pack(pady=10)
tk.Button(frameInicio, text="Ir al Reproductor", command=mostrarReproductor, width=20).pack(pady=10)
tk.Button(frameInicio, text="Canciones en el repertorio", command=mostrarListaCanciones, width=20).pack(pady=10)
tk.Button(frameInicio, text="Acerca de", command=mostrarAcercaDe, width=20).pack(pady=10)
etiquetaEstado = tk.Label(frameInicio, text="")
etiquetaEstado.pack(pady=10)


# Frame Reproductor
frameReproductor = tk.Frame(ventana)
etiquetaCancion = tk.Label(frameReproductor, text="No hay canción seleccionada", font=('Arial', 12), justify=tk.LEFT)
etiquetaCancion.pack(pady=20)

frameControles = tk.Frame(frameReproductor)
frameControles.pack(pady=15)

tk.Button(frameControles, text="⏮ Anterior", command=cancionAnterior, width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frameControles, text="⏯ Play/Pause", command=pausarCancion, width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frameControles, text="⏭ Siguiente", command=cancionSiguiente, width=12).pack(side=tk.LEFT, padx=5)

tk.Button(frameReproductor, text="Regresar", command=regresarInicio).pack(pady=20)

# Frame Canciones Ingresadas
frameCancionesIngresadas = tk.Frame(ventana)
etiquetaTitulo = tk.Label(frameCancionesIngresadas, text="Estas son las canciones en el repertorio.").pack(pady=10)


# Frame Acerca de
frameAcercaDe = tk.Frame(ventana)
etiquetaAcerca = tk.Label(
    frameAcercaDe, 
    text="Reproductor de música - Estructura de datos.\nVersión 0.6\n"
         "Desarrollado por Rodrigo Gabriel Pérez Vásquez, carnet 1576224\n"
         "Link de repositorio en Github: https://github.com/RodriGab18/Proyecto2EDI"
)
etiquetaAcerca.pack(pady=20)

buttonRegresar = tk.Button(frameAcercaDe, text="Regresar al inicio", command=regresarInicio)
buttonRegresar.pack(pady=10)

frameInicio.pack()
ventana.mainloop()