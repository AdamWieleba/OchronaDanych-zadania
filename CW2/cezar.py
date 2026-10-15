with open("cezar.bin", "rb") as f:
    dane = f.read()

wyniki = []

for k in range(256):
    tekst = bytes((b - k) % 256 for b in dane)

    poprawne = sum(
        1 for b in tekst
        if 32 <= b <= 126 or b in (9, 10, 13)
    )

    ocena = poprawne / len(tekst)
    wyniki.append((ocena, -k, tekst)) #-k do sortowania

wyniki.sort()
wyniki.reverse()
for ocena, k, tekst in wyniki[:5]:
    print("k=", -k, " ocena =", ocena, " początek tekstu =", repr(tekst[:50]))

k = 233
odszyfrowany = bytes((b - k) % 256 for b in dane)
with open("cezar.txt", "wb") as f:
    f.write(odszyfrowany)