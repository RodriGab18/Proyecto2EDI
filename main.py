from ListaReproduccion import ListaCircularDoble
from NodoCancion import NodoCancion
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font as tkFont
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

# Funciones para diseño de UI

def estiloWindowsXP():
    style = ttk.Style()
    style.theme_use('winnative')  # Usar tema nativo de Windows
    
    estiloBotones = {
        "bg": "#ece9d8",  # Color clásico XP
        "fg": "black",
        "font": ("Tahoma", 8),
        "relief": tk.RAISED,
        "borderwidth": 2,
        "activebackground": "#316ac5",
        "activeforeground": "white"
    }
    
    estiloEtiquetas = {
        "bg": "#ece9d8",
        "fg": "black",
        "font": ("Tahoma", 8)
    }
    
    return estiloBotones, estiloEtiquetas

COLORES = {
    "primary": "#5D1049",     # Morado oscuro
    "secondary": "#E30425",   # Rojo vibrante
    "background": "#F8F9FA",  # Gris claro
    "surface": "#FFFFFF",     # Blanco
    "on_primary": "#FFFFFF",  # Texto sobre primary
    "on_secondary": "#000000",# Texto sobre secondary
    "on_background": "#212529",# Texto principal
    "on_surface": "#212529"   # Texto en superficies
}
def configurar_estilos():
    style = ttk.Style()
    
    # Estilo general
    style.theme_create('musicplayer', parent='clam', settings={
        'TFrame': {
            'configure': {'background': COLORES['background']}
        },
        'TLabel': {
            'configure': {
                'background': COLORES['background'],
                'foreground': COLORES['on_background'],
                'font': ('Segoe UI', 10)
            }
        },
        'TButton': {
            'configure': {
                'background': COLORES['primary'],
                'foreground': COLORES['on_primary'],
                'font': ('Segoe UI', 10, 'bold'),
                'borderwidth': 1,
                'relief': 'raised',
                'padding': (10, 5)
            },
            'map': {
                'background': [
                    ('pressed', COLORES['secondary']),
                    ('active', COLORES['secondary'])
                ],
                'foreground': [
                    ('pressed', COLORES['on_secondary']),
                    ('active', COLORES['on_secondary'])
                ]
            }
        },
        'TProgressbar': {
            'configure': {
                'thickness': 10,
                'troughcolor': COLORES['surface'],
                'background': COLORES['secondary'],
                'lightcolor': COLORES['secondary'],
                'darkcolor': COLORES['secondary']
            }
        }
    })
    style.theme_use('musicplayer')


# Funciones sobre el funcionamiento del reproductor.

def cargarCanciones():
    try:
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de canciones")
        if not carpeta:
            return
        
        canciones_cargadas = 0
        for archivo in os.listdir(carpeta):
            if archivo.endswith('.mp3'):
                ruta = os.path.join(carpeta, archivo)
                try:
                    cancion = obtenerMetadata(ruta)
                    listaReproduccion.agregar(cancion)
                    canciones_cargadas += 1
                except Exception as e:
                    print(f"Error al cargar {archivo}: {str(e)}")
        
        etiquetaEstado.config(text=f"{canciones_cargadas} canciones cargadas")
    except Exception as e:
        etiquetaEstado.config(text=f"Error: {str(e)}")

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

estiloBotones, estiloEtiquetas = estiloWindowsXP()

# Frame Inicio
frameInicio = tk.Frame(ventana, bg="#f0f0f0")
tk.Label(
    frameInicio, 
    text="Reproductor de música", 
    **estiloEtiquetas
).pack(pady=20)

tk.Button(
    frameInicio, 
    text="Cargar Canciones", 
    command=cargarCanciones, 
    width=20,
    **estiloBotones
).pack(pady=10)

tk.Button(
    frameInicio, 
    text="Ir al Reproductor", 
    command=mostrarReproductor, 
    width=20,
    **estiloBotones
).pack(pady=10)

tk.Button(
    frameInicio, 
    text="Canciones en el repertorio", 
    command=mostrarListaCanciones, 
    width=20,
    **estiloBotones
).pack(pady=10)

tk.Button(
    frameInicio, 
    text="Acerca de", 
    command=mostrarAcercaDe, 
    width=20,
    **estiloBotones
).pack(pady=10)

etiquetaEstado = tk.Label(frameInicio, text="", **estiloEtiquetas)
etiquetaEstado.pack(pady=10)

# --- Frame Reproductor ---
frameReproductor = tk.Frame(ventana, bg="#f0f0f0")
etiquetaCancion = tk.Label(
    frameReproductor, 
    text="No hay canción seleccionada", 
    **estiloEtiquetas
)
etiquetaCancion.pack(pady=20)

frameControles = tk.Frame(frameReproductor, bg="#f0f0f0")
frameControles.pack(pady=15)

tk.Button(
    frameControles, 
    text="⏮ Anterior", 
    command=cancionAnterior, 
    width=12,
    **estiloBotones
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frameControles, 
    text="⏯ Play/Pause", 
    command=pausarCancion, 
    width=12,
    **estiloBotones
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frameControles, 
    text="⏭ Siguiente", 
    command=cancionSiguiente, 
    width=12,
    **estiloBotones
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frameReproductor, 
    text="Regresar", 
    command=regresarInicio,
    **estiloBotones
).pack(pady=20)

progress = ttk.Progressbar(
    frameReproductor, 
    orient='horizontal', 
    length=300, 
    mode='determinate'
)
progress.pack(pady=10)

# Etiqueta de tiempo
label_tiempo = ttk.Label(
    frameReproductor,
    text="00:00 / 00:00",
    font=("Tahoma", 8)
)
label_tiempo.pack()

# --- Frame Canciones Ingresadas ---
frameCancionesIngresadas = tk.Frame(ventana, bg="#f0f0f0")
tk.Label(
    frameCancionesIngresadas, 
    text="Estas son las canciones en el repertorio.", 
    **estiloEtiquetas
).pack(pady=10)

# --- Frame Acerca de ---
frameAcercaDe = tk.Frame(ventana, bg="#f0f0f0")
tk.Label(
    frameAcercaDe, 
    text="Reproductor de música - Estructura de datos.\nVersión 0.6.1\n"
         "Desarrollado por Rodrigo Gabriel Pérez Vásquez, carnet 1576224\n"
         "Link de repositorio en Github: https://github.com/RodriGab18/Proyecto2EDI",
    **estiloEtiquetas
).pack(pady=20)

tk.Button(
    frameAcercaDe, 
    text="Regresar al inicio", 
    command=regresarInicio,
    **estiloBotones
).pack(pady=10)

frameInicio.pack()
ventana.mainloop()