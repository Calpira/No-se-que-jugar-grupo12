import csv
import os

INPUT_CSV = "steam_games_filtrado.csv"
OUTPUT_CSV = "steam_games_final.csv"

UMBRAL_RATING_MINIMO = 32

def filtrar_por_rating():
    if not os.path.exists(INPUT_CSV):
        print(f"Error: No se encontró '{INPUT_CSV}'.")
        return

    juegos_originales = 0
    juegos_conservados = 0

    with open(INPUT_CSV, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        columnas = reader.fieldnames

        with open(OUTPUT_CSV, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=columnas)
            writer.writeheader()

            for row in reader:
                juegos_originales += 1
                try:
                    rating = int(row.get("Rating", 0))
                except ValueError:
                    rating = 0

                # Descarte plano de basura / review bombings irrelevantes
                if rating <= UMBRAL_RATING_MINIMO:
                    continue

                writer.writerow(row)
                juegos_conservados += 1

    eliminados = juegos_originales - juegos_conservados
    print("¡Poda final completada!")
    print(f"Juegos analizados: {juegos_originales}")
    print(f"Juegos eliminados (Rating <= {UMBRAL_RATING_MINIMO}): {eliminados}")
    print(f"Dataset final resultante: {juegos_conservados} juegos")

if __name__ == "__main__":
    filtrar_por_rating()