import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import pygame
from mutagen import File
import os
from ListaReproduccion import ListaCircularDoble
from NodoCancion import NodoCancion

pygame.mixer.init()

class ReproductorMusica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Reproductor de Música")
        self.ventana.geometry("800x600")
        self.listaDeReproduccion = ListaCircularDoble()
        self.cancionActual = None
        
        self.crearWidgets()
        self.mostrarPantallaCarga()
    
    def crearWidgets(self):
        self.pantallaCarga = tk.Frame(self.ventana)
        tk.Label(self.pantallaCarga, text="Inicializando reproductor", font=('Arial', 14)).pack(pady=20)
        tk.Label(self.pantallaCarga, text="Cargando...", font=('Arial', 12)).pack(pady=10)
        
        self.frame_inicio = tk.Frame(self.ventana)
        tk.Label(self.frame_inicio, text="¡Bienvenido, seleccione la opción que requiera!", 
                font=('Arial', 14)).pack(pady=20)
        
        ttk.Button(self.frame_inicio, text="Cargar canciones", 
                  command=self.cargarCanciones).pack(pady=10, fill=tk.X, padx=50)
        ttk.Button(self.frame_inicio, text="Mostrar canciones agregadas", 
                  command=self.mostrarCancionesAgregadas).pack(pady=10, fill=tk.X, padx=50)
        ttk.Button(self.frame_inicio, text="Acerca de", 
                  command=self.mostrarAcercaDe).pack(pady=10, fill=tk.X, padx=50)
        
        self.frame_canciones = tk.Frame(self.ventana)
        self.label_canciones = tk.Label(self.frame_canciones, text="Canciones agregadas:", font=('Arial', 14))
        self.label_canciones.pack(pady=10)
        
        self.canvas = tk.Canvas(self.frame_canciones)
        self.scrollbar = ttk.Scrollbar(self.frame_canciones, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        frame_controles = tk.Frame(self.frame_canciones)
        
        ttk.Button(frame_controles, text="Anterior", 
                  command=self.cancion_anterior).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Reproducir", 
                  command=self.reproducir).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Pausar", 
                  command=self.pausar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Detener", 
                  command=self.detener).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Siguiente", 
                  command=self.cancion_siguiente).pack(side=tk.LEFT, padx=5)
        
        frame_controles.pack(pady=10)

        self.volumen = tk.DoubleVar(value=0.7)  # Volumen inicial 70%
        ttk.Scale(self.frame_canciones, from_=0, to=1, variable=self.volumen,
                 command=self.ajustar_volumen, orient=tk.HORIZONTAL,
                 length=200).pack(pady=5)
        tk.Label(self.frame_canciones, text="Volumen").pack()
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        frame_controles = tk.Frame(self.frame_canciones)
        ttk.Button(frame_controles, text="Reproducir", command=self.reproducir).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Pausar", command=self.pausar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Detener", command=self.detener).pack(side=tk.LEFT, padx=5)
        frame_controles.pack(pady=10)
        
        ttk.Button(self.frame_canciones, text="Regresar al inicio", 
                  command=self.mostrarInicio).pack(pady=10)
        
        self.frame_acerca = tk.Frame(self.ventana)
        tk.Label(self.frame_acerca, 
                text="Reproductor de música - Estructura de datos\n\n"
                     "Versión 0.5\n\n"
                     "Desarrollado por:\n"
                     "Rodrigo Gabriel Pérez Vásquez\n"
                     "Carnet 1576224", 
                font=('Arial', 12), justify=tk.LEFT).pack(pady=20)
        
        ttk.Button(self.frame_acerca, text="Ir al repositorio en GitHub", 
                  command=self.abrir_repositorio).pack(pady=10)
        ttk.Button(self.frame_acerca, text="Regresar al inicio", 
                  command=self.mostrarInicio).pack(pady=10)
    
    def mostrarPantallaCarga(self):
        self.ocultarTodosFrames()
        self.pantallaCarga.pack(fill=tk.BOTH, expand=True)
        self.ventana.after(2000, self.mostrarInicio)
    
    def mostrarInicio(self):
        self.ocultarTodosFrames()
        self.frame_inicio.pack(fill=tk.BOTH, expand=True)
    
    def mostrarCancionesAgregadas(self):
        self.ocultarTodosFrames()
        self.frame_canciones.pack(fill=tk.BOTH, expand=True)
        self.actualizar_lista_canciones()
    
    def mostrarAcercaDe(self):
        self.ocultarTodosFrames()
        self.frame_acerca.pack(fill=tk.BOTH, expand=True)
    
    def ocultarTodosFrames(self):
        for frame in [self.pantallaCarga, self.frame_inicio, 
                     self.frame_canciones, self.frame_acerca]:
            frame.pack_forget()
    
    def cargarCanciones(self):
        archivos = filedialog.askopenfilenames(
            title="Seleccione canciones",
            filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg"), ("Todos los archivos", "*.*")]
        )
        
        if archivos:
            self.lista_reproduccion = ListaCircularDoble()
            
            for archivo in archivos:
                nombre, artista, duracion = self.extraer_info_cancion(archivo)
                cancion = {
                    'ruta': archivo,
                    'nombre': nombre,
                    'artista': artista,
                    'duracion': duracion
                }
                self.lista_reproduccion.agregar(cancion)
            
            messagebox.showinfo("Éxito", f"Se agregaron {len(archivos)} canciones")
            self.actualizar_lista_canciones()
            
            if self.lista_reproduccion.inicio:
                self.lista_reproduccion.actual = self.lista_reproduccion.inicio
                self.cancion_actual = self.lista_reproduccion.actual.dato
    
    def actualizar_lista_canciones(self):
        # Limpiar el frame de canciones
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Agregar las canciones de la lista circular doble
        if self.listaCanciones.inicio is not None:
            actual = self.listaCanciones.inicio
            while True:
                cancion = actual.dato
                tk.Label(self.scrollable_frame, 
                        text=f"{cancion.nombreCancion} - {cancion.artista} ({cancion.duracion})",
                        font=('Arial', 10)).pack(anchor='w', pady=2)
                actual = actual.siguiente
                if actual == self.listaCanciones.inicio:
                    break
    
    def extraer_info_cancion(self, ruta):
        try:
            audio = File(ruta)
            if audio is None or not audio.tags:
                nombre = os.path.basename(ruta)
                artista = "Artista Desconocido"
                duracion = 0
            else:
                nombre = audio.tags.get('title', [os.path.basename(ruta)])[0]
                artista = audio.tags.get('artist', ['Artista Desconocido'])[0]
                duracion = audio.info.length  

            minutos = int(duracion // 60)
            segundos = int(duracion % 60)
            duracion_formateada = f"{minutos:02}:{segundos:02}"

            return nombre, artista, duracion_formateada
        except Exception as e:
            print(f"Error al procesar el archivo {ruta}: {e}")
            return os.path.basename(ruta), "Artista Desconocido", "00:00"
    
    def reproducir(self):
        pass
    
    def pausar(self):
        pass
    
    def detener(self):
        pass
    
    def abrir_repositorio(self):
        webbrowser.open("https://github.com/RodriGab18/Proyecto2EDI")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReproductorMusica(root)
    root.mainloop()