# Análisis TP4 + TP5 — AVL y Árbol General

## 1. ¿Qué resolvimos?

En esta etapa incorporamos dos **estructuras de datos** que resuelven problemas distintos dentro del
sistema:

| Estructura | Problema que resuelve  | Dónde se usa |
| :--- | :---: | ---: |
|**AVL**  | Que las búsquedas por título/clave sean siempre rápidas (O(logn)) incluso cuando los datos se insertan en orden | Opción "Busqueda por titulo" del menú|
| **Árbol General** | Representar la jerarquía de categorías del dominio |Opción "Explorar categorías" del menú |

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

[Screenshot terminal](/assets/medir_tiempos_avl.jpg)

| Métrica | BST común | AVL |
|:---| :---:   | ---: |
|Altura con datos ordenados| 900 | 10 |
|Búsqueda con 900 datos ordenados |0.5294 ms|0.0029 ms|
|Complejidad peor caso búsqueda|O(n) |O(log n)|
|Complejidad promedio inserción| O(log n) | O(log n)|

>(Con 1000 datos ordenados el BST da `RecursionError`)



> **Justificación:** Insertar 10 elementos ordenados genera un BST con altura 10 (una cadena), mientras el AVL tiene altura 4 como máximo. La diferencia se amplifica con datasets grandes.

### 2.5 Prueba del AVL

Salida de [estructuras/avl.py](/estructuras/avl.py) :

[Screenshot del terminal](/assets/avl.jpg)

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


### 2.6 Código del AVL

Archivo: [estructuras/avl.py](/estructuras/avl.py)

*  NodoAVL: nodo con dato, hijos y altura.
*  AVL: árbol con inserción balanceada, búsqueda y recorridos.
*  Rotaciones: _rotacion_izquierda, _rotacion_derecha, _rotacion_izquierda_derecha, _rotacion_derecha_izquierda.
*  comparar_bst_vs_avl: arma un BST y un AVL con los mismos datos y compara sus alturas.

---

## 3. TP5 — Árbol General (N-ario)    

### 3.1 ¿Qué es un árbol general?
A diferencia del árbol binario donde cada nodo tiene máximo 2 hijos, un **árbol general** permite que cada
nodo tenga **cualquier cantidad de hijos**. Esto lo hace ideal para representar jerarquías naturales.

### 3.2 Jerarquía elegida del dominio

```
Videojuegos
├── Action
│   ├── FPS
│   ├── Shooter
│   └── Platformer
├── Adventure
│   ├── Puzzle
│   ├── Horror
│   └── Point & Click
├── RPG
│   ├── JRPG
│   └── Open World
└── Strategy
    ├── RTS
    └── Turn-Based Strategy
```

**¿Por qué esta jerarquía?**
* Los géneros y tags se eligieron entre los más frecuentes del catálogo de Steam


### 3.3 Recorridos implementados

|Recorrido |Descripción| Complejidad|
|:---|:---:|---:|
|Amplitud (BFS) |Nivel por nivel, de arriba hacia abajo| O(n)|
|Profundidad preorder| Nodo → hijos (izquierda a derecha)| O(n) |
|Profundidad postorder| Hijos → nodo |O(n)|

### 3.4 Prueba del árbol general

[Salida de python (arbol_general.py)](/estructuras/arbol_general.py):

[Screenshot del terminal](/assets/arbol_general.jpg)

```
=== Árbol General de Categorías ===
Raíz: Videojuegos
Altura: 3
Cantidad de nodos: 15

--- Recorrido en amplitud ---
['Videojuegos', 'Action', 'Adventure', 'RPG', 'Strategy', 'FPS', 'Shooter', 'Platformer', 'Puzzle', 'Horror', 'Point & Click', 'JRPG', 'Open World', 'RTS', 'Turn-Based Strategy']

--- Recorrido en profundidad (preorder) ---
['Videojuegos', 'Action', 'FPS', 'Shooter', 'Platformer', 'Adventure', 'Puzzle', 'Horror', 'Point & Click', 'RPG', 'JRPG', 'Open World', 'Strategy', 'RTS', 'Turn-Based Strategy']

--- Recorrido en profundidad (postorder) ---
['FPS', 'Shooter', 'Platformer', 'Action', 'Puzzle', 'Horror', 'Point & Click', 'Adventure', 'JRPG', 'Open World', 'RPG', 'RTS', 'Turn-Based Strategy', 'Strategy', 'Videojuegos']

--- Niveles ---
  Nivel 0: ['Videojuegos']
  Nivel 1: ['Action', 'Adventure', 'RPG', 'Strategy']
  Nivel 2: ['FPS', 'Shooter', 'Platformer', 'Puzzle', 'Horror', 'Point & Click', 'JRPG', 'Open World', 'RTS', 'Turn-Based Strategy']

--- Hijos de 'Action' ---
['FPS', 'Shooter', 'Platformer']

--- Buscar 'FPS' ---
Encontrado: Nodo(FPS)

```



### 3.5 Código del árbol general

Archivo: [estructuras/arbol_general.py](/estructuras/arbol_general.py)

* NodoGeneral: nodo con dato y lista de hijos.
* ArbolGeneral: árbol con inserción, búsqueda y recorridos.
* Métodos: insertar_raiz, agregar_hijo, buscar, amplitud, profundidad_preorder,
profundidad_postorder.

