#!/usr/bin/python3
import os

print("Content-Type: text/plain; charset=utf-8")
print()

print("Efektywny UID:", os.geteuid())
print("Efektywny GID:", os.getegid())

def odczytaj(sciezka):
    print("Plik:", sciezka)
    try:
        with open(sciezka, "r", encoding="utf-8") as plik:
            print(plik.read())
    except OSError:
        print("Blad odczytu")
    except PermissionError:
        print("Odmowa odczytu")

odczytaj("/lab-data/ogolny.txt")
odczytaj("/lab-data/poufny.txt")
