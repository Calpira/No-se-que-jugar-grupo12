import csv
import os

INPUT_CSV = "steam_games_clean.csv"
OUTPUT_CSV = "steam_games_sorted.csv"

def ordenar_dataset(por="nombre", descendente=False):
    """
    por: 'rating' o 'nombre'
    descendente: True para mayor a menor (o Z-A), False para menor a mayor (o A-Z)
    """
    descendente=False
    por="nombre"
    if not os.path.exists(INPUT_CSV):
        print(f"Error: No se encontró '{INPUT_CSV}'.")
        return

    with open(INPUT_CSV, mode='r', encoding='utf-8') as infile:
        filas = list(csv.DictReader(infile))
        if not filas:
            print("El CSV está vacío.")
            return

        columnas = filas[0].keys()

        # Criterios de ordenamiento
      #  if por.lower() == "rating":
      #      # Convierte a entero para ordenar numéricamente (ej: 100 -> 0)
      #      filas.sort(key=lambda x: int(x.get("Rating", 0)), reverse=descendente)
        if por.lower() == "nombre":
            # Convierte a minúsculas para un orden alfabético correcto (A-Z o Z-A)
            filas.sort(key=lambda x: x.get("Name", "").lower(), reverse=descendente)

    with open(OUTPUT_CSV, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(filas)

    print(f"¡Dataset ordenado por '{por}' (descendente={descendente}) y guardado en '{OUTPUT_CSV}'!")

if __name__ == "__main__":
    # --- OPCIONES DE USO ---
    
    # 1. Por Rating de MEJOR a PEOR (100 -> 0):
    ordenar_dataset(por="rating", descendente=True)
    
    # 2. Alfabéticamente de la A a la Z:
    # ordenar_dataset(por="nombre", descendente=False)