---

## 4. Integración con la aplicación

### 4.1 ¿Dónde queda cada estructura?
```
┌────────────────────────────────────────────────────────────┐
│ Interfaz de terminal                                       │
├─────────────────┬───────────────────┬──────────────────────┤
│ Opción 2:       │ Opción 5:         │ Opciones 1, 3, 4, 6  │
│ Búsqueda por    │ Explorar          │ (lista de juegos,    │
│ título          │ categorías        │ texto y salida)      │
│                 │                   │                      │
│ usa: AVL        │ usa: Árbol        │ no usan árboles      │
│                 │ General           │                      │
└─────────────────┴───────────────────┴──────────────────────┘
```

### 4.2 Código de integración en ui/terminal.py

**Import:**

```
from estructuras.avl import AVL
from estructuras.arbol_general import ArbolGeneral
```

**Inicialización (en `Menu.__init__`):**
```
self.arbol = AVL()
for elemento in self.juegos:
    self.arbol.insertar(elemento, clave=lambda e: e.titulo.lower())

self.categorias = ArbolGeneral()
self.categorias.insertar_raiz("Videojuegos")
accion = self.categorias.agregar_hijo(self.categorias.raiz, "Action")
self.categorias.agregar_hijo(accion, "FPS")
# (y así con el resto de los géneros y tags de la sección 3.2)
```

**Opción 2, "Busqueda por titulo":**
```
resultado = self.arbol.buscar(titulo.lower(), clave=lambda e: e.titulo.lower())
```
**Opción 5, "Explorar categorías":**
```
for genero in self.categorias.raiz.hijos:
    print(f"{genero.dato}: {', '.join(self.categorias.listar_hijos(genero))}")
```

---

## 5. Análisis de complejidad


|Operación | AVL | Árbol General |
|:---|:---:|---:|
|Inserción |O(log n) |O(1) (agregar hijo a un nodo conocido)|
|Búsqueda| O(log n)| O(n) (recorrido completo)|
|Recorrido preorder y postorder | O(n) | O(n)|
|Altura (peor caso)| O(log n)| O(n) (árbol degenerado)|



***¿Por qué el AVL es O(log n)?***

El AVL mantiene el factor de balance entre -1 y +1 en cada nodo. Esto garantiza que la altura siempre sea
proporcional a log₂(n). Un árbol con 1000 nodos tiene altura máxima ~10, vs ~1000 en un BST
degenerado.

En nuestras pruebas, con 900 juegos ordenados el AVL quedó con altura 10 y el BST con altura 900 ([sección 2.4](#24-comparación-bst-vs-avl)).

***¿Por qué el árbol general no se auto-balancea?*** 

El árbol general no necesita balanceo porque no tiene criterio de ordenamiento. Su estructura refleja una
jerarquía natural, no un orden numérico o alfabético. El costo de búsqueda O(n) es aceptable porque la
cantidad de categorías suele ser pequeña (decenas, no miles).

---

## 6. Conclusión

* **El AVL** garantiza búsquedas eficientes sin importar el orden de inserción, resolviendo el problema
principal de desbalance del BST. En nuestras pruebas, con 900 juegos ordenados quedó con altura 10 contra 900 del BST ([sección 2.4](#24-comparación-bst-vs-avl)).
* **El árbol general** permite organizar el dominio en una jerarquía de categorías (géneros y tags) y
mostrarla en la opción "Explorar categorías". Por ahora funciona como guía de consulta, y a futuro puede
orientar la búsqueda por etiquetas.
* Ambas estructuras se complementan: el AVL resuelve la búsqueda eficiente por título, el árbol general
organiza las categorías del catálogo.


---

## 7. Errores o dudas que tuvimos

* **`RecursionError` con datos ordenados.** En el TP3, el CSV viene ordenado alfabéticamente y el BST se degeneraba en una lista; lo resolvimos mezclando los juegos antes de insertarlos. En el TP4 volvió a aparecer: con 1000 datos ordenados el BST agota la recursión de Python ([sección 2.4](#24-comparación-bst-vs-avl)). Con el AVL ya no hace falta mezclar.
* **Opción 5 como guía.** Muestra una jerarquía fija. A futuro, queremos cargar los tags más relevantes desde el CSV para que sirva de guía de búsqueda.
* **Búsqueda por etiquetas con varias etiquetas.** Muestra los juegos que coinciden con cualquiera de ellas, no exige que se cumplan todas y un mismo juego puede aparecer más de una vez.


---

## 8. Datos y evidencia

* Script de prueba del AVL: [estructuras/avl.py](/estructuras/avl.py) (prueba con letras, sección 2.5) y [algoritmos/medir_tiempos_avl.py](/algoritmos/medir_tiempos_avl.py) (tabla con juegos, sección 2.4)
* Script de prueba del árbol general: [estructuras/arbol_general.py](/estructuras/arbol_general.py) (prueba con jerarquía de videojuegos, sección 3.4)
* Capturas de la terminal: 


[2.5](#25-prueba-del-avl) :

![avl.jpg](/assets/avl.jpg) 


[2.4](#24-comparación-bst-vs-avl) :

![medir_tiempos_avl.jpg](/assets/medir_tiempos_avl.jpg)  



[3.4](#34-prueba-del-árbol-general) :

![arbol_general.jpg](/assets/arbol_general.jpg) 
