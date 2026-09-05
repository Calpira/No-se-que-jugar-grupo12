from modelos.juego import Juego
import json
def cargar_datos():
    with open("datos/juegos.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    juegos = []
    for d in datos:
        juegos.append(Juego(d["titulo"], d["rating"], d["tags"] ))
    return juegos

def mostrar_menu():
    
