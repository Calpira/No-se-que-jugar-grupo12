# Entrega Final — Sumario del Proyecto e Integración Completa

## 1. Cumplimiento de la Propuesta Inicial ([00-propuesta.md](./00-propuesta.md))

En la propuesta original se definió el objetivo de resolver la indecisión de un usuario que busca qué jugar sin perder tiempo, planteando funcionalidades clave que fueron cubiertas en su totalidad a lo largo del desarrollo:

- **Búsqueda por palabras clave/tags + Sistema de valoración/ranking:** Resuelto en la **Opción 1** mediante un **Max-Heap**, que calcula el puntaje de coincidencia (`Rating + 10 puntos por cada tag coincidente`) y extrae el Top 10 ordenado.
- **Juegos relacionados (*"si te gustó este, probá este otro"*):** Resuelto en la **Opción 2** combinando un **Árbol AVL** (para localizar el título exacto en (O(\log n)) y un **Grafo no dirigido** recorrido con **BFS** bajo demanda para recomendar títulos similares.
- **Exploración por categorías:** Resuelto en la **Opción 4** mediante un **Árbol General** que organiza géneros y subgéneros de videojuegos.
- **Recomendación aleatoria (*"¡Sorpréndeme!"*):** Resuelto en la **Opción 3** mediante selección uniforme en tiempo constante O(1) con `random.choice()`.

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
- **Grafo con BFS:** Una vez encontrado el juego base, si el usuario elige ver recomendaciones similares, se filtran los juegos que comparten etiquetas y se ordenan de mayor a menor similitud (cantidad de tags en común y rating) para armar el subgrafo con los 15 mejores candidatos. Luego se recorren sus vecinos mediante **BFS** para mostrar los 5 más parecidos, evitando construir el grafo completo al inicio (O(V2)) y asegurando recomendaciones relevantes en lugar de los primeros títulos del CSV.

### 3.2 Nueva Opción 3: "¡Sorpréndeme!" (Juego aleatorio)
Se incorporó esta opción para resolver el problema principal de la aplicación cuando el usuario no tiene ningún criterio o filtro definido y quiere delegar por completo la elección:
- Utiliza `random.choice(self.juegos)`, que selecciona un título al azar de la lista cargada en tiempo constante **$O(1)$**, sin agregar sobrecarga al inicio ni durante la ejecución del programa.

### 3.3 Traducción automática de etiquetas (dentro de la Opción 1)
Se añadió la funcionalidad de traducción de etiquetas para que el usuario pueda escribir en español y obtener la categoría en inglés:
- El método `Traductor.traducir(etiqueta)` consulta un diccionario interno (`PALABRAS`) que mapea más de 80 etiquetas en español a su categoría en inglés correspondiente.
- **Sin pérdida de rendimiento:** la traducción es una operación de búsqueda en un diccionario en tiempo constante **$O(1)$** por cada etiqueta, mientras que la búsqueda real sobre los 16.679 juegos es la operación costosa. Primero se traducen las etiquetas (rápido), luego se filtran los juegos (costoso).
- Ejemplo: `accion` → `Action`, `cooperativo` → `Co-op`, `tiros` → `Shooter`.
- El costo total es $O(k)$ para $k$ etiquetas, despreciable frente al filtrado sobre los 16.678 juegos.
- Ejemplos: `accion` → `Action`, `cooperativo` → `Co-op`, `tiros` → `Shooter`, `música` → `Soundtrack`.

### 3.4 Sistema de puntaje de la Opción 1
El ranking no es un simple promedio: combina **cobertura de categorías** y **penalización por lo que falta**.

**a) Coincidencias (una sola vez por categoría):**
```python
return sum(
    1.0 for cat in categorias
    if any(cat.lower() in tag.lower() for tag in juego.tags)
)```

### 3.5 Ampliación del catálogo y arreglo de medir_tiempos_avl.py
La prueba `algoritmos/medir_tiempos_avl.py` tenia `/` en donde correspondían comas. Se agregó el `path` para poder realizar la prueba desde **VS Code** sin errores de terminal.
Se actualizó `datos/Juegos.csv`, que quedó en **16.678 títulos**, incorporando lanzamientos recientes (GTA VI, Minecraft, títulos de Riot, Alan Wake II, Overwatch II y la trilogía de Hoyoverse, entre otros). El registro mantiene las columnas `AppID, Name, Genres, Categories, Tags, Rating` y la carga sigue siendo tolerante a filas incompletas: los tags se unifican sin duplicados y un rating inválido se convierte en `0.0`.