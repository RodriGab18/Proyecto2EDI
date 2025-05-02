import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import pygame
import os

class WindowsXpPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Música - Windows XP Style")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        
        # Configuración de pygame
        pygame.mixer.init()
        
        # Variables de control
        self.listaReproduccion = []
        self.indiceActual = -1
        self.pausado = False
        
        # Configurar estilo
        self.setupXpStyle()
        
        # Crear interfaz
        self.crearInterfaz()
    
    def setupXpStyle(self):
        """Configura los estilos visuales XP"""
        self.root.configure(bg='#ECE9D8')
        
        self.style = ttk.Style()
        self.style.configure('XP.TFrame', background='#ECE9D8', relief=tk.RAISED, borderwidth=2)
        self.style.configure('XP.TLabelframe', background='#ECE9D8', foreground='#003399', 
                           font=('Tahoma', 10, 'bold'))
        
        self.style.configure('XP.TButton', background='#ECE9D8', foreground='black',
                           font=('Tahoma', 8), borderwidth=1, relief=tk.RAISED)
        self.style.map('XP.TButton',
                      background=[('active', '#316AC5'), ('pressed', '#003399')],
                      foreground=[('active', 'white'), ('pressed', 'white')])
    
    def crearInterfaz(self):
        """Construye la interfaz completa"""
        mainFrame = ttk.Frame(self.root, style='XP.TFrame')
        mainFrame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.crearPanelSuperior(mainFrame)
        self.crearPanelCentral(mainFrame)
        self.crearBarraControles(mainFrame)
    
    def crearPanelSuperior(self, parent):
        """Panel de información de la canción"""
        topFrame = ttk.LabelFrame(parent, text="Reproduciendo", style='XP.TLabelframe')
        topFrame.pack(fill=tk.X, padx=5, pady=5)
        
        # Imagen de álbum
        self.albumArt = tk.Label(topFrame, bg='#D4D0C8', width=100, height=100)
        self.albumArt.pack(side=tk.LEFT, padx=5, pady=5)
        
        infoFrame = ttk.Frame(topFrame, style='XP.TFrame')
        infoFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.lblTitulo = tk.Label(infoFrame, text="Título: ", bg='#ECE9D8', 
                                font=('Tahoma', 10, 'bold'), anchor='w')
        self.lblTitulo.pack(fill=tk.X)
        
        self.lblArtista = tk.Label(infoFrame, text="Artista: ", bg='#ECE9D8',
                                 font=('Tahoma', 9), anchor='w')
        self.lblArtista.pack(fill=tk.X)
        
        self.lblAlbum = tk.Label(infoFrame, text="Álbum: ", bg='#ECE9D8',
                               font=('Tahoma', 9), anchor='w')
        self.lblAlbum.pack(fill=tk.X)
        
        # Barra de progreso
        self.progressBar = ttk.Progressbar(topFrame, orient=tk.HORIZONTAL, 
                                         length=200, mode='determinate')
        self.progressBar.pack(side=tk.RIGHT, padx=10)
    
    def crearPanelCentral(self, parent):
        """Panel con la lista de reproducción"""
        midFrame = ttk.LabelFrame(parent, text="Lista de reproducción", style='XP.TLabelframe')
        midFrame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollY = ttk.Scrollbar(midFrame)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlistTree = ttk.Treeview(midFrame, columns=('titulo', 'artista', 'duracion'),
                                       selectmode='browse', yscrollcommand=scrollY.set)
        
        scrollY.config(command=self.playlistTree.yview)
        
        # Configurar columnas
        self.playlistTree.heading('#0', text='#')
        self.playlistTree.heading('titulo', text='Título')
        self.playlistTree.heading('artista', text='Artista')
        self.playlistTree.heading('duracion', text='Duración')
        
        self.playlistTree.column('#0', width=30, anchor='center')
        self.playlistTree.column('titulo', width=250)
        self.playlistTree.column('artista', width=150)
        self.playlistTree.column('duracion', width=80, anchor='center')
        
        self.playlistTree.pack(fill=tk.BOTH, expand=True)
        self.playlistTree.bind('<Double-1>', self.reproducirSeleccion)
    
    def crearBarraControles(self, parent):
        """Barra de controles de reproducción"""
        ctrlFrame = ttk.Frame(parent, style='XP.TFrame')
        ctrlFrame.pack(fill=tk.X, padx=5, pady=5)
        
        btnStyle = {'style': 'XP.TButton', 'width': 8}
        
        ttk.Button(ctrlFrame, text="Abrir", command=self.cargarCanciones, **btnStyle).pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrlFrame, text="<<", command=self.anterior, **btnStyle).pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrlFrame, text="Play", command=self.playPause, **btnStyle).pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrlFrame, text=">>", command=self.siguiente, **btnStyle).pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrlFrame, text="Stop", command=self.detener, **btnStyle).pack(side=tk.LEFT, padx=2)
        
        # Control de volumen
        volFrame = ttk.Frame(ctrlFrame, style='XP.TFrame')
        volFrame.pack(side=tk.RIGHT, padx=5)
        
        tk.Label(volFrame, text="Volumen:", bg='#ECE9D8').pack(side=tk.LEFT)
        self.volumenSlider = tk.Scale(volFrame, from_=0, to=100, orient=tk.HORIZONTAL,
                                    bg='#ECE9D8', highlightthickness=0)
        self.volumenSlider.set(70)
        self.volumenSlider.pack(side=tk.LEFT)
    
    # Métodos de funcionalidad
    def cargarCanciones(self):
        """Carga archivos MP3"""
        archivos = filedialog.askopenfilenames(filetypes=[("Archivos MP3", "*.mp3")])
        if archivos:
            self.listaReproduccion = list(archivos)
            self.actualizarLista()
    
    def actualizarLista(self):
        """Actualiza la lista de reproducción"""
        self.playlistTree.delete(*self.playlistTree.get_children())
        for i, archivo in enumerate(self.listaReproduccion, 1):
            nombre = os.path.basename(archivo).replace('.mp3', '')
            self.playlistTree.insert('', 'end', text=str(i), values=(nombre, "Desconocido", "--:--"))
    
    def reproducirSeleccion(self, event):
        """Reproduce la canción seleccionada"""
        seleccion = self.playlistTree.selection()
        if seleccion:
            self.indiceActual = int(self.playlistTree.item(seleccion, 'text')) - 1
            self.reproducir()
    
    def reproducir(self):
        """Inicia la reproducción"""
        if 0 <= self.indiceActual < len(self.listaReproduccion):
            pygame.mixer.music.load(self.listaReproduccion[self.indiceActual])
            pygame.mixer.music.play()
            self.actualizarInfo()
    
    def playPause(self):
        """Alterna entre play y pause"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pausado = True
        else:
            if self.pausado:
                pygame.mixer.music.unpause()
                self.pausado = False
            elif self.indiceActual >= 0:
                self.reproducir()
            elif self.listaReproduccion:
                self.indiceActual = 0
                self.reproducir()
    
    def detener(self):
        """Detiene la reproducción"""
        pygame.mixer.music.stop()
        self.pausado = False
    
    def anterior(self):
        """Canción anterior"""
        if self.listaReproduccion:
            self.indiceActual = (self.indiceActual - 1) % len(self.listaReproduccion)
            self.reproducir()
    
    def siguiente(self):
        """Siguiente canción"""
        if self.listaReproduccion:
            self.indiceActual = (self.indiceActual + 1) % len(self.listaReproduccion)
            self.reproducir()
    
    def actualizarInfo(self):
        """Actualiza la información de la canción"""
        if 0 <= self.indiceActual < len(self.listaReproduccion):
            archivo = self.listaReproduccion[self.indiceActual]
            nombre = os.path.basename(archivo).replace('.mp3', '')
            self.lblTitulo.config(text=f"Título: {nombre}")
            self.lblArtista.config(text="Artista: Desconocido")
            self.lblAlbum.config(text="Álbum: Desconocido")

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowsXpPlayer(root)
    
    def onClosing():
        pygame.mixer.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.mainloop()