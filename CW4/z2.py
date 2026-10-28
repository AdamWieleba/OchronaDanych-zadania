from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from hmac import compare_digest


def weryfikuj(podany_login, haslo):
    for login, iteracje_str, sol_hex, skrot_hex in dane:
        if podany_login == login:
            sol = bytes.fromhex(sol_hex)
            iteracje = int(iteracje_str)

            key = PBKDF2(
                haslo.encode("utf-8"),
                sol,
                dkLen=32,
                count=iteracje,
                hmac_hash_module=SHA256
            )

            return compare_digest(key.hex(), skrot_hex)

    return False


def dodaj(login, haslo):
    sol = get_random_bytes(16)
    iteracje = 600000

    key = PBKDF2(
        haslo.encode("utf-8"),
        sol,
        dkLen=32,
        count=iteracje,
        hmac_hash_module=SHA256
    )

    return [login, str(iteracje), sol.hex(), key.hex()]


dane = []

for linia in open("hasla.txt", encoding="utf-8"):
    dane.append(linia.rstrip("\n").split(":"))


print("Weryfikacja (anna, Kasztan-2026):", weryfikuj("anna", "Kasztan-2026"))
print("Weryfikacja (anna, kasztan-2026):", weryfikuj("anna", "kasztan-2026"))
print("Weryfikacja (piotr, Żółw na łące):", weryfikuj("piotr", "Żółw na łące"))
print("Weryfikacja (kasia, Kasztan-2026):", weryfikuj("kasia", "Kasztan-2026"))


test1 = dodaj("test1", "haslo123")
test2 = dodaj("test2", "haslo123")

dane.append(test1)
dane.append(test2)

print("Czy sole są takie same:", test1[2] == test2[2])
print("Czy skróty są takie same:", test1[3] == test2[3])

print("Weryfikacja test1:", weryfikuj("test1", "haslo123"))
print("Weryfikacja test2:", weryfikuj("test2", "haslo123"))

