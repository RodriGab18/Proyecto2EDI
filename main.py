from ListaReproduccion import ListaCircularDoble
from NodoCancion import NodoCancion
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import os
import webbrowser
from PIL import Image, ImageTk
import cv2
import numpy as np

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
    for widget in frameCancionesIngresadas.winfo_children():
        widget.destroy()

    tk.Label(
        frameCancionesIngresadas, 
        bg="#f0f0f0"
    ).pack(pady=10)

    frameControladores = tk.Frame(frameCancionesIngresadas)
    frameControladores.pack(fill=tk.X, pady=(0, 10))

    tk.Button(frameControladores, text="Cerrar", command=lambda: limpiarFrame()).pack(side=tk.RIGHT)

    tree = ttk.Treeview(
        frameCancionesIngresadas,
        columns=('nombre', 'artista', 'duracion', 'acciones'),
        show='headings',
        selectmode='browse'
    )
    
    tree.heading('nombre', text='Canción')
    tree.heading('artista', text='Artista')
    tree.heading('duracion', text='Duración')
    tree.heading('acciones', text='Acciones')
    
    tree.column('nombre', width=150)
    tree.column('artista', width=100)
    tree.column('duracion', width=50)
    tree.column('acciones', width=50)
    
    scrollbar = ttk.Scrollbar(frameCancionesIngresadas, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)
    
    itemANodo = {}
    
    if listaReproduccion.inicio:
        nodo = listaReproduccion.inicio
        while True:
            cancion = nodo.dato
            item = tree.insert('', tk.END, values=(cancion.nombreCancion, cancion.artista, cancion.duracion, "Eliminar"))
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

def limpiarFrame():
    for widget in frameCancionesIngresadas.winfo_children():
        widget.destroy()
    tk.Label(frameCancionesIngresadas, bg="#f0f0f0").pack(pady=10)


def regresarInicio():
    frameReproductor.pack_forget()
    frameAcercaDe.pack_forget()
    frameInicio.pack(pady=20)

def mostrarAcercaDe():
    frameInicio.pack_forget()
    frameAcercaDe.pack(pady=20)

def enlaceGit():
    webbrowser.open("https://github.com/RodriGab18/Proyecto2EDI")

# Funciones para diseño de UI


COLORES = {
    "fondo": "#2E0249",       
    "widgets": "#570A57",     
    "texto": "#F806CC",       
    "hover": "#3D0C5A"        
}

class VideoPlayer:
    def __init__(self, parent, video_path):
        self.parent = parent
        self.video_path = video_path
        self.label = tk.Label(parent)
        self.label.pack()
        
        self.cap = cv2.VideoCapture(video_path)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))
        self.update()
    
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            
            self.label.config(image=img_tk)
            self.label.image = img_tk
            self.label.after(self.delay, self.update)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update()
    
    def stop(self):
        self.cap.release()

class TransparentVideoBackground:
    def __init__(self, window, video_path, alpha=0.1):
        self.window = window
        self.alpha = alpha
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video no encontrado: {video_path}")
        
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError("No se pudo abrir el video")
            
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.delay = int(1000/self.fps) if self.fps else 30
        
        self.canvas = tk.Canvas(window, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=False)
        
        self.content_frame = tk.Frame(self.canvas, bg='')
        self.content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.update_video()
        
    def apply_transparency(self, frame):
        """Aplica transparencia al frame del video"""
        img = Image.fromarray(frame)
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        data = np.array(img)
        data[..., 3] = int(255 * self.alpha)  
        return Image.fromarray(data)
    
    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            win_width = self.window.winfo_width()
            win_height = self.window.winfo_height()
            if win_width > 0 and win_height > 0:
                frame = cv2.resize(frame, (win_width, win_height))
            
            transparent_img = self.apply_transparency(frame)
            
            img_tk = ImageTk.PhotoImage(image=transparent_img)
            
            self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
            self.canvas.image = img_tk
            
            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            self.window.after(30, self.update_video)
        else:
            self.cap.release()

    def add_content_widget(self, widget):
        """Añade widgets sobre el video"""
        widget.pack(in_=self.content_frame)
    
# Funciones sobre el funcionamiento del reproductor.

barra_progreso = None
etiqueta_tiempo = None
actualizando_progreso = False

def cargarCanciones():
    try:
        archivos = filedialog.askopenfilenames(
            title="Seleccionar canciones",
            filetypes=[("Archivos MP3", "*.mp3"), ("Todos los archivos", "*.*")]
        )
        
        if not archivos:
            return
        
        canciones_cargadas = 0
        for ruta in archivos:
            try:
                cancion = obtenerMetadata(ruta)
                listaReproduccion.agregar(cancion)
                canciones_cargadas += 1
            except Exception as e:
                print(f"Error al cargar {ruta}: {str(e)}")
        
        etiquetaEstado.config(text=f"{canciones_cargadas} canciones cargadas")
        
        if frameCancionesIngresadas.winfo_ismapped():
            mostrarListaCanciones()
            
    except Exception as e:
        etiquetaEstado.config(text=f"Error: {str(e)}")

def actualizarInfoCancion():
    if listaReproduccion.actual:
        cancion = listaReproduccion.actual.dato
        texto = f"{cancion.nombreCancion}\nArtista: {cancion.artista}\nDuración: {cancion.duracion}"
        etiquetaCancion.config(text=texto)

