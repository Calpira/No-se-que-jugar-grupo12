import csv
import os

ORIGINAL_CSV = "games.csv"
CLEAN_CSV = "steam_games_clean.csv"

def limpiar_texto(texto):
    if not texto:
        return ""
    return texto.strip().replace('"', '').replace("'", "")

def recortar_lista(texto_raw, max_elementos=5):
    texto = limpiar_texto(texto_raw)
    if not texto:
        return ""
    elementos = [e.strip() for e in texto.split(",") if e.strip()]
    return ", ".join(elementos[:max_elementos])

def calcular_rating_bayesiano(positivos, negativos, umbral_minal=3000, nota_promedio_global=30):
    votos_totales = positivos + negativos
    if votos_totales == 0:
        return 0
    rating_crudo = (positivos / votos_totales) * 100
    rating_ponderado = ((votos_totales * rating_crudo) + (umbral_minal * nota_promedio_global)) / (votos_totales + umbral_minal)
    return round(rating_ponderado)

def reparar_y_trimear_dataset():
    if not os.path.exists(ORIGINAL_CSV):
        print(f"Error: No se encontró el archivo '{ORIGINAL_CSV}'.")
        return

    print("Corrigiendo el desplazamiento en cadena de columnas...")

    with open(ORIGINAL_CSV, mode='r', encoding='utf-8', errors='ignore') as infile:
        reader = csv.DictReader(infile)

        with open(CLEAN_CSV, mode='w', encoding='utf-8', newline='') as outfile:
            columnas_finales = ["AppID", "Name", "Genres", "Categories", "Tags", "Rating"]
            writer = csv.DictWriter(outfile, fieldnames=columnas_finales)
            writer.writeheader()

            juegos_procesados = 0
            for row in reader:
                try:
                    appid = row.get("AppID", "").strip()
                    if not appid or not appid.isdigit():
                        continue

                    name = limpiar_texto(row.get("Name", "Unknown Game"))

                    # --- DESFASE DE 1 COLUMNA A LA DERECHA CORREGIDO ---
                    # Categories reales están en la cabecera "Genres"
                    categories = recortar_lista(row.get("Genres", ""), max_elementos=5)

                    # Genres reales están en la cabecera "Tags"
                    genres = recortar_lista(row.get("Tags", ""), max_elementos=5)

                    # Tags reales están en la cabecera "Screenshots"
                    tags = recortar_lista(row.get("Screenshots", ""), max_elementos=5)

                    # Votos desplazados
                    positivos_str = row.get("Negative", "0")
                    negativos_str = row.get("Score rank", "0")

                    positivos = int(positivos_str) if positivos_str.isdigit() else 0
                    negativos = int(negativos_str) if negativos_str.isdigit() else 0

                    rating = calcular_rating_bayesiano(positivos, negativos)

                    writer.writerow({
                        "AppID": appid,
                        "Name": name,
                        "Genres": genres,
                        "Categories": categories,
                        "Tags": tags,
                        "Rating": rating
                    })
                    juegos_procesados += 1

                except Exception:
                    continue

    print(f"¡Dataset procesado con éxito! Se guardaron {juegos_procesados} juegos en '{CLEAN_CSV}'.")

if __name__ == "__main__":
    reparar_y_trimear_dataset()