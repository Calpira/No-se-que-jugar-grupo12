import timeit
from ui.terminal import cargar_datos
from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL


def ordenar_por_titulo(lista):
    return sorted(lista, key=lambda e: e.titulo.lower())


def armar_arboles(lista):
    bst = ArbolBST()
    avl = AVL()
    for juego in lista:
        bst.insertar(juego, clave=lambda e: e.titulo.lower())
        avl.insertar(juego, clave=lambda e: e.titulo.lower())
    return bst, avl


def main() -> None:
    juegos_totales = cargar_datos()
    ordenados = ordenar_por_titulo(juegos_totales)
    tamaños = (100 / 500 / 900)

    print("tamaño\taltura_bst\taltura_avl\tbst_ms\tavl_ms")
    for n in tamaños:
        lista = ordenados[:n]
        bst, avl = armar_arboles(lista)
        valor = lista[-1].titulo.lower()
        t_bst = min(timeit.repeat(lambda: bst.buscar(valor, clave=lambda e: e.titulo.lower()), number=20, repeat=5)) / 20 * 1000
        t_avl = min(timeit.repeat(lambda: avl.buscar(valor, clave=lambda e: e.titulo.lower()), number=20, repeat=5)) / 20 * 1000

        print(f"{n}\t{bst.altura()}\t\t{avl.altura()}\t\t{t_bst:.4f}\t\t{t_avl:.4f}")


if __name__ == "__main__":
    main()