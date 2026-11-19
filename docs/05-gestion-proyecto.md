# Gestión del Proyecto 

## 1. Herramientas de Gestión y Comunicación

* **Seguimiento de tareas:** Checklist de entregables elaborado a partir de las consignas y guías de trabajos prácticos de la materia (`TP0` a `TP7` y entrega final).
* **Comunicación y coordinación:** Canal y llamadas de voz en **Discord** para división de tareas, revisión de avances y sesiones de programación conjunta.
* **Control de versiones:** Repositorio central en GitHub ([No-se-que-jugar-grupo12](https://github.com/Calpira/No-se-que-jugar-grupo12)), rama `main`.

---

## 2. Metodología de Trabajo

El desarrollo del proyecto se organizó de manera **iterativa e incremental**, avanzando por etapas según los hitos de cada trabajo práctico de la materia:

1. **Armado del checklist:** Al iniciar cada etapa se listaron las tareas concretas a resolver (implementación de cada estructura de datos, integración en `ui/terminal.py` y validación con el dataset `datos/juegos.csv`).
2. **Coordinación por Discord:** La planificación, resolución de errores y pruebas funcionales se coordinaron mediante mensajes y llamadas en Discord.
3. **Integración en GitHub:** A medida que se completaba y probaba cada ítem del checklist, los cambios se integraban en el repositorio principal.

---

## 3. Etapas e Hitos Completados

| Etapa / Hito | Tareas del Checklist Completadas | Archivos Principales | Estado |
| :--- | :--- | :--- | :--- |
| **TP0 / TP1: Base y Catálogo** | Definición del dominio, modelado de la clase `Juego`, carga desde `datos/juegos.csv` y estructura base del menú por consola. | `modelos/juego.py`, `datos/juegos.csv`, `ui/terminal.py`, `main.py` | Completado |
| **TP3 / TP4: Árboles Binarios y AVL** | Implementación de `ArbolBinario` y `AVL` con rotaciones simples y dobles para búsqueda exacta de títulos en $O(\log n)$. | `estructuras/arbol_binario.py`, `estructuras/avl.py` | Completado |
| **TP5: Árbol General** | Implementación de `ArbolGeneral` ($n$-ario) y carga de la jerarquía de géneros y subcategorías de videojuegos. | `estructuras/arbol_general.py`, `ui/terminal.py` | Completado |
| **TP6 / TP7: Heap y Grafo** | Implementación de `Heap` (Max-Heap) para el ranking Top 10 por etiquetas y `Grafo` ponderado con recorrido `BFS` para juegos similares. | `estructuras/heap.py`, `estructuras/grafo.py` | Completado |
| **Entrega Final: Cierre y Documentación** | Ajustes finales de navegación en el menú y redacción de requerimientos, casos de uso, diagramas UML y gestión en `docs/`. | `ui/terminal.py`, `docs/01` a `docs/05`, `README.md` | Completado |

---

## 4. Organización del Equipo (Comisión 3, Grupo 12)

El proyecto fue desarrollado de forma colaborativa por los integrantes del equipo:

* **Luciano "Reddaz" Rezoagli:** 
* **Ezequiel Armoa:** 
* **Carolina "Calpira" Lopez:** 