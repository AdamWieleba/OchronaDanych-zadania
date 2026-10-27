#użycie: python program.py baza_htpasswd identyfikator hasło


# 1. Sprawdzanie identyfikatora i hasła użytkownika
import sys
import subprocess

plik = sys.argv[1]
uzytkownik = sys.argv[2]
haslo = sys.argv[3]

wynik = subprocess.run(
    ["htpasswd", "-vb", plik, uzytkownik, haslo],
    capture_output=True
)

if wynik.returncode == 0:
    print("Hasło poprawne")
else:
    print("Hasło niepoprawne")




# 2. Zmiana hasła użytkownika
"""-B – używa algorytmu bcrypt.
-b – pobiera hasło z argumentu polecenia."""
import sys
import subprocess

plik = sys.argv[1]
uzytkownik = sys.argv[2]
haslo = sys.argv[3]

subprocess.run(
    ["htpasswd", "-B", "-b", plik, uzytkownik, haslo]
)

print("Zmieniono hasło użytkownika.")




# 3. Dodawanie nowego użytkownika do bazy
import sys
import subprocess

plik = sys.argv[1]
uzytkownik = sys.argv[2]
haslo = sys.argv[3]

subprocess.run(
    ["htpasswd", "-B", "-b", plik, uzytkownik, haslo]
)

print("Dodano użytkownika.")


"""
htpasswd:
-c	Tworzy nowy plik bazy (nadpisuje istniejący!).
-b	Pobiera hasło z argumentu polecenia.
-v	Weryfikuje podane hasło.
-D	Usuwa użytkownika z bazy.
-B	Używa algorytmu bcrypt do haszowania haseł.
-m	Używa algorytmu MD5 (Apache APR1).
-d	Używa DES crypt() (niezalecane).
-s	Używa SHA-1 (niezalecane do nowych zastosowań).
-i	Odczytuje hasło ze standardowego wejścia.
-n	Wyświetla wynik na standardowym wyjściu zamiast zapisywać do pliku.
-v	Sprawdza, czy podane hasło odpowiada zapisowi w bazie.

Przykłady
# Utworzenie bazy i pierwszego użytkownika
htpasswd -c hasla.txt jan

# Dodanie użytkownika do istniejącej bazy
htpasswd hasla.txt anna

# Dodanie użytkownika z bcrypt
htpasswd -B hasla.txt anna

# Weryfikacja hasła
htpasswd -v hasla.txt jan

# Usunięcie użytkownika
htpasswd -D hasla.txt jan
"""


# 4. Odtworzenie działania md5sum
"""
Wynik jest taki sam jak dla  md5sum [plik]  dla tego samego pliku.
- hashlib.md5(data) – oblicza skrót MD5 z bajtów
- hexdigest() – zwraca skrót jako ciąg znaków szesnastkowych.
"""
import sys
import hashlib

plik = sys.argv[1]

data = open(plik, "rb").read()
hash = hashlib.md5(data).hexdigest()

print(hash, plik)




# 5. Kontrola spójności plików jak w md5sum -c [plik]
"""
python sprawdz_md5.py sumy.txt
Program odczytuje plik sum kontrolnych, oblicza MD5 każdego wskazanego pliku i porównuje wynik z zapisanym skrótem.

Zakładamy standardowy format pliku kontrolnego, np. d41d...27e  pusty.txt

split("  ", 1) rozdziela skrót i nazwę pliku.
hashlib.md5(data).hexdigest() oblicza aktualny skrót.
Porównanie wynik == suma wykrywa zmianę zawartości pliku.
"""
import sys
import hashlib

plik_sum = sys.argv[1]

for linia in open(plik_sum):
    suma, plik = linia.rstrip("\n").split("  ", 1)

    data = open(plik, "rb").read()
    wynik = hashlib.md5(data).hexdigest()

    if wynik == suma:
        print(plik + ": OK")
    else:
        print(plik + ": FAILED")





# 6. Pomiar czasu ataku brute-force
"""
najpierw wygeneruj skrót testowego hasła, np. aB:
python -c "import hashlib; print(hashlib.md5(b'aB').hexdigest())"

Następnie uruchom atak, wstawiając otrzymany skrót:
python brute.py [skrót_MD5] 2
"""
import sys
import hashlib
import string
import itertools
import time