def reproducirCancion():
    global actualizando_progreso
    
    if listaReproduccion.actual:
        pygame.mixer.music.load(listaReproduccion.actual.dato.rutaArchivo)
        pygame.mixer.music.play()
        actualizarInfoCancion()
        
        barra_progreso['value'] = 0
        if not actualizando_progreso:
            actualizando_progreso = True
            actualizarProgreso()

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

def actualizarProgreso():
    global actualizando_progreso
    
    if pygame.mixer.music.get_busy() and listaReproduccion.actual:
        pos_actual = pygame.mixer.music.get_pos() / 1000  
        
        duracion_total = listaReproduccion.actual.dato.duracion.split(":")
        duracion_total = int(duracion_total[0]) * 60 + int(duracion_total[1])
        
        if duracion_total > 0:
            porcentaje = (pos_actual / duracion_total) * 100
            barra_progreso['value'] = porcentaje
            
            tiempo_actual = f"{int(pos_actual // 60)}:{int(pos_actual % 60):02d}"
            tiempo_total = listaReproduccion.actual.dato.duracion
            etiqueta_tiempo.config(text=f"{tiempo_actual} / {tiempo_total}")
        
        ventana.after(1000, actualizarProgreso)
    else:
        actualizando_progreso = False


# Interfaz gráfica del reproductor

ventana = tk.Tk()
ventana.title("Reproductor de Música")
ventana.geometry("900x600")

# Frame Inicio
frameInicio = tk.Frame(ventana, bg='')
frameInicio.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

video_bg = TransparentVideoBackground(ventana, "C:/Users/rodri/Desktop/Trabajos Uni/3er. Semestre/Estructura de datos/Fondo.mp4", alpha=1)


frameBotones = tk.Frame(
    ventana, 
    bg="#d3d3d3",  
    width=200,     
    padx=10,       
    pady=20        
)
frameBotones.pack_propagate(False) 
frameBotones.pack(side=tk.LEFT, fill=tk.Y)


boton_config = {
    'master': frameBotones,
    'font': ('Arial', 10),  
    'bd': 0,                
    'highlightthickness': 0,
    'anchor': 'w',          
    'width': 18,            
    'pady': 6               
}
botones = [
    ("Cargar Canciones", cargarCanciones),
    ("Ir al Reproductor", mostrarReproductor),
    ("Canciones en el repertorio", mostrarListaCanciones),
    ("Acerca de", mostrarAcercaDe)
]

for texto, comando in botones:
    btn = tk.Button(
        text=texto,
        command=comando,
        fg="black",
        **boton_config
    )
    btn.pack(pady=6, fill=tk.X)

etiquetaEstado = tk.Label(frameBotones, text="")
etiquetaEstado.pack(pady=10)

# --- Frame Reproductor ---
frameReproductor = tk.Frame(ventana, bg="#f0f0f0")
frameReproductor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True) 
etiquetaCancion = tk.Label(
    frameReproductor, 
    text="No hay canción seleccionada", 
)
etiquetaCancion.pack(pady=20)

frameControles = tk.Frame(frameReproductor, bg="#f0f0f0")
frameControles.pack(pady=15)

tk.Button(
    frameControles, 
    text="⏮ Anterior", 
    command=cancionAnterior, 
    width=12,
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frameControles, 
    text="⏯ Play/Pause", 
    command=pausarCancion, 
    width=12,
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frameControles, 
    text="⏭ Siguiente", 
    command=cancionSiguiente, 
    width=12,
).pack(side=tk.LEFT, padx=5)

frameProgreso = tk.Frame(frameReproductor, bg="#f0f0f0")
frameProgreso.pack(pady=(10, 5), padx=20)

barra_progreso = ttk.Progressbar(
    frameProgreso,
    orient='horizontal',
    length=400,
    mode='determinate'
)
barra_progreso.pack(fill=tk.X)

etiqueta_tiempo = tk.Label(
    frameProgreso,
    text="0:00 / 0:00",
    bg="#f0f0f0"
)
etiqueta_tiempo.pack()

tk.Button(
    frameReproductor, 
    text="Regresar", 
    command=regresarInicio,
).pack(pady=20)

# --- Frame Canciones Ingresadas ---
frameCancionesIngresadas = tk.Frame(ventana, bg="#f0f0f0")
frameCancionesIngresadas.pack(side=tk.LEFT, fill=tk.BOTH, expand=False) 
tk.Label(
    frameCancionesIngresadas, 
).pack(pady=10)

# --- Frame Acerca de ---
frameAcercaDe = tk.Frame(ventana, bg="#f0f0f0")
tk.Label(
    frameAcercaDe, 
    text="Reproductor de música - Estructura de datos.\nVersión 1.1.1\n"
         "Desarrollado por Rodrigo Gabriel Pérez Vásquez, carnet 1576224\n"
).pack(pady=20)

tk.Button(frameAcercaDe,
    text="Enlace al repositorio en Github.",
    command=enlaceGit,
          ).pack(pady=10)
tk.Button(
    frameAcercaDe, 
    text="Regresar al inicio", 
    command=regresarInicio,
).pack(pady=10)

frameInicio.pack()
ventana.mainloop()