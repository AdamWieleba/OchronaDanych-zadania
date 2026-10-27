
# 1. Sprawdzanie identyfikatora i hasła użytkownika
"""
subprocess.run() – uruchamia zewnętrzny program.
htpasswd -v – sprawdza hasło użytkownika.
Kod zakończenia 0 oznacza powodzenie.
"""
import sys
import subprocess
import os

if len(sys.argv) != 2:
    print("Użycie: python sprawdz.py [plik_bazy]")
    sys.exit(1)

plik = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    sys.argv[1])

if not os.path.isfile(plik):
    print("Nie znaleziono pliku bazy.")
    sys.exit(1)

uzytkownik = input("Podaj identyfikator: ")

try:
    wynik = subprocess.run(
        ["htpasswd", "-v", plik, uzytkownik]
    )

    if wynik.returncode == 0:
        print("Logowanie poprawne.")
    else:
        print("Niepoprawne hasło lub błąd weryfikacji.")

except FileNotFoundError:
    print("Nie znaleziono programu htpasswd.")





# 2. Zmiana hasła użytkownika
"""
Program sprawdza obecność identyfikatora w bazie.
getpass() ukrywa wpisywane hasło.
Porównanie dwóch wpisów zapobiega literówkom.
htpasswd -B -i aktualizuje rekord, generując nowy skrót bcrypt.
"""
import sys
import subprocess
import os
from getpass import getpass

if len(sys.argv) != 2:
    print("Użycie: python zmien_haslo.py [plik_bazy]")
    sys.exit(1)

plik = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    sys.argv[1])

if not os.path.isfile(plik):
    print("Nie znaleziono pliku bazy.")
    sys.exit(1)

uzytkownik = input("Podaj identyfikator użytkownika: ")

# Odczyt identyfikatorów z bazy
with open(plik, "r", encoding="utf-8") as f:
    uzytkownicy = {
        linia.split(":", 1)[0]
        for linia in f
        if ":" in linia
    }

if uzytkownik not in uzytkownicy:
    print("Taki użytkownik nie istnieje.")
    sys.exit(1)

haslo = getpass("Podaj nowe hasło: ")
powtorzenie = getpass("Powtórz nowe hasło: ")

if not haslo:
    print("Hasło nie może być puste.")
    sys.exit(1)

if haslo != powtorzenie:
    print("Hasła nie są identyczne.")
    sys.exit(1)

try:
    wynik = subprocess.run(
        ["htpasswd", "-B", "-i", plik, uzytkownik],
        input=haslo + "\n",
        text=True,
        capture_output=True
    )

    if wynik.returncode == 0:
        print("Hasło zostało zmienione.")
    else:
        print("Nie udało się zmienić hasła.")
        print(wynik.stderr)

except FileNotFoundError:
    print("Nie znaleziono programu htpasswd.")





# 3. Dodawanie nowego użytkownika do bazy
"""
Program odczytuje identyfikatory z pliku.
Jeśli użytkownik już istnieje, operacja zostaje przerwana.
Po poprawnym wpisaniu hasła htpasswd -B -i tworzy nowy rekord z hasłem zabezpieczonym algorytmem bcrypt.
Opcja -c nie jest używana, ponieważ mogłaby nadpisać całą istniejącą bazę
"""

import sys
import subprocess
import os
from getpass import getpass

if len(sys.argv) != 2:
    print("Użycie: python dodaj.py [plik_bazy]")
    sys.exit(1)

plik = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    sys.argv[1])

if not os.path.isfile(plik):
    print("Nie znaleziono pliku bazy.")
    sys.exit(1)

uzytkownik = input("Podaj nowy identyfikator: ")

if not uzytkownik or ":" in uzytkownik or "\n" in uzytkownik:
    print("Niepoprawny identyfikator.")
    sys.exit(1)

# Odczyt istniejących użytkowników
with open(plik, "r", encoding="utf-8") as f:
    uzytkownicy = {
        linia.split(":", 1)[0]
        for linia in f
        if ":" in linia
    }

if uzytkownik in uzytkownicy:
    print("Użytkownik już istnieje.")
    sys.exit(1)

haslo = getpass("Podaj hasło: ")
powtorzenie = getpass("Powtórz hasło: ")

if not haslo:
    print("Hasło nie może być puste.")
    sys.exit(1)

if haslo != powtorzenie:
    print("Hasła nie są identyczne.")
    sys.exit(1)

try:
    wynik = subprocess.run(
        ["htpasswd", "-B", "-i", plik, uzytkownik],
        input=haslo + "\n",
        text=True,
        capture_output=True
    )

    if wynik.returncode == 0:
        print("Dodano nowego użytkownika.")
    else:
        print("Nie udało się dodać użytkownika.")
        print(wynik.stderr)

except FileNotFoundError:
    print("Nie znaleziono programu htpasswd.")

