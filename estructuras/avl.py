r"""
avl.py — Árbol AVL (Árbol Binario de Búsqueda Auto-Balanceado)

Registro de rotaciones:
    - Rotación simple izquierda  (caso derecha-derecha)
    - Rotación simple derecha     (caso izquierda-izquierda)
    - Rotación doble izquierda    (caso izquierda-derecha)
    - Rotación doble derecha      (caso derecha-izquierda)

Uso:
    from estructuras.avl import AVL

    arbol = AVL()
    arbol.insertar(pelicula, clave=lambda p: p.titulo.lower())
    resultado = arbol.buscar("matrix", clave=lambda p: p.titulo.lower())
"""


class NodoAVL:
    """Cada nodo del AVL guarda su dato, hijos, y la altura para calcular el balance."""

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


class AVL:
    """Árbol AVL: árbol binario de búsqueda que se auto-balancea después de cada inserción.

    Regla: para todo nodo, la diferencia de altura entre el subárbol izquierdo
    y el subárbol derecho (factor de balance) debe ser -1, 0 o +1.
    """

    def __init__(self):
        self.raiz = None

    # ==================== UTILIDADES DE ALTURA ====================

    def _altura(self, nodo):
        """Retorna la altura de un nodo. Un nodo None tiene altura 0."""
        if nodo is None:
            return 0
        return nodo.altura

    def _factor_balance(self, nodo):
        """Factor de balance = altura(izquierdo) - altura(derecho)."""
        if nodo is None:
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)

    def _actualizar_altura(self, nodo):
        """Recalcula la altura de un nodo basándose en sus hijos."""
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                              self._altura(nodo.derecho))

    # ==================== ROTACIONES ====================

    def _rotacion_izquierda(self, z):
        """Rotación simple izquierda.

        Caso: el nodo z está desbalanceado hacia la DERECHA (factor < -1)
y su hijo derecho también está pesado a la derecha.

             z                 y
              .               / \
               y      ->      z   T3
              / \
             T2  T3
        """
        y = z.derecho
        T2 = y.izquierdo

        y.izquierdo = z
        z.derecho = T2

        self._actualizar_altura(z)
        self._actualizar_altura(y)

        return y

    def _rotacion_derecha(self, z):
        """Rotación simple derecha.

        Caso: el nodo z está desbalanceado hacia la IZQUIERDA (factor > 1)
y su hijo izquierdo también está pesado a la izquierda.

             z               y
/               / /
           y      ->      T1  z
          / /                  / /
         T1  T2               T2  T3
        """
        y = z.izquierdo
        T2 = y.derecho

        y.derecho = z
        z.izquierdo = T2

        self._actualizar_altura(z)
        self._actualizar_altura(y)

        return y

    def _rotacion_izquierda_derecha(self, nodo):
        """Rotación doble izquierda-derecha.

        Caso: el nodo está desbalanceado hacia la izquierda (factor > 1)
        pero su hijo izquierdo está desbalanceado hacia la derecha.
        """
        nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
        return self._rotacion_derecha(nodo)

    def _rotacion_derecha_izquierda(self, nodo):
        """Rotación doble derecha-izquierda.

        Caso: el nodo está desbalanceado hacia la derecha (factor < -1)
        pero su hijo derecho está desbalanceado hacia la izquierda.
        """
        nodo.derecho = self._rotacion_derecha(nodo.derecho)
        return self._rotacion_izquierda(nodo)

    # ==================== INSERCIÓN ====================

    def insertar(self, dato, clave):
        """Inserta un dato en el AVL manteniendo el balance.

        clave es una función que devuelve el valor de ordenamiento.
        Ejemplo: clave=lambda p: p.titulo.lower()
        """
        self.raiz = self._insertar_recursivo(self.raiz, dato, clave)

    def _insertar_recursivo(self, nodo, dato, clave):
        """Recursión que inserta y luego balancea el camino de vuelta."""
        # Paso 1: inserción estándar como en un BST
        if nodo is None:
            return NodoAVL(dato)

        if clave(dato) < clave(nodo.dato):
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, dato, clave)
        elif clave(dato) > clave(nodo.dato):
            nodo.derecho = self._insertar_recursivo(nodo.derecho, dato, clave)
        else:
            return nodo  # Duplicado, no se inserta

        # Paso 2: actualizar la altura del nodo actual
        self._actualizar_altura(nodo)

        # Paso 3: obtener el factor de balance
        balance = self._factor_balance(nodo)

        # Paso 4: si está desbalanceado, aplicar la rotación correspondiente
        # Caso 1: Izquierda-Izquierda (factor > 1 y el hijo izquierdo está a la izquierda)
        if balance > 1 and clave(dato) < clave(nodo.izquierdo.dato):
            return self._rotacion_derecha(nodo)

        # Caso 2: Derecha-Derecha (factor < -1 y el hijo derecho está a la derecha)
        if balance < -1 and clave(dato) > clave(nodo.derecho.dato):
            return self._rotacion_izquierda(nodo)

        # Caso 3: Izquierda-Derecha (factor > 1 y el hijo izquierdo está a la derecha)
        if balance > 1 and clave(dato) > clave(nodo.izquierdo.dato):
            return self._rotacion_izquierda_derecha(nodo)

        # Caso 4: Derecha-Izquierda (factor < -1 y el hijo derecho está a la izquierda)
        if balance < -1 and clave(dato) < clave(nodo.derecho.dato):
            return self._rotacion_derecha_izquierda(nodo)

        return nodo

    # ==================== BÚSQUEDA ====================

    def buscar(self, valor, clave):
        """Busca un elemento cuyo valor de clave coincide con `valor`.

        Devuelve el dato o None si no existe.
        Complejidad: O(log n) gracias al balance del AVL.
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

    # ==================== RECORRIDOS ====================

    def inorder(self):
        """Izquierda → raíz → derecha. Devuelve elementos ORDENADOS."""
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

    # ==================== INFORMACIÓN ====================

    def altura(self):
        """Retorna la altura del árbol. Árbol vacío → 0."""
        return self._altura(self.raiz)

    def esta_vacio(self):
        return self.raiz is None

    def __len__(self):
        """Cantidad de nodos en el árbol."""
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_nodos(nodo.izquierdo) + self._contar_nodos(nodo.derecho)


# ==================== FUNCIONES DE COMPARACIÓN ====================

def comparar_bst_vs_avl(lista_datos, clave):
    """Compara un BST común con un AVL insertando los mismos datos.

    Retorna un diccionario con las alturas de ambos árboles y
    tiempos de búsqueda para demostrar la diferencia de desbalance.
    """
    import time

    # --- BST común (usa arboles.py) ---
    try:
        from arboles import ArbolBST
    except ImportError:
        try:
            from estructuras.arboles import ArbolBST
        except ImportError:
            return {"error": "No se encontró arboles.py para comparar"}

    bst = ArbolBST()
    for d in lista_datos:
        bst.insertar(d, clave=clave)

    # --- AVL ---
    avl = AVL()
    for d in lista_datos:
        avl.insertar(d, clave=clave)

    # Medir tiempo de búsqueda en ambos
    valor_test = clave(lista_datos[0])

    inicio = time.time()
    for _ in range(1000):
        bst.buscar(valor_test, clave=clave)
    tiempo_bst = (time.time() - inicio) * 1000

    inicio = time.time()
    for _ in range(1000):
        avl.buscar(valor_test, clave=clave)
    tiempo_avl = (time.time() - inicio) * 1000

    return {
        "altura_bst": bst.altura(),
        "altura_avl": avl.altura(),
        "tiempo_bst_ms": tiempo_bst,
        "tiempo_avl_ms": tiempo_avl,
        "mejor_balance": avl.altura() < bst.altura(),
    }


# ==================== EJEMPLO DE USO ====================

if __name__ == "__main__":
    class Elemento:
        def __init__(self, nombre, valor):
            self.nombre = nombre
            self.valor = valor

        def __repr__(self):
            return f"{self.nombre}({self.valor})"

    # Insertar en ORDEN ALFABÉTICO para mostrar el desbalance del BST
    datos = [
        Elemento("A", 1),
        Elemento("B", 2),
        Elemento("C", 3),
        Elemento("D", 4),
        Elemento("E", 5),
        Elemento("F", 6),
        Elemento("G", 7),
        Elemento("H", 8),
        Elemento("I", 9),
        Elemento("J", 10),
    ]

    # AVL
    avl = AVL()
    for d in datos:
        avl.insertar(d, clave=lambda x: x.nombre.lower())

    print("=== AVL con datos ordenados ===")
    print("Altura del AVL:", avl.altura())
    print("Cantidad de nodos:", len(avl))
    print()

    print("--- inorder ---")
    for e in avl.inorder():
        print(" ", e)

    print()
    print("--- preorder (muestra el balance) ---")
    for e in avl.preorder():
        print(" ", e)

    print()
    print("Buscar 'F':", avl.buscar("f", clave=lambda x: x.nombre.lower()))
    print("Buscar 'Z':", avl.buscar("z", clave=lambda x: x.nombre.lower()))

    # Comparar con BST
    print("\n=== Comparación BST vs AVL ===")
    resultado = comparar_bst_vs_avl(datos, clave=lambda x: x.nombre.lower())
    if "error" in resultado:
        print("  ", resultado["error"])
    else:
        print(f"  Altura BST: {resultado['altura_bst']}")
        print(f"  Altura AVL: {resultado['altura_avl']}")
        print(f"  BST es más alto que AVL: {resultado['mejor_balance']}")
