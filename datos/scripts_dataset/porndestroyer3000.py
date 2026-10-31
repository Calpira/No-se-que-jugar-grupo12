import csv
import os

INPUT_CSV = "steam_games_sorted.csv"
OUTPUT_CSV = "steam_games_filtrado.csv"

# 1. Palabras en el título que JAMÁS van en un juego mainstream (Descarte inmediato)
TITULO_PORNO_DIRECTO = [
    "hentai", "meet and fuck", "sex with", "waifu", "fuck", "cum", "milf",
    "oppai", "boobs", "strip", "ecchi", "pussy", "dick", "cock", "orgasm",
    "porno", "porn", "hentai girl", "erotic puzzle", "sex simulator","gooner","goonnette","incest"
]

# 2. Tags de la comunidad 100% NSFW (GTA V y Cyberpunk NUNCA usan estos tags)
TAGS_100_PORNO = [
    "hentai", "erotica", "nsfw audio", "hentai 3d", "anime nudity"
]

# 3. Tags ambiguos (Los tienen tanto Cyberpunk/GTA como el porno indie)
TAGS_AMBIGUOS = ["sexual content", "nudity", "mature content","furry"]

# 4. Géneros/Tags "Protectores" (Si tiene uno de estos, es un juego real con contenido adulto)
GENEROS_PROTECTORES = [
    "action", "rpg", "strategy", "shooter", "open world", 
    "racing", "sports", "fps", "survival", "story-rich"
]

# Tags de contenido adulto para contar densidad
TAGS_ADULTOS_CONTEO = [
    "sexual content", "nudity", "mature content", "mature", "erotica", "hentai", "nsfw"
]

# Tags de peso pesado que identifican juegos AAA/Grandes (que un RPG erótico de $1 no suele tener)
MARCADORES_MAINSTREAM = [
    "open world", "story rich", "great soundtrack", "sci-fi", "fps", "multiplayer", "co-op"
]

def es_juego_porno(nombre, genres, categories, tags):
    nombre_l = nombre.lower()
    meta_l = f"{genres} {categories} {tags}".lower()

    # 1. Filtro directo por título explícito
    for palabra in TITULO_PORNO_DIRECTO:
        if palabra in nombre_l:
            return True

    # 2. Filtro directo por tags 100% NSFW
    for tag in TAGS_100_PORNO:
        if tag in meta_l:
            return True

    # 3. CONTEO DE TAGS ADULTOS (Triple/Double Match)
    conteo_adulto = sum(1 for tag in TAGS_ADULTOS_CONTEO if tag in meta_l)
    tiene_marcador_mainstream = any(m in meta_l for m in MARCADORES_MAINSTREAM)

    # Si junta 3 o más tags adultos ("Sexual Content", "Nudity", "Mature"), vuela
    if conteo_adulto >= 3 and not tiene_marcador_mainstream:
        return True

    # Si junta 2 tags adultos y no tiene un género principal fuerte
    tiene_genero_real = any(g in meta_l for g in GENEROS_PROTECTORES)
    if conteo_adulto >= 2 and not (tiene_genero_real and tiene_marcador_mainstream):
        return True

    return False

def filtrar_dataset():
    if not os.path.exists(INPUT_CSV):
        print(f"Error: No se encontró '{INPUT_CSV}'.")
        return

    juegos_procesados = 0
    eliminados = 0

    with open(INPUT_CSV, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        columnas = reader.fieldnames

        with open(OUTPUT_CSV, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=columnas)
            writer.writeheader()

            for row in reader:
                juegos_procesados += 1
                nombre = row.get("Name", "")
                genres = row.get("Genres", "")
                categories = row.get("Categories", "")
                tags = row.get("Tags", "")

                if es_juego_porno(nombre, genres, categories, tags):
                    eliminados += 1
                    continue

                writer.writerow(row)

    print("¡Filtrado completado!")
    print(f"Total procesados: {juegos_procesados}")
    print(f"Juegos porno eliminados: {eliminados}")
    print(f"Juegos limpios conservados: {juegos_procesados - eliminados}")

if __name__ == "__main__":
    filtrar_dataset()