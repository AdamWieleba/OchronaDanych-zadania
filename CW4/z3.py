from Crypto.Hash import SHA256


def h24(dane):
    return SHA256.new(dane).digest()[:3]


oryginal = open("oryginal.txt", "rb").read().splitlines(keepends=True)
zmieniony = open("zmieniony.txt", "rb").read().splitlines(keepends=True)

skroty = {}

for v in range(8192):
    dane = b""

    for i in range(13): # dla każdego wiersza 0-12
        dane += oryginal[i][:-1]

        if (v >> i) & 1:
            dane += b" "

        dane += b"\n"

    skrot = h24(dane)

    if skrot not in skroty:
        skroty[skrot] = v


znaleziono = False
skrot_oryginalu = h24(b"".join(oryginal))
licznik = 0

for v in range(8192):
    dane = b""

    for i in range(13):
        dane += zmieniony[i][:-1]

        if (v >> i) & 1:
            dane += b" "

        dane += b"\n"

    skrot = h24(dane)

    if skrot == skrot_oryginalu:
        licznik += 1

    if not znaleziono and skrot in skroty:
        print("Kolizja:")
        print("v oryginału:", skroty[skrot])
        print("v zmienionego:", v)
        print("h24:", skrot.hex())
        znaleziono = True

print("Liczba wariantów zmienionego o h24 równym oryginałowi:", licznik)