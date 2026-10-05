# Análisis TP4 + TP5 — AVL y Árbol General

## 1. ¿Qué resolvimos?

En esta etapa incorporamos dos **estructuras de datos** que resuelven problemas distintos dentro del
sistema:

| Estructura | Problema que resuelve  | Dónde se usa |
| :--- | :---: | ---: |
|**AVL**  | Que las búsquedas por título/clave sean siempre rápidas (O(logn)) incluso cuando los datos se insertan en orden | Opción "Busqueda por titulo" del menú|
| **Árbol General** | Representar la jerarquía de categorías del dominio |Opción "Explorar categorías" del menú (x) |

---

## 2. TP4 — Árbol AVL

### 2.1 ¿Por qué AVL y no un BST común?

Un BST común se desbalancea cuando se insertan datos ordenados (ej: títulos en orden alfabético). Esto lo
convierte en una lista enlazada con complejidad O(n) por búsqueda. El AVL resuelve esto con **rotaciones automáticas** que mantienen la altura en O(log n) sin importar el orden de inserción.

### 2.2 Rotaciones implementadas

| Tipo | Caso | Cuándo se aplica |
| :---                | :---:         | ---: |
| Rotación simple derecha          | Izquierda-Izquierda | Factor de balance > 1 y el nuevo dato va a la izquierda del hijo izquierdo    |
| Rotación simple izquierda        | Derecha-Derecha     | Factor de balance < -1 y el nuevo dato va a la derecha del hijo derecho       |
| Rotación doble izquierda-derecha | Izquierda-Derecha   | Factor de balance > 1 pero el hijo izquierdo está desbalanceado a la derecha  |
| Rotación doble derecha-izquierda | Derecha-Izquierda   | Factor de balance < -1 pero el hijo derecho está desbalanceado a la izquierda |

### 2.3 Casos de desbalance generados

Insertamos datos **en orden alfabético** (escenario que rompe un BST común) y demostramos que el AVL
mantiene la altura controlada. 

**Datos de prueba:**

```
Prueba 1: A, B, C, D, E, F, G, H, I, J (10 elementos en orden)
Prueba 2: títulos de juegos del catálogo ordenados alfabéticamente
```

### 2.4 Comparación BST vs AVL

Salida de [medir_tiempos_avl.py](/algoritmos/medir_tiempos_avl.py) :

| Métrica | BST común | AVL |
|:---| :---:   | ---: |
|Altura con datos ordenados| 900 | 10 |
|Búsqueda con 900 datos ordenados |0.5294 ms|0.0029 ms|
|Complejidad peor caso búsqueda|O(n) |O(log n)|
|Complejidad promedio inserción| O(log n) | O(log n)|

>(Con 1000 datos ordenados el BST da `RecursionError`)

![Tiempos y error con datos ordenados](/assets/medir_tiempos_avl.jpg)

> **Justificación:** Insertar 10 elementos ordenados genera un BST con altura 10 (una cadena), mientras el AVL tiene altura 4 como máximo. La diferencia se amplifica con datasets grandes.

### 2.5 Prueba del AVL

Salida de [estructuras/avl.py](/estructuras/avl.py) :

```
=== AVL con datos ordenados ===
Altura del AVL: 4
Cantidad de nodos: 10

--- inorder ---
  A(1)
  B(2)
  C(3)
  D(4)
  E(5)
  F(6)
  G(7)
  H(8)
  I(9)
  J(10)

--- preorder (muestra el balance) ---
  D(4)
  B(2)
  A(1)
  C(3)
  H(8)
  F(6)
  E(5)
  G(7)
  I(9)
  J(10)

Buscar 'F': F(6)
Buscar 'Z': None

=== Comparación BST vs AVL ===
  Altura BST: 10
  Altura AVL: 4
  BST es más alto que AVL: True
```
![Salida de la prueba del AVL](/assets/avl.jpg)

### 2.6 Código del AVL

Archivo: [estructuras/avl.py](/estructuras/avl.py)

*  NodoAVL: nodo con dato, hijos y altura.
*  AVL: árbol con inserción balanceada, búsqueda y recorridos.
*  Rotaciones: _rotacion_izquierda, _rotacion_derecha, _rotacion_izquierda_derecha, _rotacion_derecha_izquierda.
*  comparar_bst_vs_avl: arma un BST y un AVL con los mismos datos y compara sus alturas.

---

## 3. TP5 — Árbol General (N-ario)     ---a partir de aca     

### 3.1 ¿Qué es un árbol general?
A diferencia del árbol binario donde cada nodo tiene máximo 2 hijos, un **árbol general** permite que cada
nodo tenga **cualquier cantidad de hijos**. Esto lo hace ideal para representar jerarquías naturales.

### 3.2 Jerarquía elegida del dominio

[Describir la jerarquía elegida, ej:]

