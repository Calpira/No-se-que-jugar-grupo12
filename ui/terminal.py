from estructuras.arbol_binario import ArbolBST
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
        random.seed(42)
        juegos_mezclados = self.juegos.copy()
        random.shuffle(juegos_mezclados)  #MEzclamos los juegos del cvs porque en orden alfabetico se conflictuaba

        self.arbol = ArbolBST()
        for elemento in juegos_mezclados:
            self.arbol.insertar(elemento, clave=lambda e: e.titulo.lower())

        self.estado = 0

        self.opciones_principal = {
            1: "Búsqueda por etiquetas",
            2: "Busqueda por titulo",
            3: "Quiénes somos",
            4: "Cómo evaluamos los puntajes?",
            5: "Salir del Programa"
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


def main():
    menu = Menu()

    while menu.estado != 5:
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

print("Gracias por usar nuestro programa.")

if __name__ == "__main__":
    main()
