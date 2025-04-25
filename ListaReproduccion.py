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