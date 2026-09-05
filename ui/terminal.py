from modelos.juego import Juego
import json

def cargar_datos():
    with open("datos/juegos.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    juegos = []
    for d in datos:
        juegos.append(Juego(d["titulo"], d["tags"], d["rating"]))
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
    def listar(self, juegos):
        for i in range(len(juegos)):
            print(f"{i + 1}. {juegos[i]}")


class Menu:
    def __init__(self):
        self.buscador = Buscador()
        self.juegos = cargar_datos()
        self.estado = 0

        self.opciones_principal = {
            1: "Realizar una Búsqueda",
            2: "Quiénes somos",
            3: "Cómo evaluamos los puntajes?",
            4: "Listar todos los juegos",
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

        elif menu.estado == 3:
            print('''
    === Metodología de Evaluación ===
                            (a desarrollar)
    Tenemos una base de datos con mas de 1000 juegos. 

    Cada juego tiene un puntaje en base al grado de similitud
    con las categorías / juegos que el usuario elige.''')
            input("(Presioná Enter para volver)")
            menu.estado = 0

        elif menu.estado == 4:
            menu.buscador.listar(menu.juegos)
            input("(Presioná Enter para volver)")
            menu.estado = 0
    print("Gracias por usar nuestro programa.")

if __name__ == "__main__":
    main()
