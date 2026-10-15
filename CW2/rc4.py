def rc4(dane, klucz):
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + klucz[i % len(klucz)]) % 256
        S[i], S[j] = S[j], S[i]

    wynik = bytearray()
    i = 0
    j = 0

    for bajt in dane:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        wynik.append(bajt ^ k)

    return bytes(wynik)


with open("rc4.bin", "rb") as plik:
    kryptogram = plik.read()

test = b"fjkdahfkdjasfhkdsdhjkds"
klucz_testowy = b"hxjcgjx"

print("Zgodność po zaszyfrowaniu i odszyfrowaniu:",
      rc4(rc4(test, klucz_testowy), klucz_testowy) == test)
