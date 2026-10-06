from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL
from estructuras.arbol_general import ArbolGeneral
from modelos.juego import Juego
import csv
import random


def cargar_datos():
    juegos = []
    with open("datos/juegos.csv", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            nombre = fila["Name"].strip() if fila["Name"] else ""
            if not nombre:
                continue

            generos = [t.strip() for t in fila["Genres"].split(",") if t.strip()]
            tags_extra = [t.strip() for t in fila["Tags"].split(",") if t.strip()]

            tags = []
            for t in generos + tags_extra:
                if t not in tags:
                    tags.append(t)

            try:
                rating = float(fila["Rating"])
            except (ValueError, KeyError):
                rating = 0.0

            juegos.append(Juego(nombre, tags, rating))
    return juegos


class Buscador:
    def __init__(self):
        print("Buscador e indices inicializados.")

    def realizar_busqueda(self, categorias, juegos):
        for j in juegos:
            for cat in categorias:
                for tag in j.tags:
                    if cat.lower() in tag.lower():
                        print(j)


class Menu:
    def __init__(self):
        self.buscador = Buscador()
        self.juegos = cargar_datos()
        #borramos el shuffle porque con el avl se soluciona el problema del orden alfabetico

        self.arbol = AVL()
        for elemento in self.juegos:
            self.arbol.insertar(elemento, clave=lambda e: e.titulo.lower())

        self.categorias = ArbolGeneral()
        self.categorias.insertar_raiz("Videojuegos")

        accion = self.categorias.agregar_hijo(self.categorias.raiz, "Action")
        aventura = self.categorias.agregar_hijo(self.categorias.raiz, "Adventure")
        rpg = self.categorias.agregar_hijo(self.categorias.raiz, "RPG")
        estrategia = self.categorias.agregar_hijo(self.categorias.raiz, "Strategy")

        self.categorias.agregar_hijo(accion, "FPS")
        self.categorias.agregar_hijo(accion, "Shooter")
        self.categorias.agregar_hijo(accion, "Platformer")

        self.categorias.agregar_hijo(aventura, "Puzzle")
        self.categorias.agregar_hijo(aventura, "Horror")
        self.categorias.agregar_hijo(aventura, "Point & Click")

        self.categorias.agregar_hijo(rpg, "JRPG")
        self.categorias.agregar_hijo(rpg, "Open World")

        self.categorias.agregar_hijo(estrategia, "RTS")
        self.categorias.agregar_hijo(estrategia, "Turn-Based Strategy")

        self.estado = 0

        self.opciones_principal = {
            1: "Búsqueda por etiquetas",
            2: "Busqueda por titulo",
            3: "Quiénes somos",
            4: "Cómo evaluamos los puntajes?",
            5: "Explorar categorías",
            6: "Salir del Programa"
        }

    def mostrar_principal(self):
        print()
        print("=== NO SÉ QUÉ JUGAR ===")
        for clave, texto in self.opciones_principal.items():
            print(f"{clave}) {texto}")

    def ejecutar_busqueda(self):
        categorias_input = input("Ingresá tags separados por coma: ")
        categorias = categorias_input.split(",")
        for i in range(len(categorias)):
            categorias[i] = categorias[i].strip()
        self.buscador.realizar_busqueda(categorias, self.juegos)

    def ejecutar_busqueda_arbol(self):
            titulo = input("inserte titulo para buscar: ").strip()
            resultado = self.arbol.buscar(titulo.lower(), clave=lambda e: e.titulo.lower())
            if resultado:
                print(f"Encontrado: {resultado}")
            else:
                print(f"No se encontró '{titulo}'.")

    def explorar_categorias(self):
        print("\n=== Categorías ===")
        for genero in self.categorias.raiz.hijos:
            print(f"{genero.dato}: {', '.join(self.categorias.listar_hijos(genero))}")    #pendiente ampliar, igualmente es funcional


def main():
    menu = Menu()

    while menu.estado != 6:
        if menu.estado == 0:
            menu.mostrar_principal()
            try:
                opc = int(input("\n> "))
                if opc in menu.opciones_principal:
                    menu.estado = opc
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Por favor, ingresá un número.")

        elif menu.estado == 1:
            menu.ejecutar_busqueda()
            input("(Presioná Enter para volver)")
            menu.estado = 0

        elif menu.estado == 2:
            menu.ejecutar_busqueda_arbol()
            input("(Presioná Enter para volver)")
            menu.estado = 0

        elif menu.estado == 3:
            print('''
    === Quiénes somos ===

    Luciano "Reddaz" Rezoagli
    Ezequiel Armoa
    Carolina "Calpira" Lopez

    Somos estudiantes de la UNAB y este es nuestro
    trabajo practico integrador de la materia
    Estructuras de Datos''')
            input("(Presioná Enter para volver)")
            menu.estado = 0

        elif menu.estado == 4:
            print('''
    === Metodología de Evaluación ===
                            (a desarrollar)
    Tenemos una base de datos con mas de 1000 juegos. 

    Cada juego tiene un puntaje en base al grado de similitud
    con las categorías / juegos que el usuario elige.''')
            input("(Presioná Enter para volver)")
            menu.estado = 0

#todavia no cumple una funcion real, solo decorativo (pero funciona)

        elif menu.estado == 5:
            menu.explorar_categorias()
            input("(Presioná Enter para volver)")
            menu.estado = 0

    print("Gracias por usar nuestro programa.")

if __name__ == "__main__":
    main()
