import timeit
import time
import bisect
import random
from ui.terminal import cargar_datos
from estructuras.arbol_binario import ArbolBST


def buscar(lista, titulo):
    #Búsqueda secuencial por titulo
    for elemento in lista:
        if elemento.titulo.lower() == titulo.lower():
            return elemento
    return None


def ordenar_por_titulo(lista):
    return sorted(lista, key=lambda e: e.titulo.lower())


def buscar_binaria(lista_ordenada, titulo):
    claves = [e.titulo.lower() for e in lista_ordenada]
    indice = bisect.bisect_left(claves, titulo.lower())
    if indice < len(claves) and claves[indice] == titulo.lower():
        return lista_ordenada[indice]
    return None


def medir_arbol(lista, titulo):
    random.seed(42)
    lista_mezclada = lista.copy()
    random.shuffle(lista_mezclada)
    arbol = ArbolBST()
    for e in lista_mezclada:
        arbol.insertar(e, clave=lambda e: e.titulo.lower())

    inicio = time.time()
    resultado = arbol.buscar(titulo.lower(), clave=lambda e: e.titulo.lower())
    fin = time.time()
    return (fin - inicio) * 1000  


def main() -> None:
    juegos_totales = cargar_datos()
    tamaños = (100, 1_000, 10_000, len(juegos_totales))

    print("tamaño\tsecuencial_ms\tbinaria_ms\tarbol_ms")
    for n in tamaños:
        lista = juegos_totales[:n]
        lista_ordenada = ordenar_por_titulo(lista)
        titulo_prueba = lista[-1].titulo  
        t_sec = min(timeit.repeat(lambda: buscar(lista, titulo_prueba), number=20, repeat=5)) / 20 * 1000
        t_bin = min(timeit.repeat(lambda: buscar_binaria(lista_ordenada, titulo_prueba), number=20, repeat=5)) / 20 * 1000
        t_arb = medir_arbol(lista, titulo_prueba)

        print(f"{n}\t{t_sec:.4f}\t\t{t_bin:.4f}\t\t{t_arb:.4f}")


if __name__ == "__main__":
    main()