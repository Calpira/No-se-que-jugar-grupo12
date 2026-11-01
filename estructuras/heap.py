class Heap:
    #Cola de prioridad (min-heap por defecto, max-heap si maximo=True).  para obtener los K mejores juegos sin ordenar toda la lista.

    def __init__(self, clave=None, maximo=True):
        self.datos = []
        self.clave = clave if clave is not None else (lambda x: x)
        self.maximo = maximo

    def _tiene_prioridad(self, a, b):
        va, vb = self.clave(a), self.clave(b)
        return va > vb if self.maximo else va < vb

    def insertar(self, elemento):
        self.datos.append(elemento)
        self._subir(len(self.datos) - 1)

    def extraer(self):
        if not self.datos:
            return None
        raiz = self.datos[0]
        ultimo = self.datos.pop()
        if self.datos:
            self.datos[0] = ultimo
            self._bajar(0)
        return raiz

    def ver_raiz(self):
        return self.datos[0] if self.datos else None

    def esta_vacio(self):
        return len(self.datos) == 0

    def __len__(self):
        return len(self.datos)

    def _subir(self, i):
        while i > 0:
            padre = (i - 1) // 2
            if self._tiene_prioridad(self.datos[i], self.datos[padre]):
                self.datos[i], self.datos[padre] = self.datos[padre], self.datos[i]
                i = padre
            else:
                break

    def _bajar(self, i):
        n = len(self.datos)
        while True:
            izq, der, mejor = 2 * i + 1, 2 * i + 2, i
            if izq < n and self._tiene_prioridad(self.datos[izq], self.datos[mejor]):
                mejor = izq
            if der < n and self._tiene_prioridad(self.datos[der], self.datos[mejor]):
                mejor = der
            if mejor == i:
                break
            self.datos[i], self.datos[mejor] = self.datos[mejor], self.datos[i]
            i = mejor