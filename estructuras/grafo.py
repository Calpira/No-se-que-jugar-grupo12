from collections import deque
from estructuras.heap import Heap


class Grafo:

    def __init__(self):
        self._adyacencia = {}

    def agregar_nodo(self, nodo):
        if nodo not in self._adyacencia:
            self._adyacencia[nodo] = {}

    def agregar_arista(self, a, b, peso=1.0):
        self.agregar_nodo(a)
        self.agregar_nodo(b)
        self._adyacencia[a][b] = peso
        self._adyacencia[b][a] = peso

    def vecinos(self, nodo):
        return self._adyacencia.get(nodo, {})

    def nodos(self):
        return list(self._adyacencia.keys())

    def __len__(self):
        return len(self._adyacencia)

    def similitud(self, a, b):
        #Devuelve la similitud entre dos nodos (1.0 = idénticos).
        if a in self._adyacencia and b in self._adyacencia[a]:
            return 1.0 - self._adyacencia[a][b]
        return 0.0

    def mas_similares(self, nodo, k=5):
        #Devuelve los k vecinos más similares a `nodo`.

        if nodo not in self._adyacencia:
            return []
        vecinos = sorted(self._adyacencia[nodo].items(), key=lambda x: x[1])
        return [(v, 1.0 - p) for v, p in vecinos[:k]]

    def bfs(self, inicio):
        visitados, cola, orden = set(), deque([inicio]), []
        while cola:
            actual = cola.popleft()
            if actual in visitados:
                continue
            visitados.add(actual)
            orden.append(actual)
            for vecino in self._adyacencia.get(actual, {}):
                if vecino not in visitados:
                    cola.append(vecino)
        return orden

    def dfs(self, inicio):
        visitados, pila, orden = set(), [inicio], []
        while pila:
            actual = pila.pop()
            if actual in visitados:
                continue
            visitados.add(actual)
            orden.append(actual)
            for vecino in self._adyacencia.get(actual, {}):
                if vecino not in visitados:
                    pila.append(vecino)
        return orden

    def dijkstra(self, inicio):
        distancias = {n: float("inf") for n in self._adyacencia}
        predecesores = {n: None for n in self._adyacencia}
        if inicio not in self._adyacencia:
            return distancias, predecesores

        distancias[inicio] = 0.0
        heap = Heap(clave=lambda x: x[0], maximo=False)
        heap.insertar((0.0, inicio))
        visitados = set()

        while not heap.esta_vacio():
            dist, actual = heap.extraer()
            if actual in visitados:
                continue
            visitados.add(actual)
            for vecino, peso in self._adyacencia[actual].items():
                nueva = dist + peso
                if nueva < distancias[vecino]:
                    distancias[vecino] = nueva
                    predecesores[vecino] = actual
                    heap.insertar((nueva, vecino))

        return distancias, predecesores

    def camino_minimo(self, inicio, fin):
        distancias, predecesores = self.dijkstra(inicio)
        if fin not in distancias or distancias[fin] == float("inf"):
            return None, float("inf")
        camino, actual = [], fin
        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]
        camino.reverse()
        return camino, distancias[fin]