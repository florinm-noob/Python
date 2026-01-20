import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "Input")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

def citeste_fisier(nume_fisier):
    try:
        with open(nume_fisier, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print("Fisierul de input nu este gasit!")
        return []

def proceseaza_nume(linii):
    rezultat = []

    for linie in linii:
        nume = linie.strip().lower()
        if nume and nume not in rezultat:
            rezultat.append(nume)
    return rezultat


def scrie_fisier(nume_fisier, lista):
    try:
        with open(nume_fisier, "w") as f:
            for nume in lista:
                f.write(nume + "\n")
    except FileNotFoundError:
        print("Fisierul de output nu este gasit!")
        return False
    except PermissionError:
        print("Nu ai destule permisiuni!")
        return False

def main():
    input_path = os.path.join(INPUT_DIR, "input.txt")
    output_path = os.path.join(OUTPUT_DIR, "output2.txt")
    linii = citeste_fisier(input_path)
    if linii:
        nume_procesate = proceseaza_nume(linii)

        print("Nume procesate:")
        for n in nume_procesate:
            print(n)

        scrie_fisier(output_path, nume_procesate)

main()
