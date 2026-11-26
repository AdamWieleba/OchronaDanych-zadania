
import math
import time

n = 1466056398307
e = 65537
c = [1276399951879, 106940793212, 684046625666, 960092665163, 364786929191, 1264904338683, 166227478096, 35014330973, 1420987870609, 499336535119, 
     227818277782, 1130954112845, 190462688288, 63550420202, 369305189176, 623354059250, 1179166008663, 944014363107, 214643169131, 726491477478, 
     22133939293, 330565705661, 1400101629899, 755925812857, 713851579523, 1191852064143, 514596226329, 491636820274, 255288661822, 317915037793]

# Potęgowanie modularne
def modular_power(base, exponent, modulus):
    result = 1
    base %= modulus

    while exponent > 0:

        if exponent % 2 == 1:
            result = (result * base) % modulus

        base = (base * base) % modulus
        exponent //= 2
    return result

print("4^13 mod 497 =", modular_power(4, 13, 497), "(poprawne: 445)")
print("4^0 mod 497 =", modular_power(4, 0, 497), "(poprawne: 1)")


# Rozłożenie na p,q
def factorize(n):
    if n < 2:
        return (None, None)

    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return i, n // i

    return (None, None)

start = time.perf_counter()
p, q = factorize(n)
koniec = time.perf_counter()

print(f"p = {p}, q = {q}")
print(f"Czas: {koniec - start:.6f}s")


phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

print(f"phi = {phi}, d = {d}")
print("Sprawdzenie (e * d) % phi == 1:", (e * d) % phi == 1)


decrypted_blocks = []

for block in c:
    m = modular_power(block, d, n)
    decrypted_blocks.append(m)

plaintext_bytes = b""

for m in decrypted_blocks:
    plaintext_bytes += m.to_bytes(4, byteorder='big')

plaintext = plaintext_bytes.decode('utf-8')

print("\nOdszyfrowany tekst:")
print(plaintext)