cel = sys.argv[1]
dlugosc = int(sys.argv[2])

znaki = string.ascii_letters
proby = 0
start = time.time()

for kombinacja in itertools.product(znaki, repeat=dlugosc):
    haslo = "".join(kombinacja)
    wynik = hashlib.md5(haslo.encode()).hexdigest()
    proby += 1

    if wynik == cel:
        czas = time.time() - start
        print("Złamane hasło:", haslo)
        print("Liczba prób:", proby)
        print("Czas:", czas, "s")
        print("Próby na sekundę:", proby / czas)
        break
else:
    czas = time.time() - start
    print("Nie znaleziono hasła o podanej długości.")
    print("Liczba prób:", proby)
    print("Czas:", czas, "s")
    print("Próby na sekundę:", proby / czas)



# 7. Zgadywanie haseł z bazy htpasswd
"""
python zgadnij.py hasla.txt jan
- crypt.crypt(trial, passwd) oblicza skrót z solą pobraną z istniejącego zapisu.
- Jeśli skróty są identyczne, program wypisuje znalezione hasło.
W nowszych wersjach Pythona moduł crypt może być niedostępny.
"""
import sys
import crypt
import itertools
import string

plik = sys.argv[1]
uzytkownik = sys.argv[2]

baza = open(plik).readlines()

for linia in baza:
    nazwa, passwd = linia.rstrip("\n").split(":", 1)

    if nazwa == uzytkownik:
        break

chars = string.ascii_lowercase

for kombinacja in itertools.product(chars, repeat=3):
    trial = "".join(kombinacja)

    if crypt.crypt(trial, passwd) == passwd:
        print("Hasło złamane:", trial)
        break
else:
    print("Nie znaleziono hasła")




# 8. Dwa dokumenty o identycznym skrócie trivial_hash()
# python kolizja.py
"""
Generuje losowe teksty długości 10 znaków.
Oblicza skrót każdego tekstu i zapamiętuje go w słowniku znalezione.
Jeśli dany skrót już występuje, a teksty są różne, znaleziono kolizję.
Zapisuje oba dokumenty do plików.
"""
import hashlib
import random
import string

def trivial_hash(dane):
    hash = 0
    for znak in dane:
        hash += ord(znak)
    return hash % 999

znaki = string.ascii_letters + string.digits
znalezione = {}

while True:
    tekst = "".join(
        random.choices(znaki, k=10)
    )

    h = trivial_hash(tekst)

    if h in znalezione and znalezione[h] != tekst:
        tekst1 = znalezione[h]
        tekst2 = tekst

        open("dokument1.txt", "w").write(tekst1)
        open("dokument2.txt", "w").write(tekst2)

        print("Znaleziono kolizję!")
        print("Dokument 1:", tekst1)
        print("Dokument 2:", tekst2)
        print("Wspólny skrót:", h)
        break

    znalezione[h] = tekst



# 9. Szukanie kolizji przez modyfikację białych znaków
"""
Najpierw oblicz skrót dokumentu, np. za pomocą krótkiego polecenia:
python -c "d=open('dokument.txt').read(); print(sum(map(ord,d))%999)"

Następnie przekaż nazwę pliku i obliczony skrót:
python bialeznaki.py dokument.txt 123

Dlaczego to działa?
Każda spacja zwiększa sumę znaków o 32, a funkcja zwraca wynik modulo 999. Ponieważ 32 i 999 są względnie pierwsze, 
dopisując od 1 do 999 spacji, można uzyskać każdą wartość skrótu modulo 999. Zmiana białych znaków nie musi być widoczna 
podczas zwykłego czytania dokumentu, ale zmienia jego treść.
"""

import sys

def trivial_hash(dane):
    hash = 0
    for znak in dane:
        hash += ord(znak)
    return hash % 999

plik = sys.argv[1]
cel = int(sys.argv[2])

dane = open(plik, "r").read()

for i in range(1, 1000):
    nowy_tekst = dane + " " * i

    if trivial_hash(nowy_tekst) == cel:
        open("kolizja.txt", "w").write(nowy_tekst)

        print("Znaleziono kolizję!")
        print("Liczba dodanych spacji:", i)
        print("Wspólny skrót:", cel)
        break
