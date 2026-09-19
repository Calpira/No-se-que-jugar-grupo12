
class NodoArbol:
    """Cada caja del árbol. Tiene UN dato y hasta DOS hijos."""
    def __init__(self, dato):
        self.dato = dato # el elemento (ej: la película)
        self.izquierdo = None # hijo menor (va hacia la izquierda)
        self.derecho = None # hijo mayor (va hacia la derecha)

class ArbolBST:
    """Árbol Binario de Búsqueda ordenado por clave del elemento."""
    def __init__(self):
        self.raiz = None
# ---------- INSERTAR ----------

    def insertar(self, dato, clave):
        """Agrega un elemento. `clave` es una función que devuelve el valor
        por el que se ordena (ej: lambda p: p.titulo.lower())."""
        if self.raiz is None:
            self.raiz = NodoArbol(dato)
        else:
            self._insertar_recursivo(self.raiz, dato, clave)

    def _insertar_recursivo(self, nodo, dato, clave):
        if clave(dato) < clave(nodo.dato):
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(dato)
            else:
                self._insertar_recursivo(nodo.izquierdo, dato, clave)
        else:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(dato)
            else:
                self._insertar_recursivo(nodo.derecho, dato, clave)

# ---------- BUSCAR ----------

    def buscar(self, valor, clave):
        """Busca por valor. Devuelve el elemento o None si no existe."""
        return self._buscar_recursivo(self.raiz, valor, clave)

    def _buscar_recursivo(self, nodo, valor, clave):
        if nodo is None:
            return None
        if valor == clave(nodo.dato):
            return nodo.dato
        if valor < clave(nodo.dato):
            return self._buscar_recursivo(nodo.izquierdo, valor, clave)
        return self._buscar_recursivo(nodo.derecho, valor, clave)


# ---------- RECORRIDOS ----------

    def inorder(self):
        """Izquierda → raíz → derecha. Devuelve los elementos ORDENADOS."""
        resultado = []
        self._inorder_recursivo(self.raiz, resultado)
        return resultado

    def _inorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorder_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._inorder_recursivo(nodo.derecho, resultado)

    def preorder(self):
        """Raíz → izquierda → derecha."""
        resultado = []
        self._preorder_recursivo(self.raiz, resultado)
        return resultado

    def _preorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.dato)
            self._preorder_recursivo(nodo.izquierdo, resultado)
            self._preorder_recursivo(nodo.derecho, resultado)

    def postorder(self):
        """Izquierda → derecha → raíz."""
        resultado = []
        self._postorder_recursivo(self.raiz, resultado)
        return resultado

    def _postorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorder_recursivo(nodo.izquierdo, resultado)
            self._postorder_recursivo(nodo.derecho, resultado)
            resultado.append(nodo.dato)

# ---------- EXTRA: mostrar la estructura ----------

    def altura(self):
        """Profundidad máxima del árbol."""
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo): 
        if nodo is None:
            return 0
        return 1 + max(self._altura_recursiva(nodo.izquierdo),
                        self._altura_recursiva(nodo.derecho))