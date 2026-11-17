# Entrega Final — Sumario del Proyecto e Integración Completa

## 1. Cumplimiento de la Propuesta Inicial ([00-propuesta.md](./00-propuesta.md))

En la propuesta original se definió el objetivo de resolver la indecisión de un usuario que busca qué jugar sin perder tiempo, planteando funcionalidades clave que fueron cubiertas en su totalidad a lo largo del desarrollo:

- **Búsqueda por palabras clave/tags + Sistema de valoración/ranking:** Resuelto en la **Opción 1** mediante un **Max-Heap**, que calcula el puntaje de coincidencia (`Rating + 10 puntos por cada tag coincidente`) y extrae el Top 10 ordenado.
- **Juegos relacionados (*"si te gustó este, probá este otro"*):** Resuelto en la **Opción 2** combinando un **Árbol AVL** (para localizar el título exacto en $O(\log n)$) y un **Grafo no dirigido** recorrido con **BFS** bajo demanda para recomendar títulos similares.
- **Exploración por categorías:** Resuelto en la **Opción 4** mediante un **Árbol General** que organiza géneros y subgéneros de videojuegos.
- **Recomendación aleatoria (*"¡Sorpréndeme!"*):** Resuelto en la **Opción 3** mediante selección uniforme en tiempo constante $O(1)$ con `random.choice()`.

---

## 2. Evolución de Estructuras por Etapa

| Etapa | Estructura | Problema que resuelve | Dónde se aplica |
| ----- | ---------- | --------------------- | --------------- |
| **TP3** | *Árbol Binario de Búsqueda (BST)* | Primera optimización para buscar por título sin recorrer linealmente todo el catálogo | Reemplazado luego por AVL |
| **TP4** | *Árbol AVL* | Evita el desbalanceo ($O(n)$) al insertar títulos ordenados alfabéticamente, garantizando búsquedas en $O(\log n)$ mediante rotaciones | Opción 2: "Búsqueda por título" |
| **TP5** | *Árbol General* | Modela la jerarquía de géneros y subgéneros (Action, Adventure, RPG, Strategy) | Opción 4: "Explorar categorías" |
| **TP6** | *Max-Heap* | Ordena y extrae el Top 10 de juegos más relevantes según el puntaje de coincidencia con las etiquetas elegidas | Opción 1: "Búsqueda por etiquetas" |
| **TP7 / Final** | *Grafo no dirigido (BFS)* | Conecta juegos como nodos por similitud de etiquetas para recomendar títulos parecidos bajo demanda | Opción 2: "Ver juegos similares" |

---

## 3. Últimas Integraciones en el Menú Principal (`ui/terminal.py`)

Para cerrar el flujo completo de la aplicación, se reorganizaron las opciones del menú principal y se completaron las integraciones pendientes:

### 3.1 Árbol AVL + Grafo en la Opción 2 (Búsqueda por título)
Antes esta opción solo usaba el **Árbol AVL** para buscar el título exacto rápido (O(\log n)). Ahora le sumamos el **Grafo** para recomendar juegos similares:
- **Árbol AVL (O(\log n)):** Funciona como un índice alfabético balanceado que ubica rápidamente el título buscado por el usuario sin recorrer todo el catálogo.
- **Grafo con BFS:** Una vez encontrado el juego base, si el usuario elige ver recomendaciones similares, se arma una red local conectando ese título con otros que comparten etiquetas y se recorren sus vecinos mediante **BFS** para mostrar los más parecidos.


### 3.2 Nueva Opción 3: "¡Sorpréndeme!" (Juego aleatorio)
Se incorporó esta opción para resolver el problema principal de la aplicación cuando el usuario no tiene ningún criterio o filtro definido y quiere delegar por completo la elección:
- Utiliza `random.choice(self.juegos)`, que selecciona un título al azar de la lista cargada en tiempo constante **$O(1)$**, sin agregar sobrecarga al inicio ni durante la ejecución del programa.
