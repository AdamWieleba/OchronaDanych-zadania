"""
p, q - jakieś 2 liczby pierwsze
n = p * q
phi = (p - 1) * (q - 1)
e: 
dowolne 1 < e < phi, gdzie  phi % e != 0  (lub inaczej: NWD(e,phi) = 1)
d:
(e * d) % phi = 1

Szyfrowanie c = m^e % n, deszyfrowanie m = c^d % n, gdzie  0 <= m < n
"""


# Algorytm Euklidesa = NWD (największy wspólny dzielnik)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a
print(gcd(48, 18))  # 6
print(gcd(17, 3120))  # 1



# Rozszerzony algorytm Euklidesa
# daje x,y   a*x + b*y = NWD(a,b)
# "x" jest odwrotnością modularną liczby a mod b
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1
    # // = dzielenie całkowite (zaokr w dół)

    return gcd, x, y
#test:
gcd, x, y = extended_gcd(17, 3120)

print("NWD:", gcd)
print("x:", x)
print("y:", y)

print(17 * x + 3120 * y) #powinno być 1

# odwrotność modularna
def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)

    if gcd != 1:
        raise ValueError("Nie istnieje bo NWD(a,m) != 1")

    return x % m

d = mod_inverse(17, 3120)
print(d)  # 2753



# Szybkie potęgowanie modularne - metoda kwadratów i mnożeń
def modular_power(base, exponent, modulus):
    result = 1
    base %= modulus

    while exponent > 0:

        if exponent % 2 == 1:
            result = (result * base) % modulus

        base = (base * base) % modulus
        exponent //= 2
    return result

# 3^13 mod 7:
print(modular_power(3, 13, 7))  # 3

#działające tak samo wbudowane w python
pow(3, 13, 7)



# Dzielenie próbne do pierwiastka z n
# bo jedno musi być < sqrt(n)
import math
def is_prime(n):
    if n < 2:
        return False

# math.isqrt() zwraca całkowitą część pierwiastka z liczby
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False

    return True

print(is_prime(53), is_prime(61), is_prime(15), is_prime(1)) 
# T T F F



# Tekst -> bajty
message = "OK".encode("utf-8") # b'OK'

# Bajty -> liczba
data = bytes.fromhex("0102")
number = int.from_bytes(data, byteorder="big") # 258
# odwrotnie
number = 258
data = number.to_bytes(2, byteorder="big")
data.hex() # 0102


# Tekst na liczbę (tekst -> bajty -> liczba)
message = "abc"
message_bytes = message.encode("utf-8")
message_number = int.from_bytes(message_bytes, byteorder="big")
# odwrotnie
recovered_bytes = message_number.to_bytes(len(message_bytes), byteorder="big")
recovered_message = recovered_bytes.decode("utf-8") # abc



"""
Podręcznikowe RSA: 
Szyfrowanie c = m^e % n,  deszyfrowanie m = c^d % n  (gdzie 0 <= m < n)
nie ma elementów losowych więc taka sama wiadomość -> taki sam szyfrogram
Dopełnienie OAEP  dodaje tą losowość
"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

private_key = RSA.generate(2048)
public_key = private_key.public_key()

cipher = PKCS1_OAEP.new(
    public_key,
    hashAlgo=SHA256,
    mgfunc=lambda seed, length:
        PKCS1_OAEP.MGF1(seed, length, SHA256)
    # mgfunc - funkcja maskująca MGF1
)
# szyfrowanie
message = b"Wiadomosc"
ciphertext = cipher.encrypt(message)

#deszyfrowanie
decryptor = PKCS1_OAEP.new(
    private_key,
    hashAlgo=SHA256,
    mgfunc=lambda seed, length:
        PKCS1_OAEP.MGF1(seed, length, SHA256)
)
plaintext = decryptor.decrypt(ciphertext) 
print(plaintext) # b"Wiadomosc"

"""
Limit długości wiadomości RSA-OAEP:
mLen <= k - 2*hLen - 2
mLen – maksymalna długość wiadomości (w bajtach)
k – długość modułu RSA (w bajtach)
hLen – długość skrótu (w bajtach)

Dla SHA-256 (hLen=32):
RSA 2048 (k=2048/8) - 190
RSA 3072 (k=3072/8) - 384
"""


# Podpis cyfrowy RSA-PSS
# skrót SHA-256, MGF1, długość soli
# Weryfikacja kluczem publicznym.
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pss

private_key = RSA.generate(2048)
public_key = private_key.public_key()

message = b"Wiadomosc"

hash_object = SHA256.new(message) # Obliczenie skrótu SHA-256

# Tworzenie podpisu
signer = pss.new(
    private_key,
    mask_func=lambda seed, length:
        pss.MGF1(seed, length, SHA256),
    salt_bytes=32
)

signature = signer.sign(hash_object)
print("Podpis:", signature.hex())


# Weryfikacja
from Crypto.Signature import pss
from Crypto.Hash import SHA256

# Ponownie obliczamy skrót wiadomości
hash_object = SHA256.new(message)

verifier = pss.new(
    public_key,
    mask_func=lambda seed, length:
        pss.MGF1(seed, length, SHA256),
    salt_bytes=32
)

try:
    verifier.verify(hash_object, signature)
    print("Poprawny")

except (ValueError, TypeError):
    print("Niepoprawny")


#modyfikacja
modified_message = b"Podmienilem wiadomosc"
modified_hash = SHA256.new(modified_message)

verifier.verify(modified_hash, signature) # będzie wyjątek


"""
Szyfrowanie hybrydowe – RSA + AES-256-GCM
RSA - wolny i ograniczona długość
AES - szybki ale symetryczny
więc 
AES szyfruje wiadomość, a RSA losowy klucz do aes
AES-256 = klucz 32 Bajty

