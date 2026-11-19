# Requerimientos 

## 1. Requerimientos Funcionales (RF)

* **RF01 — Búsqueda por etiquetas (Ranking Top 10):** El sistema debe permitir ingresar una o más etiquetas (*tags*) separadas por coma y mostrar un Top 10 de videojuegos recomendados, priorizados según un puntaje que combina calificación base y cantidad de coincidencias (`rating + 10 * coincidencias`).
* **RF02 — Búsqueda por título:** El sistema debe permitir buscar un videojuego específico por su título exacto y desplegar su ficha con título, rating y etiquetas asociadas.
* **RF03 — Sugerencia de juegos similares:** Luego de encontrar un videojuego por título, el sistema debe ofrecer la posibilidad de recomendar hasta 5 juegos similares basándose en las etiquetas compartidas.
* **RF04 — Recomendación aleatoria ("¡Sorprendeme!"):** El sistema debe permitir seleccionar y mostrar un videojuego al azar del catálogo cargado.
* **RF05 — Exploración de categorías:** El sistema debe desplegar la jerarquía de géneros principales (`Action`, `Adventure`, `RPG`, `Strategy`) junto con sus subcategorías asociadas.

---

## 2. Requerimientos No Funcionales (RNF)

* **RNF01 — Eficiencia en búsqueda por título:** La búsqueda exacta por título debe resolverse en tiempo logarítmico $O(\log n)$ en el peor caso mediante un árbol binario de búsqueda autobalanceado (`AVL`).
* **RNF02 — Eficiencia en ranking Top 10:** La obtención de los 10 mejores resultados por etiquetas debe resolverse mediante una cola de prioridad (`Heap` máximo), evitando ordenar la totalidad del catálogo en cada consulta.
* **RNF03 — Escalabilidad del catálogo:** El sistema debe soportar la carga y consulta de catálogos de al menos 1.000 videojuegos sin degradación perceptible en los tiempos de respuesta.
* **RNF04 — Usabilidad en consola:** La navegación debe realizarse mediante un menú numérico claro, con validaciones y mensajes informativos ante entradas inválidas o búsquedas sin resultados.
* **RNF05 — Autonomía y persistencia local:** El sistema debe operar íntegramente a partir del archivo local `datos/juegos.csv` sin requerir conexión a internet ni motores de bases de datos externos.

---

## 3. Alcance y Fuera de Alcance

### Dentro del alcance
* Carga del catálogo de videojuegos desde `datos/juegos.csv` en objetos `Juego`.
* Implementación propia en Python de las estructuras de datos fundamentales (`AVL`, `ArbolGeneral`, `Heap`, `Grafo`) y algoritmos de recorrido/búsqueda (`BFS`, `DFS`, `Dijkstra`).
* Interfaz interactiva por línea de comandos (`ui/terminal.py`).

### Fuera del alcance
* **Autenticación y perfiles de usuario:** No se implementa registro, inicio de sesión ni guardado de preferencias o historial por usuario.
* **Conexión a APIs externas:** El sistema no consulta servicios externos (como Steam o IGDB) en tiempo real para actualizar precios, reseñas o lanzamientos.
* **Gestión de bibliotecas o compras:** El sistema funciona exclusivamente como motor de recomendación y consulta, sin enlaces de compra ni descarga.