import pygame

class Nodo:
    def __init__(self, dato):
        self.dato = dato  
        self.siguiente = None
        self.anterior = None

class ListaCircularDoble:
    def __init__(self):
        self.inicio = None
        self.fin = None
        self.actual = None
        self.pausado = False  

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo
            self.fin = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            self.actual = self.inicio
        else:
            nuevo.anterior = self.fin
            nuevo.siguiente = self.inicio
            self.fin.siguiente = nuevo
            self.inicio.anterior = nuevo
            self.fin = nuevo

    def siguienteCancion(self):
        if self.actual:
            self.actual = self.actual.siguiente
            self.reproducir()
            return self.actual.dato
        return None
    
    def cancionAnterior(self):
        if self.actual:
            self.actual = self.actual.anterior
            self.reproducir()
            return self.actual.dato
        return None
    
    def reproducir(self):
        if self.actual:
            pygame.mixer.music.load(self.actual.dato)
            pygame.mixer.music.play()
            self.pausado = False
            return True
        return False