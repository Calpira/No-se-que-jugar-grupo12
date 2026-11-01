import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from estructuras.heap import Heap
from estructuras.grafo import Grafo


JUEGO_ANCLA = None
JUEGO_DESTINO = None

PREFERENCIAS = ["Action", "FPS", "Shooter"]
UMBRAL_SIMILITUD = 0.15    
MAX_JUEGOS_GRAFO = 120    


JUEGOS_DE_RESPALDO = [
    {"titulo": "Counter-Strike", "tags": ["Action", "FPS", "Shooter", "Multiplayer"], "rating": 85.0},
    {"titulo": "Half-Life", "tags": ["Action", "FPS", "Shooter", "Story"], "rating": 90.0},
    {"titulo": "Portal", "tags": ["Adventure", "Puzzle", "Story"], "rating": 95.0},
    {"titulo": "Portal 2", "tags": ["Adventure", "Puzzle", "Story", "Co-op"], "rating": 96.0},
    {"titulo": "Dota 2", "tags": ["Strategy", "MOBA", "Multiplayer"], "rating": 80.0},
    {"titulo": "The Elder Scrolls V: Skyrim", "tags": ["RPG", "Open World", "Adventure"], "rating": 92.0},
    {"titulo": "Stardew Valley", "tags": ["Simulation", "RPG", "Indie"], "rating": 89.0},
    {"titulo": "Hades", "tags": ["Action", "Roguelike", "Indie"], "rating": 93.0},
    {"titulo": "Civilization VI", "tags": ["Strategy", "Turn-Based"], "rating": 85.0},
    {"titulo": "Dark Souls III", "tags": ["Action", "RPG", "Difficult"], "rating": 90.0},
]


def _buscar_columna(filas, candidatos):
    if not filas:
        return None
    claves = list(filas[0].keys())
    for c in candidatos:
        if c in claves:
            return c
    for c in candidatos:
        for k in claves:
            if k.lower() == c.lower():
                return k
    return None


def _normalizar_lista(valor):
    #Convierte una columna del CSV en lista de strings
    if valor is None:
        return []
    if isinstance(valor, (list, tuple, set)):
        return [str(t).strip() for t in valor if str(t).strip()]
    texto = str(valor)
    for sep in [";", "|", ","]:
        if sep in texto:
            return [t.strip() for t in texto.split(sep) if t.strip()]
    return [texto.strip()] if texto.strip() else []


def cargar_juegos(ruta="datos/juegos.csv"):
    #Lee el CSV combinando generos + tags
    if not os.path.isfile(ruta):
        return None
    try:
        with open(ruta, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
    except Exception:
        return None
    if not filas:
        return None

    col_nombre = _buscar_columna(filas, ["Name", "title", "titulo", "nombre"])
    col_generos = _buscar_columna(filas, ["Genres", "generos", "genres"])
    col_tags = _buscar_columna(filas, ["Tags", "tags", "etiquetas"])
    col_rating = _buscar_columna(filas, ["Rating", "rating", "score", "puntaje"])

    if not col_nombre:
        return None

    juegos, vistos = [], set()
    for fila in filas:
        titulo = (fila.get(col_nombre) or "").strip()
        if not titulo or titulo in vistos:
            continue
        vistos.add(titulo)

        tags = []
        if col_generos:
            for t in _normalizar_lista(fila.get(col_generos)):
                if t not in tags:
                    tags.append(t)
        if col_tags:
            for t in _normalizar_lista(fila.get(col_tags)):
                if t not in tags:
                    tags.append(t)

        try:
            rating = float(fila.get(col_rating) or 0) if col_rating else 0.0
        except ValueError:
            rating = 0.0

        juegos.append({"titulo": titulo, "tags": tags, "rating": rating})
    return juegos or None


def similitud(j1, j2):
    t1 = {t.lower() for t in j1["tags"]}
    t2 = {t.lower() for t in j2["tags"]}
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)


