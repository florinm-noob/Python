import os
import csv
import json
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "Input")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

def citeste_csv(file_name):
    importFile = []
    try:
        with open(file_name, newline="", encoding="utf-8") as file:
            csvFile = csv.DictReader(file)
            for row in csvFile:
                row['name'] = row['name'].strip().lower()
                row['city'] = row['city'].strip().title()
                row['age'] = row['age'].strip()
                try:
                    int(row['age'])
                except ValueError:
                    row['age'] = ""
                if row['name'].strip() == "" or row['city'].strip() == "" or row['age'].strip() == "":
                    print("Line is not correct:", row)
                else:
                    importFile.append(row)
            return importFile
    except FileNotFoundError:
        print("Fisierul csv de input nu este gasit!")
        return []

def proceseaza_people(linii):
    nr_people = len(linii)
    ages = 0
    cities = defaultdict(int)

    for linie in linii:
        ages += int(linie['age'])
        cities[linie['city']] += 1
    
    stats = {
        "numar_total_persoane": nr_people,
        "varsta_medie": round(ages / nr_people, 2) if nr_people > 0 else 0,
        "numar_persoane_pe_orase": dict(cities)
    }
    return stats

def main():
    input_path = os.path.join(INPUT_DIR, "people.csv")
    linii = citeste_csv(input_path)
    print("testing")
    if linii:
        stats = proceseaza_people(linii)
        print(stats)
        output_path = os.path.join(OUTPUT_DIR, "output.json")
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=4, ensure_ascii=False)
            print(f"Rezultatele au fost salvate in {output_path}")
        except Exception as e:
            print(f"Eroare la scrierea fisierului: {e}")
main()
