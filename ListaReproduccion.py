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

    def eliminar(self, nodo_a_eliminar):
        if self.inicio is None:
            return

        if self.inicio == self.fin == nodo_a_eliminar:
            self.inicio = self.fin = self.actual = None
            return

        nodo_anterior = nodo_a_eliminar.anterior
        nodo_siguiente = nodo_a_eliminar.siguiente

        nodo_anterior.siguiente = nodo_siguiente
        nodo_siguiente.anterior = nodo_anterior

        if nodo_a_eliminar == self.inicio:
            self.inicio = nodo_siguiente
        if nodo_a_eliminar == self.fin:
            self.fin = nodo_anterior

        if nodo_a_eliminar == self.actual:
            self.actual = nodo_siguiente