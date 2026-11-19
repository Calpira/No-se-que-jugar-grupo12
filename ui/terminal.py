from estructuras.heap import Heap
from estructuras.avl import AVL
from estructuras.arbol_general import ArbolGeneral
from modelos.juego import Juego
from estructuras.grafo import Grafo
from algoritmos.traductor import Traductor
import csv
import random


def cargar_datos():
    juegos = []
    with open("datos/Juegos.csv", encoding="utf-8") as f:
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
        # borramos el shuffle porque con el avl se soluciona el problema del orden alfabetico

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
            2: "Búsqueda por título",
            3: "¡Sorprendeme!",
            4: "Explorar categorías",
            5: "Quiénes somos",
            6: "Salir del Programa"
        }

    def mostrar_principal(self):
        print()
        print("=== NO SÉ QUÉ JUGAR ===")
        for clave, texto in self.opciones_principal.items():
            print(f"{clave}) {texto}")

    def ejecutar_busqueda(self):
        categorias_input = input("Ingresá tags separados por coma: ")
        # Limpiamos los tags y pasamos todo a min
        etiquetas_usuario = [c.strip().lower() for c in categorias_input.split(",") if c.strip()]

        if not etiquetas_usuario:
            print("No ingresaste ninguna etiqueta.")
            return

        # Traducimos automáticamente cada etiqueta al inglés
        # No perdemos rendimiento: la traducción es O(k) por k etiquetas,
        # y la búsqueda sigue siendo la operación costosa sobre los 16.000 juegos
        categorias = []
        traducciones = []
        for etiqueta in etiquetas_usuario:
            traducida = Traductor.traducir(etiqueta)
            if traducida and traducida not in categorias:
                categorias.append(traducida)
                if traducida.lower() != etiqueta:
                    traducciones.append(f"{etiqueta} -> {traducida}")

        if traducciones:
            print(f"Etiquetas traducidas: {', '.join(traducciones)}")

        # saca los puntajes más altos primero
        heap = Heap(clave=lambda j: self._calcular_puntaje(j, categorias), maximo=True)

        # buscamos coincidencias y las insertamos en el heap
        for juego in self.juegos:
            if any(cat.lower() in tag.lower() for cat in categorias for tag in juego.tags):
                heap.insertar(juego)

        # mostramos top 10
        if heap.esta_vacio():
            print("No se encontraron juegos con esas etiquetas.")
        else:
            etiquetas_mostradas = ", ".join(categorias)
            print(f"\n--- Top 10 recomendados para {etiquetas_mostradas} ---")
            for i in range(10):
                if heap.esta_vacio():
                    break
                juego = heap.extraer()
                print(f"{i+1}. {juego}")

    def _calcular_puntaje(self, juego, categorias):
        # Le damos 10 puntos por cada tag que coincida, más el rating original del juego
        coincidencias = sum(1 for cat in categorias for tag in juego.tags if cat.lower() in tag.lower())
        return juego.rating + (coincidencias * 10)

    def ejecutar_busqueda_arbol(self):
        titulo = input("Inserte título para buscar: ").strip()
        resultado = self.arbol.buscar(titulo.lower(), clave=lambda e: e.titulo.lower())
        if resultado:
            print(f"Encontrado: {resultado}")
            ver_sim = input("¿Ver juegos similares? (s/n): ").strip().lower()
            if ver_sim == "s":
                grafo = Grafo()
                tags_base = set(resultado.tags)
                candidatos = []
                for juego in self.juegos:
                    if juego.titulo != resultado.titulo:
                        comunes = len(tags_base & set(juego.tags))
                        if comunes > 0:
                            candidatos.append((comunes, juego.rating, juego))

                candidatos.sort(key=lambda x: (x[0], x[1]), reverse=True)

                for comunes, _, juego in candidatos[:15]:
                    grafo.agregar_arista(resultado.titulo, juego.titulo, peso=1 / comunes)

                similares = grafo.bfs(resultado.titulo)[1:6]
                if similares:
                    print(f"\n--- Juegos similares a '{resultado.titulo}' (BFS) ---")
                    for s in similares:
                        print(f"- {s}")
                else:
                    print("No se encontraron juegos similares.")
        else:
            print(f"No se encontró '{titulo}'.")

    def explorar_categorias(self):
        print("\n=== Categorías ===")
        for genero in self.categorias.raiz.hijos:
            print(f"{genero.dato}: {', '.join(self.categorias.listar_hijos(genero))}")

    def ejecutar_juego_aleatorio(self):
        if not self.juegos:
            print("No hay juegos cargados.")
            return
        juego_random = random.choice(self.juegos)
        print("\n=== Sorprendeme! ===")
        print("Hoy te recomendamos jugar a:")
        print(f"{juego_random.titulo} (Rating: {juego_random.rating})")
        print(f"Tags: {', '.join(juego_random.tags)}")


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
            menu.ejecutar_juego_aleatorio()
            input("(Presioná Enter para volver)")
            menu.estado = 0

        elif menu.estado == 4:
            menu.explorar_categorias()
            input("(Presioná Enter para volver)")
            menu.estado = 0

        elif menu.estado == 5:
            print('''
    === Quiénes somos ===

    Luciano "Reddaz" Rezoagli
    Ezequiel Armoa
    Carolina "Calpira" Lopez

    Somos estudiantes de la UNAB y este es nuestro
    trabajo practico integrador de la materia
    Estructuras de Datos

    Este programa incluye un traductor integrado que convierte
    etiquetas en español a categorías en inglés.
    ''')
            input("(Presioná Enter para volver)")
            menu.estado = 0

    print("Gracias por usar nuestro programa.")


if __name__ == "__main__":
    main()
