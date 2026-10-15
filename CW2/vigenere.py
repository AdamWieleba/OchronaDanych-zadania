def szyfruj(dane, klucz):
    wynik = []
    for i in range(len(dane)):
        bajt = dane[i]
        znak_klucza = klucz[i % len(klucz)]
        nowy_bajt = (bajt + znak_klucza) % 256
        wynik.append(nowy_bajt)
    return bytes(wynik)

def odszyfruj(dane, klucz):
    wynik = []
    for i in range(len(dane)):
        bajt = dane[i]
        znak_klucza = klucz[i % len(klucz)]
        nowy_bajt = (bajt - znak_klucza) % 256
        wynik.append(nowy_bajt)
    return bytes(wynik)


klucz = b"ZAMEK"

with open("tekst_pl.txt", "rb") as plik:
    tekst = plik.read()

kryptogram = szyfruj(tekst, klucz)

with open("vigenere.bin", "wb") as plik:
    plik.write(kryptogram)

odczyt = odszyfruj(kryptogram, klucz)

print("Zgodność pliku po zaszyfrowaniu i odszyfrowaniu:", odczyt == tekst)

print("Test dla pustych danych:", szyfruj(b"", klucz) == b"")
test = bytes([0, 255, 10, 128])
print("Test dla bajtów 0 i 255:", odszyfruj(szyfruj(test, klucz), klucz) == test)


tekst = b"BRAMABRAMABRAMA"

for klucz in [b"SZYFR", b"KOD"]:
    wynik = szyfruj(tekst, klucz)
    print("\nKlucz:", klucz.decode())
    print("Hex:", wynik.hex())

    for i in range(0, len(wynik), 5):
        print(wynik[i:i + 5].hex())