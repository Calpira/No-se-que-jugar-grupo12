# Documentación Técnica: Pipeline de Procesamiento y Limpieza de Dataset de Steam

## Fuente de los Datos:

Se descargó el dataset de el siguiente sitio porque era de los pocos completos y actualizados al día de la fecha 17/9/2026.
[Kaggle.com - fronkongames Steam Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset?resource=download)

## 1. Contexto y problemática inicial

El dataset original de Steam (`games.csv`) presentaba fallas estructurales críticas que impedían su utilización directa en estructuras de datos avanzadas (como árboles de búsqueda o grafos de recomendación):

- **Peso excesivo (~150 MB):** contenía metadatos sobredimensionados, textos planos kilométricos y desvíos de columnas que inflaban artificialmente el tamaño del archivo.
- **Desplazamiento severo en cadena:** las cabeceras del CSV no coincidían con sus valores reales. Las columnas de géneros, categorías, etiquetas y estadísticas de votos estaban corridas una posición hacia la derecha, provocando un caos de datos cruzados.
- **Contenido NSFW masivo camuflado:** el dataset estaba plagado de juegos porno de baja calidad (*shovelware*). Sin embargo, un filtrado ingenuo basado en palabras como `nudity` o `sexual content` eliminaba por error a grandes producciones mainstream legítimas como *Cyberpunk 2077*, *The Witcher 3* o *Grand Theft Auto V*.
- **Ruido por valoraciones extremas:** existían miles de juegos muertos, gachas abandonados o títulos afectados por *review bombings* masivos con calificaciones muy bajas que ensuciaban los nodos de búsqueda.

---

## 2. Fase 1: Reparación estructural y normalización (`arreglar_dataset.py`)

Para solucionar el problema del peso y el desfase de columnas, se diseñó un script de saneamiento inicial.

**¿Por qué se hizo?**
Era necesario realinear las columnas desplazadas del CSV original y recortar la longitud de los textos para evitar cadenas gigantescas que ralentizaran las búsquedas en memoria.

**Cómo ayudó la IA:**
Se estructuró la lectura de columnas aplicando el corrimiento correcto:

| Campo real | Se leía desde la cabecera |
|---|---|
| Categories | `Genres` |
| Genres | `Tags` |
| Tags de la comunidad | `Screenshots` |

- Se implementó una función de recorte estricta (`recortar_lista`) para limitar cada campo a un máximo de elementos (por ejemplo, 5).
- **Rating bayesiano:** para evitar que juegos con apenas 2 o 3 votos tuvieran un puntaje perfecto y falso de 100%, se implementó una fórmula de ponderación bayesiana que jala los extremos hacia una nota promedio global (configurada en 30) utilizando un umbral de votos mínimos:

Rating Ponderado = ((votos_totales * rating_crudo) + (umbral_minimal * nota_promedio_global))
                   / (votos_totales + umbral_minimal)

Valores por defecto en el código: `umbral_minal=3000` y `nota_promedio_global=30`.

---

## 3. Fase 2: Filtrado inteligente de contenido adulto (`porndestroyer3000.py`)

El gran desafío era erradicar el contenido erótico/hentai de baja calidad sin que cayera en la volteada la industria AAA madura.

**¿Por qué se hizo?**
Las búsquedas y recomendaciones en los árboles debían mantenerse limpias de contenido pornográfico explícito o de estafas visuales.

**Cómo ayudó la IA:**
Se desarrolló un filtro multicapa de alta precisión ("Porndestroyer 3000") basado en condiciones combinadas:

1. **Filtro directo por título:** búsqueda de patrones explícitos e inconfundibles en el nombre del juego (ej. `hentai`, `meet and fuck`, `gooner`, etc.).
2. **Tags 100% explícitos:** etiquetas que los juegos mainstream nunca utilizan de forma legítima (ej. `erotica`, `nsfw audio`, `anime nudity`).
3. **Análisis de densidad para tags ambiguos:** etiquetas como `sexual content`, `nudity` o `mature content` aparecen tanto en *Cyberpunk 2077* como en un juego porno barato de $1. Para diferenciarlos, el script evalúa la ausencia de géneros protectores (`action`, `rpg`, `strategy`, etc.) y la falta de marcadores de producción mainstream (`open world`, `story rich`). Si un juego acumula múltiples tags adultos sin ningún respaldo de gran producción, se descarta automáticamente.

---

## 4. Fase 3: Poda definitiva por calificación (`trim_dataset.py`)

Una vez saneado el contenido y normalizadas las métricas, se realizó un último corte estricto de calidad.

**¿Por qué se hizo?**
Los juegos con calificaciones muy bajas (juegos rotos, abandonware injugable o gachas spameados) ocupan espacio inútil y empeoran las recomendaciones de los árboles.

**Cómo ayudó la IA:**
Se programó un filtro plano final centrado en el rating ponderado:

```python
UMBRAL_RATING_MINIMO = 32
```

Cualquier registro con un `Rating <= 32` fue descartado de forma definitiva, asegurando que el archivo resultante (`steam_games_final.csv`) contenga exclusivamente juegos con valoraciones aceptables y de interés real para el usuario.

---

## 5. Fase 4: Utilidades auxiliares de ordenamiento (`sort_dataset.py`)

**¿Por qué se hizo?**
Para disponer de una herramienta opcional que permita ordenar las filas del dataset antes de alimentar las estructuras de datos finales.

**Cómo ayudó la IA:**
Se dejó preparado un script auxiliar basado en `csv.DictReader` y el método `sort` nativo de Python con una `key` por columna.

*Estado actual:*
El repositorio contiene los archivos `Juegos.csv` y `Juegos_steam_unsafe.csv`, siendo la version "unsafe" el archivo pre-fase 3 ordenado, para utilizar en pruebas únicamente. 

---
## Resumen del pipeline

```
games.csv (~150 MB, columnas corridas)
   │
   ▼  arreglar_dataset.py   (realinea columnas, recorta listas, rating bayesiano)
steam_games_clean.csv
   │
   ├──▼  porndestroyer3000.py   (filtro multicapa de contenido adulto)
   │  steam_games_filtrado.csv
   │     │
   │     ▼  trim_dataset.py   (descarta Rating <= 32)
   │  steam_games_final.csv   ← dataset final
   │
   └──▼  sort_dataset.py   (opcional, hoy solo ordena por Name)
      steam_games_sorted.csv
```

