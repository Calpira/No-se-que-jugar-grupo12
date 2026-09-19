from estructuras.arbol_binario import ArbolBST
from modelos.juego import Juego  #suestra clase


def main():
    arbol = ArbolBST()

    # Lo construimos SIN orden, para que el árbol ordene solo
    datos = [
        Juego("Portal 2", ["Puzzle", "Co-op"], 97.0),
        Juego("Elden Ring", ["Action", "RPG"], 96.0),
        Juego("Hollow Knight", ["Metroidvania", "Action"], 93.0),
        Juego("Celeste", ["Platformer", "Indie"], 94.0),
        Juego("Stardew Valley", ["Simulation", "RPG"], 96.0),
    ]

    for d in datos:
        arbol.insertar(d, clave=lambda e: e.titulo.lower())

    print("Altura del árbol:", arbol.altura())

    print("\n--- inorder (ordenado alfabéticamente) ---")
    for e in arbol.inorder():
        print(" ", e)

    print("\n--- preorder ---")
    for e in arbol.preorder():
        print(" ", e.titulo)

    print("\n--- postorder ---")
    for e in arbol.postorder():
        print(" ", e.titulo)

    print("\n--- búsquedas ---")
    encontrado = arbol.buscar("portal 2", clave=lambda e: e.titulo.lower())
    print("Buscar 'portal 2':", encontrado)

    no_encontrado = arbol.buscar("zzz", clave=lambda e: e.titulo.lower())
    print("Buscar 'zzz':", no_encontrado)


if __name__ == "__main__":
    main()