Osoba 1:
1. Generuje losowy klucz AES o długości 256 bitów.
2. Generuje nonce dla AES-GCM.
3. Szyfruje wiadomość przy pomocy AES-GCM.
4. Szyfruje klucz AES za pomocą RSA-OAEP i publicznego klucza Osoby2.
5. Wysyła zaszyfrowany klucz AES, nonce, szyfrogram AES i tag.
Osoba 2:
1. Odszyfrowuje klucz AES swoim kluczem prywatnym RSA.
2. Otrzymuje oryginalny klucz AES.
3. Wykorzystuje go do odszyfrowania wiadomości.
4. Sprawdza poprawność tagu uwierzytelniającego.

AES-GCM zapewnia jednocześnie:
- poufność – szyfruje wiadomość
- integralność – wykrywa zmiany w danych
- uwierzytelnienie – pozwala sprawdzić, czy dane nie zostały zmodyfikowane

Nonce to nietajna wartość wykorzystywana przy szyfrowaniu, u nas 12 Bajtów
Tag to wartość, która pozwala sprawdzić integralność danych, u nas 16 Bajtów
"""
# Kompletny program szyfrowania hybrydowego RSA + AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


# GENEROWANIE KLUCZY RSA
private_key = RSA.generate(2048)
public_key = private_key.public_key()


# FUNKCJA SZYFRUJĄCA RSA-OAEP
def rsa_encrypt(data, public_key):

    cipher = PKCS1_OAEP.new(
        public_key,
        hashAlgo=SHA256,
        mgfunc=lambda seed, length:
            PKCS1_OAEP.MGF1(seed, length, SHA256)
    )

    return cipher.encrypt(data)


# FUNKCJA DESZYFRUJĄCA RSA-OAEP
def rsa_decrypt(data, private_key):

    cipher = PKCS1_OAEP.new(
        private_key,
        hashAlgo=SHA256,
        mgfunc=lambda seed, length:
            PKCS1_OAEP.MGF1(seed, length, SHA256)
    )

    return cipher.decrypt(data)


# SZYFROWANIE HYBRYDOWE
def encrypt_message(message, public_key):

    aes_key = get_random_bytes(32) # 1. Generowanie klucza AES-256 i nonce
    nonce = get_random_bytes(12)

    # 3. Szyfrowanie wiadomości AES-GCM
    aes_cipher = AES.new(
        aes_key,
        AES.MODE_GCM,
        nonce=nonce,
        mac_len=16
    )

    ciphertext, tag = aes_cipher.encrypt_and_digest(message)

    # 4. Szyfrowanie klucza AES RSA-OAEP
    encrypted_aes_key = rsa_encrypt(
        aes_key,
        public_key
    )

    return {
        "encrypted_aes_key": encrypted_aes_key,
        "nonce": nonce,
        "ciphertext": ciphertext,
        "tag": tag
    }


# DESZYFROWANIE HYBRYDOWE
def decrypt_message(encrypted_data, private_key):

    # 1. Odszyfrowanie klucza AES za pomocą RSA
    aes_key = rsa_decrypt(
        encrypted_data["encrypted_aes_key"],
        private_key
    )

    # 2. Odtworzenie obiektu AES-GCM
    aes_cipher = AES.new(
        aes_key,
        AES.MODE_GCM,
        nonce=encrypted_data["nonce"],
        mac_len=16
    )

    # 3. Odszyfrowanie i sprawdzenie tagu
    plaintext = aes_cipher.decrypt_and_verify(
        encrypted_data["ciphertext"],
        encrypted_data["tag"]
    )

    return plaintext


# TEST
message = "Tajna wiadomość dla odbiorcy!".encode("utf-8")

# Szyfrowanie
encrypted_data = encrypt_message(
    message,
    public_key
)

print("Wiadomość została zaszyfrowana.")

# Deszyfrowanie
decrypted_message = decrypt_message(
    encrypted_data,
    private_key
)

print("Odszyfrowana wiadomość:")
print(decrypted_message.decode("utf-8"))



""" Formaty kluczy:
PEM
- tekstowa reprezentacja danych binarnych
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCg... <- Base64
-----END PUBLIC KEY-----

SubjectPublicKeyInfo
- struktura przechowująca klucz publiczny
- Dla RSA zawiera m.in.  informację o algorytmie, moduł n, wykładnik publiczny e.

PKCS#8
Może przechowywać klucz bez szyfrowania
-----BEGIN PRIVATE KEY-----
lub z szyfrowaniem zabezpieczonym hasłem
-----BEGIN ENCRYPTED PRIVATE KEY-----
Wykorzystuje PBKDF2 i PBES2
"""
# Możemy również utworzyć zaszyfrowany klucz prywatny 
# bezpośrednio w Pythonie:
from Crypto.PublicKey import RSA

private_key = RSA.generate(2048)

encrypted_pem = private_key.export_key(
    format="PEM",
    pkcs=8,
    passphrase=b"moje_silne_haslo",
    protection="PBKDF2WithHMAC-SHA512AndAES256-CBC"
)

with open("private_encrypted.pem", "wb") as f:
    f.write(encrypted_pem)


# wczytanie
with open("private_encrypted.pem", "rb") as f:
    data = f.read()

key = RSA.import_key(
    data,
    passphrase=b"moje_silne_haslo"
)

print(key.has_private())  # True


# Publiczny:
public_key = private_key.public_key()
public_pem = public_key.export_key(format="PEM")
with open("public.pem", "wb") as f:
    f.write(public_pem)

with open("public.pem", "rb") as f:
    public_data = f.read()
public_key = RSA.import_key(public_data)
print(public_key.has_private())  # False