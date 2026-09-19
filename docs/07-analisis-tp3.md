# Análisis TP3 — Árbol Binario de Búsqueda

## 1. ¿Qué resolvimos?
Incorporamos un **árbol binario de búsqueda (BST)** para resolver la búsqueda por **título** de forma más eficiente que recorrer la lista completa.

## 2. Clave de ordenamiento
Ordenamos por **título** porque es el dato por el que el usuario busca un juego puntual (la opción "Buscar por título" del menú). La funcionalidad 'búsqueda por tags' sigue operando sobre la lista normal, sin cambios. Y 'listar' se elimino debido al volumen de datos.

## 3. Prueba del árbol
Salida de `python -m algoritmos.probar_bst`:
```
Altura del árbol: 3

--- inorder (ordenado alfabéticamente) ---
  Celeste ⭐94.0 (Platformer, Indie)
  Elden Ring ⭐96.0 (Action, RPG)
  Hollow Knight ⭐93.0 (Metroidvania, Action)
  Portal 2 ⭐97.0 (Puzzle, Co-op)
  Stardew Valley ⭐96.0 (Simulation, RPG)

--- preorder ---
  Portal 2
  Elden Ring
  Celeste
  Hollow Knight
  Stardew Valley

--- postorder ---
  Celeste
  Hollow Knight
  Elden Ring
  Stardew Valley
  Portal 2

--- búsquedas ---
Buscar 'portal 2': Portal 2 ⭐97.0 (Puzzle, Co-op)
Buscar 'zzz': None
```
## 4. Comparación de tiempos
En la tabla siguiente, los tiempos son **reales**, sacados con nuestro
script `algoritmos/medir_tiempos.py`.

| N elementos | Secuencial (ms) | Binaria (ms) | Árbol BST (ms) |
|-----------|-----------|-----------|-------------  |
|100          |0.0177           |0.0139          |0.0072  |
|1000         |0.2305           |0.1404          |0.0098 |
|10000        |2.7323           |1.9605          |0.0100|
|16667        |4.1984           |3.2399          |0.0072|

## 5. Análisis de complejidad
- **Búsqueda secuencial:** O(n). Recorre toda la lista en el peor caso.
- **Búsqueda binaria:** O(log n) pero exige lista ordenada (ordenar cuesta O(n log n) una sola vez)
- **Búsqueda en árbol:** O(log n) promedio si el árbol está balanceado;
O(n) en el peor caso si está degenerado (como una lista).
- **Inserción en árbol:** O(log n) promedio, O(n) peor caso.
- **Recorridos (inorder, preorder, postorder):** O(n), porque visitan cada nodo 1 vez.

## 6. Conclusión

>Con 16.667 elementos, la secuencial tardó ~4.2 ms y el árbol ~0.007 ms.

A medida que agregamos más juegos, la búsqueda secuencial se hace cada vez más lenta porque tiene que revisar más elementos. El árbol casi no se ve afectado, porque en cada paso descarta la mitad de las opciones restantes. Por eso, para una búsqueda que se usa seguido (como buscar por título), conviene más el árbol.

## 7. Errores o dudas que tuvimos

Al construir el árbol con los datos del CSV, nos encontramos con un `RecursionError`. El motivo: el CSV viene **ordenado alfabéticamente por título**, y si insertábamos los juegos en ese mismo orden, el árbol se "degeneraba" — cada nodo nuevo se insertaba siempre del mismo lado, quedando prácticamente como una lista enlazada. La solución fue **mezclar el orden de inserción** (con `random.shuffle`) antes de construir el árbol.

## 8. Notas extra

Conseguimos adaptar un CSV con datos reales del catálogo de Steam y modificamos el programa para dejar de usar el json con el que se efectuaron las primeras pruebas.

sacamos la opción "Listar todos los juegos" del menú. Con el catálogo actualizado de juegos, consideramos que listarlos todos en consola no es util ni practico. Igualmente la funcionalidad ya fue comprobada en la Entrega 1 con el dataset anterior.

El campo `Rating` no es un promedio simple de votos positivos/negativos, sino un **rating ponderado**, para evitar que un juego con muy pocos votos (por ejemplo, 2 positivos y 0 negativos) aparezca como "el mejor" por encima de juegos con miles de reseñas: 

![rating](/assets/image.png)


>queda pendiente implementar el listado de rating en el codigo.

