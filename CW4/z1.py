from Crypto.Hash import SHA256
import os

plik_sum = "SHA256SUMS.txt"

for linia in open(plik_sum, encoding="utf-8"):
    suma, plik = linia.rstrip("\n").split("  ", 1)

    if not os.path.isfile(plik):
        print(plik + ": BRAK")
    else:
        data = open(plik, "rb").read()
        h = SHA256.new(data)
        wynik = h.hexdigest()

        if wynik == suma:
            print(plik + ": OK")
        else:
            print(plik + ": BŁĄD")


a = SHA256.new(b"Ala ma kota.").digest()
b = SHA256.new(b"Ola ma kota.").digest()

wynik = bytes(a[i] ^ b[i] for i in range(32))
print("Różniące się bity:", sum(bajt.bit_count() for bajt in wynik))