```
Películas
├── Ciencia Ficción
│ ├── Cyberpunk
│ ├── Viajes temporales
│ └── Inteligencia artificial
├── Acción
│ ├── Superhéroes
│ └── Guerra
└── Comedia
├── Comedia romántica
└── Comedia negra
```

**¿Por qué esta jerarquía?**
* Los géneros son una clasificación natural del dominio.
* Permite al usuario explorar categorías jerárquicas.
* Se conecta con el árbol AVL: el AVL busca por título, el árbol general organiza por categoría.

### 3.3 Recorridos implementados

|Recorrido |Descripción| Complejidad|
|:---|:---:|---:|
|Amplitud (BFS) |Nivel por nivel, de arriba hacia abajo| O(n)|
|Profundidad preorder| Nodo → hijos (izquierda a derecha)| O(n) |
|Profundidad postorder| Hijos → nodo |O(n)|

### 3.4 Prueba del árbol general

Salida de python estructuras/arbol_general.py:
[PEGAR AQUÍ LA SALIDA COMPLETA]

### 3.5 Código del árbol general

Archivo: estructuras/arbol_general.py
* NodoGeneral: nodo con dato y lista de hijos.
* ArbolGeneral: árbol con inserción, búsqueda y recorridos.
* Métodos: insertar_raiz, agregar_hijo, buscar, amplitud, profundidad_preorder,
profundidad_postorder.

---

## 4. Integración con la aplicación

### 4.1 ¿Dónde queda cada estructura?
```
┌─────────────────────────────────────────────┐
│ Interfaz de terminal                        │
├──────────────┬──────────────┬───────────────┤
│ Opción 1:    │ Opción 2:    │ Opción 3:     │
│ Buscar       │ Explorar     │ Ver Top 10    │
│              │ categorías   │               │
│ usa: AVL     │ usa:         │               │
│              │ Árbol Gen.   │               │
└──────────────┴──────────────┴───────────────┘
```

### 4.2 Código de integración en main.py

**Import:**

```
from estructuras.avl import AVL
from estructuras.arbol_general import ArbolGeneral
```

**Inicialización:**
```
avl = AVL()
arbol_categorias = ArbolGeneral()
# (cargar el árbol de categorías con la jerarquía del dominio)
```

**Opción "Buscar":**
```
resultado = avl.buscar(titulo.lower(), clave=lambda e: e.titulo.lower())
```
**Opción "Explorar categorías":**
```
print("Categorías por amplitud:")
for categoria in arbol_categorias.amplitud():
print(f" - {categoria}")
```

---

## 5. Análisis de complejidad

|Operación | AVL | Árbol General |
|:---|:---:|---:|
|Inserción |O(log n) |O(1) (agregar hijo a un nodo conocido)|
|Búsqueda| O(log n)| O(n) (recorrido completo)|
|Recorrido inorder  | O(n)| O(n)|
|Recorrido amplitud     | O(n) |O(n)|
|Altura (peor caso)| O(log n)| O(n) (árbol degenerado)|



***¿Por qué el AVL es O(log n)?***

El AVL mantiene el factor de balance entre -1 y +1 en cada nodo. Esto garantiza que la altura siempre sea
proporcional a log₂(n). Un árbol con 1000 nodos tiene altura máxima ~10, vs ~1000 en un BST
degenerado.

***¿Por qué el árbol general no se auto-balancea?*** 

El árbol general no necesita balanceo porque no tiene criterio de ordenamiento. Su estructura refleja una
jerarquía natural, no un orden numérico o alfabético. El costo de búsqueda O(n) es aceptable porque la
cantidad de categorías suele ser pequeña (decenas, no miles).

---

## 6. Conclusión

* **El AVL** garantiza búsquedas eficientes sin importar el orden de inserción, resolviendo el problema
principal de desbalance del BST.
* **El árbol general** permite organizar el dominio en jerarquías significativas que mejoran la
experiencia del usuario al explorar categorías.
* Ambas estructuras se complementan: el AVL resuelve búsqueda eficiente por clave, el árbol general
organiza la navegación por categorías.
* Ninguna de las dos se usó "por cumplir": el AVL resuelve un problema real (desbalance) y el árbol
general resuelve otro (jerarquización del dominio).

---

## 7. Errores o dudas que tuvimos

[Si tuvieron algún problema y cómo lo resolvieron. Suma puntos mostrarlo.]
[Describir si hubo problemas con las rotaciones, imports, integración, etc.]

---

## 8. Datos y evidencia

* Script de prueba del AVL: [estructuras/avl.py](/estructuras/avl.py) (prueba con letras, sección 2.5) y [algoritmos/medir_tiempos_avl.py](/algoritmos/medir_tiempos_avl.py) (tabla con juegos, sección 2.4)
* Script de prueba del árbol general: (pendiente: TP5)
* Capturas de la terminal: [avl.jpg](/assets/avl.jpg) (sección 2.5) y [medir_tiempos_avl.jpg](/assets/medir_tiempos_avl.jpg) (sección 2.4)