def puntaje_para_usuario(juego, preferencias):
    prefs = {p.lower() for p in preferencias}
    tags = {t.lower() for t in juego["tags"]}
    coincidencias = len(tags & prefs)
    return juego["rating"] + 10.0 * coincidencias


def demo_heap(juegos, preferencias):
    print("=" * 60)
    print("DEMO HEAP — ranking por preferencias")
    print(f"Preferencias: {preferencias}")
    print("=" * 60)

    heap = Heap(clave=lambda j: puntaje_para_usuario(j, preferencias), maximo=True)
    for j in juegos:
        heap.insertar(j)

    print(f"Juegos cargados en el Heap: {len(heap)}")
    print("\nTop 5 recomendados:")
    for i in range(5):
        j = heap.extraer()
        if j is None:
            break
        print(f"  {i + 1}. {j['titulo']:<40} score={puntaje_para_usuario(j, preferencias):.1f}  tags={j['tags']}")


def construir_grafo(juegos, umbral):
    g = Grafo()
    for j in juegos:
        g.agregar_nodo(j["titulo"])
    for i in range(len(juegos)):
        for k in range(i + 1, len(juegos)):
            s = similitud(juegos[i], juegos[k])
            if s >= umbral:
                peso = max(1e-6, 1.0 - s)  # peso bajo más similares
                g.agregar_arista(juegos[i]["titulo"], juegos[k]["titulo"], peso)
    return g


def demo_grafo(juegos, ancla=None, destino=None):
    print("\n" + "=" * 60)
    print("DEMO GRAFO — similitud entre juegos")
    print("=" * 60)

    sub = juegos[:MAX_JUEGOS_GRAFO]
    g = construir_grafo(sub, UMBRAL_SIMILITUD)
    print(f"Nodos: {len(g)}   Aristas: {sum(len(g.vecinos(n)) for n in g.nodos()) // 2}")

    if len(g) == 0:
        print("No se generaron aristas con el umbral actual.")
        return

    nodos = g.nodos()
    if ancla is None or ancla not in nodos:
        ancla = nodos[0]

    print(f"\nNodo ancla: {ancla}")
    print(f"Vecinos directos ({len(g.vecinos(ancla))}): {list(g.vecinos(ancla).keys())[:8]}")

    orden_bfs = g.bfs(ancla)
    print(f"\nBFS desde '{ancla}' — primeros 10: {orden_bfs[:10]}")

    orden_dfs = g.dfs(ancla)
    print(f"DFS desde '{ancla}' — primeros 10: {orden_dfs[:10]}")

    print(f"\nTop 5 más similares a '{ancla}' (caso de uso 'ver juegos similares'):")
    for titulo, sim in g.mas_similares(ancla, k=5):
        print(f"  - {titulo:<40} similitud={sim:.3f}")

    distancias, _ = g.dijkstra(ancla)
    alcanzables = {n: d for n, d in distancias.items() if d != float("inf") and n != ancla}
    if not alcanzables:
        print("\nNo hay otros nodos alcanzables.")
        return

    if destino is None or destino not in alcanzables:
        destino = max(alcanzables, key=alcanzables.get)

    camino, costo = g.camino_minimo(ancla, destino)
    print(f"\nCamino mínimo '{ancla}' -> '{destino}'")
    print(f"  Camino: {' -> '.join(camino)}")
    print(f"  Costo total: {costo:.4f}")


def main():
    ancla = sys.argv[1] if len(sys.argv) > 1 else JUEGO_ANCLA
    destino = sys.argv[2] if len(sys.argv) > 2 else JUEGO_DESTINO

    juegos = cargar_juegos()
    if juegos is None:
        print("No se pudo leer datos/juegos.csv — usando juegos de respaldo.")
        juegos = JUEGOS_DE_RESPALDO
    else:
        print(f"Dataset cargado: {len(juegos)} juegos desde datos/juegos.csv")

    demo_heap(juegos, PREFERENCIAS)
    demo_grafo(juegos, ancla, destino)


if __name__ == "__main__":
    main()