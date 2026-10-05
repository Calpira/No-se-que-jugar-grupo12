"""
arboles.py — Árbol binario de búsqueda (BST) listo para usar.

Cómo usarlo en tu proyecto:
    1. Copiá este archivo a la carpeta estructuras/ de tu repo.
       O importalo directo:  from arboles import ArbolBST
    2. Creá el árbol.
    3. Insertá los elementos con una CLAVE de ordenamiento
       (por ejemplo, el título en minúsculas).
    4. Buscá con la misma clave.

Ejemplo rápido:
    from arboles import ArbolBST

    arbol = ArbolBST()
    for pelicula in lista_peliculas:
        arbol.insertar(pelicula, clave=lambda p: p.titulo.lower())

    resultado = arbol.buscar("matrix", clave=lambda p: p.titulo.lower())
"""


class NodoArbol:
    """Cada caja del árbol: guarda UN dato y apunta a sus dos hijos."""

    def __init__(self, dato):
        self.dato = dato          # el elemento (ej: la película completa)
        self.izquierdo = None     # hijo menor (izquierda)
        self.derecho = None       # hijo mayor (derecha)


class ArbolBST:
    """Árbol Binario de Búsqueda.

    Regla de ordenamiento: en cada nodo, todo lo menor va a la izquierda
    y todo lo mayor va a la derecha. Para buscar, en cada paso descartamos
    la mitad del árbol → O(log n) promedio.
    """

    def __init__(self):
        self.raiz = None

    # ================= INSERTAR =================
    def insertar(self, dato, clave):
        """Agrega un elemento usando `clave(dato)` para ordenar.

        clave es una función: ej. lambda p: p.titulo.lower()
        """
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
        elif clave(dato) > clave(nodo.dato):
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(dato)
            else:
                self._insertar_recursivo(nodo.derecho, dato, clave)
        # si es IGUAL, se ignora (dato duplicado según la clave)

    # ================= BUSCAR =================
    def buscar(self, valor, clave):
        """Busca el elemento cuyo valor de clave == `valor`.

        Devuelve el elemento o None si no existe.
        """
        return self._buscar_recursivo(self.raiz, valor, clave)

    def _buscar_recursivo(self, nodo, valor, clave):
        if nodo is None:
            return None
        valor_nodo = clave(nodo.dato)
        if valor == valor_nodo:
            return nodo.dato
        if valor < valor_nodo:
            return self._buscar_recursivo(nodo.izquierdo, valor, clave)
        return self._buscar_recursivo(nodo.derecho, valor, clave)

    # ================= RECORRIDOS =================
    def inorder(self):
        """Izquierda → raíz → derecha. Devuelve los elementos ORDENADOS."""
        return self._recorrer(self._inorder_recursivo, self.raiz)

    def preorder(self):
        """Raíz → izquierda → derecha."""
        return self._recorrer(self._preorder_recursivo, self.raiz)

    def postorder(self):
        """Izquierda → derecha → raíz."""
        return self._recorrer(self._postorder_recursivo, self.raiz)

    def _recorrer(self, funcion, nodo):
        resultado = []
        funcion(nodo, resultado)
        return resultado

    def _inorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorder_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._inorder_recursivo(nodo.derecho, resultado)

    def _preorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.dato)
            self._preorder_recursivo(nodo.izquierdo, resultado)
            self._preorder_recursivo(nodo.derecho, resultado)

    def _postorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorder_recursivo(nodo.izquierdo, resultado)
            self._postorder_recursivo(nodo.derecho, resultado)
            resultado.append(nodo.dato)

    # ================= INFORMACIÓN =================
    def altura(self):
        """Profundidad máxima del árbol. Árbol vacío → 0."""
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura_recursiva(nodo.izquierdo),
                       self._altura_recursiva(nodo.derecho))

    def esta_vacio(self):
        return self.raiz is None


if __name__ == "__main__":
    # ============ EJEMPLO DE USO ============
    class Pelicula:
        def __init__(self, titulo, rating):
            self.titulo = titulo
            self.rating = rating

        def __repr__(self):
            return f"{self.titulo} (rating {self.rating})"

    arbol = ArbolBST()
    for pelicula in [
        Pelicula("Matrix", 9.0),
        Pelicula("Inception", 8.8),
        Pelicula("Titanic", 7.8),
        Pelicula("Blade Runner", 8.5),
        Pelicula("Arrival", 8.4),
    ]:
        arbol.insertar(pelicula, clave=lambda p: p.titulo.lower())

    print("Altura del árbol:", arbol.altura())

    print("\n--- inorder (ordenado alfabéticamente) ---")
    for p in arbol.inorder():
        print(" ", p)

    print("\n--- preorder ---")
    for p in arbol.preorder():
        print(" ", p.titulo)

    print("\n--- postorder ---")
    for p in arbol.postorder():
        print(" ", p.titulo)

    print("\n--- búsquedas ---")
    encontrada = arbol.buscar("matrix", clave=lambda p: p.titulo.lower())
    print("Buscar 'matrix':", encontrada)
    inexistente = arbol.buscar("zzz", clave=lambda p: p.titulo.lower())
    print("Buscar 'zzz':", inexistente)