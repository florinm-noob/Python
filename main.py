print("Invat Python de la zero")

lista = ["ana", "baca", "tutu", "carusel", "ll"]

newNume = input("Introduceti un nume:")
lista.append(newNume)

for k in lista:
    print("Nume:", k)

if "Florin" in lista:
    print("Florin este in lista")
else:
    print("Florin nu este in lista")