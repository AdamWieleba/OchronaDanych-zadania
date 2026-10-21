#(py/) python -m pip install pycryptodome
#pip3 install też może działać, jeśli pip3 jest dostępny

#Program: PBKDF2-HMAC-SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

password = "moje haslo".encode("utf-8")
salt = get_random_bytes(16)

key = PBKDF2(
    password,
    salt,
    dkLen=32,
    count=10000,
    hmac_hash_module=SHA256
)

print(len(key))  # 32
print(key.hex())




#Program: entropia shannona w rozkładzie bajtów
from collections import Counter
from math import log2

def shannon_entropy(data):
    if len(data) == 0:
        return 0.0

    counts = Counter(data)
    total = len(data)

    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * log2(p)

    return entropy

data = open("demo24.bmp", "rb").read()
print(shannon_entropy(data))




#Program: AES-CBC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(16)
data = b"To sa dane do zaszyfrowania."

# Szyfrowanie
iv = get_random_bytes(16)
aes = AES.new(key, AES.MODE_CBC, iv)
encrypted = aes.encrypt(pad(data, AES.block_size))

# Zachowujemy IV obok szyfrogramu
encrypted_file_data = iv + encrypted

# Odszyfrowanie
stored_iv = encrypted_file_data[:16]
stored_encrypted = encrypted_file_data[16:]

decipher = AES.new(key, AES.MODE_CBC, stored_iv)
plaintext = unpad(
    decipher.decrypt(stored_encrypted),
    AES.block_size
)

print(plaintext)




#Program AES-ECB: podany_plik -> [+] plik_zaszyfrowany -> [+] plik_odszyfrowany
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

if len(sys.argv) != 2:
    print("Użycie: python aes_file.py obraz.bmp")
    sys.exit(1)

nazwa = sys.argv[1]

try:
    with open(nazwa, "rb") as plik:
        dane = plik.read()
except FileNotFoundError:
    print("Błąd: plik nie istnieje.")
    sys.exit(1)

# Generowanie klucza AES-128
klucz = get_random_bytes(16)

# Szyfrowanie AES w trybie ECB
szyfr = AES.new(klucz, AES.MODE_ECB)
kryptogram = szyfr.encrypt(pad(dane, AES.block_size))

with open(nazwa + ".encrypted", "wb") as plik:
    plik.write(kryptogram)

# Odszyfrowanie kryptogramu
deszyfr = AES.new(klucz, AES.MODE_ECB)
odszyfrowane = unpad(
    deszyfr.decrypt(kryptogram),
    AES.block_size
)

with open(nazwa + ".decrypted", "wb") as plik:
    plik.write(odszyfrowane)

print("Zapisano:", nazwa + ".encrypted")
print("Zapisano:", nazwa + ".decrypted")
print("Czy dane są identyczne:", dane == odszyfrowane)






# Najpierw zainstaluj bibliotekę:
# pip install pycryptodome

# Atak brute force na AES-128. Program zakłada, że kryptogram został zaszyfrowany w trybie AES-ECB z dopełnieniem PKCS#7. 
# Klucz ma 16 bajtów, a odszyfrowany tekst powinien być poprawnym tekstem UTF-8.
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from itertools import product
from math import log2
from collections import Counter


# Alfabet, z którego budujemy kolejne klucze.
ALPHABET = b"ab"

# AES-128 wymaga klucza o długości dokładnie 16 bajtów.
KEY_LENGTH = 16
MAX_ITERATIONS = 1000

# Próg entropii wykorzystywany jako wskaźnik diagnostyczny.
MIN_ENTROPY = 2.0

# Czy wypisywać szczegóły każdej próby? True / False
VERBOSE = False


def shannon_entropy(data):

    if not data:
        return 0.0

    # Counter(data) zlicza, ile razy wystąpił każdy bajt.
    # Przykład: b"AAB" daje {65: 2, 66: 1}.
    counts = Counter(data)

    # Liczba wszystkich bajtów w analizowanych danych.
    total = len(data)

    entropy = 0.0

    # Iterujemy po liczbie wystąpień poszczególnych bajtów.
    for count in counts.values():

        # Prawdopodobieństwo = liczność bajtu / liczba wszystkich bajtów
        probability = count / total
        entropy -= probability * log2(probability)

    return entropy



def looks_like_text(data):
    # Sprawdza, czy dane można zdekodować jako UTF-8 i czy nie zawierają wielu znaków sterujących.

    try:
        # Próbujemy przekształcić bajty na tekst Unicode.
        text = data.decode("utf-8")

    except UnicodeDecodeError:
        # Niepoprawny UTF-8: odrzucamy tego kandydata.
        return False

    # Dopuszczamy znaki drukowalne oraz typowe białe znaki, nowe linie, tabulatory.
    return all(
        character.isprintable() or character in "\n\r\t"
        for character in text
    )


# GENEROWANIE KOLEJNYCH KANDYDATÓW NA KLUCZ
def generate_keys(alphabet, key_length):

    # product(*[alphabet] * key_length) tworzy iloczyn
    # kartezjański alfabetu z samym sobą key_length razy.
    # bytes(...) łączy wartości bajtowe w jeden klucz.
    for combination in product(alphabet, repeat=key_length):
        yield bytes(combination)


def brute_force_aes_ecb(ciphertext,
                        alphabet=ALPHABET,
                        key_length=KEY_LENGTH,
                        max_iterations=MAX_ITERATIONS):
    """
    Testuje kolejnych kandydatów na klucz AES-ECB.

    Zakładamy:
    - AES-ECB,
    - dopełnienie PKCS#7,
    - tekst jawny zakodowany w UTF-8.

    Zwraca znaleziony klucz i tekst albo None.
    Entropia jest tylko wskaźnikiem diagnostycznym.
    """

    if not ciphertext or len(ciphertext) % AES.block_size != 0:
        raise ValueError(
            "Szyfrogram musi być niepusty i mieć długość będącą wielokrotnością 16 bajtów."
        )

    iterations = 0

    for key in generate_keys(alphabet, key_length):

        if iterations >= max_iterations:
            print("Osiągnięto limit prób.")
            break

        iterations += 1

        try:
            # Tworzymy obiekt AES-ECB dla aktualnego klucza.
            cipher = AES.new(key, AES.MODE_ECB)

            # Odszyfrowujemy szyfrogram do postaci bajtów.
            decrypted_padded = cipher.decrypt(ciphertext)

            # Usuwamy PKCS#7 (dopełnienie)
            plaintext = unpad(
                decrypted_padded,
                AES.block_size
            )

        except ValueError:
            # Błędne dopełnienie: przechodzimy do następnego kandydata.
            continue

        entropy = shannon_entropy(plaintext)

        text_candidate = looks_like_text(plaintext)

        if VERBOSE:
            print(
                f"Próba {iterations}: "
                f"klucz={key.hex()}, "
                f"entropia={entropy:.3f}, "
                f"tekst={text_candidate}"
            )

        # Próg entropii jako filtr.
        if text_candidate and entropy >= MIN_ENTROPY:

            # Zamieniamy tekstowe bajty na napis UTF-8.
            text = plaintext.decode("utf-8")

            print("\nKandydat spełnił warunki heurystyki.")
            print(f"Liczba prób: {iterations}")
            print(f"Klucz w zapisie hex: {key.hex()}")
            print(f"Entropia: {entropy:.3f} bitów/bajt")
            print(f"Wynik: {text!r}")

            # Zwracamy klucz i odszyfrowane dane.
            return key, plaintext

    # Jeśli pętla nie znalazła kandydata, zwracamy None.
    print(f"Brak dobrych wyników po {iterations} próbach.")
    return None


# URUCHOMIENIE 
if __name__ == "__main__":  # sprawdza, czy plik Pythona jest uruchamiany bezpośrednio, a nie importowany jako moduł.

    # Tutaj należy podać rzeczywisty szyfrogram w bajtach
    ciphertext = b""

    if not ciphertext:
        print(
            "Uzupełnij zmienną ciphertext rzeczywistym szyfrogramem AES-ECB z dopełnieniem PKCS#7."
        )
    else:
        brute_force_aes_ecb(ciphertext)







#fragmenty program rc4 ze sprawdzaniem wszystkich kluczy
if len(sys.argv) != 2:
    print("Użycie: python skrypt.py rc4.bin")
    sys.exit(1)

with open(sys.argv[1], "rb") as plik:
    kryptogram = plik.read()

# [...]
tekst = rc4(kryptogram, klucz)

with open("rc4.txt", "wb") as plik:
    plik.write(tekst)


# Zapamiętujemy czas rozpoczęcia przeszukiwania kluczy, time.time() zwraca aktualny czas w sekundach.
poczatek = time.time()

ranking = []

# Pobieramy pierwsze 512 bajtów kryptogramu. Sprawdzamy tylko początek żeby przyspieszyć przeszukiwanie.
fragment = kryptogram[:512]

liczba_prob = 0 #liczba sprawdzonych kluczy

# Generujemy wszystkie możliwe kombinacje trzech małych liter alfabetu.
# repeat=3 oznacza, że każdy klucz ma dokładnie 3 litery. aaa, aab, aac, .., zzz
for litery in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=3):

    # Łączymy trzy litery w jeden napis. Następnie zamieniamy napis na bajty ASCII bo RC4 przyjmuje klucz w postaci bajtów.
    # repeat=3 losuje litery[] "abc", które zamieniamy -> b"abc"
    klucz = "".join(litery).encode("ascii")

    # Próbujemy odszyfrować pierwsze 512 bajtów kryptogramuprzy użyciu aktualnie sprawdzanego klucza.
    # Funkcja RC4 generuje nowy stan dla każdego wywołania.
    tekst = rc4(fragment, klucz)

    # Obliczamy entropię odszyfrowanych danych (bajtów). W tym zadaniu niższa entropia może wskazywać na tekst, w którym częściej występują niektóre znaki.
    h = entropia(tekst)

    # Dopisujemy do listy parę: (entropia, klucz zapisany jako zwykły napis)
    ranking.append((h, klucz.decode("ascii")))

    # Zwiększamy licznik sprawdzonych kluczy o jeden.
    liczba_prob += 1

# Sortujemy wyniki rosnąco.
# Najpierw porównywana jest entropia.
# Jeśli dwa klucze mają taką samą entropię, porównywane są alfabetycznie.
ranking.sort()

# Obliczamy czas przeszukiwania w sekundach, tzn odejmujemy czas rozpoczęcia od aktualnego czasu.
czas = time.time() - poczatek

print("\nRanking pięciu kandydatów:")

# Pobieramy pięć pierwszych elementów posortowanej listy. Są to klucze o najniższej entropii.
for h, klucz in ranking[:5]:
    print(klucz, round(h, 6)) # round(h, 6) zaokrągla entropię do 6 miejsc po przecinku.

# Wybieramy pierwszy klucz z rankingu.
# ranking[0] oznacza pierwszy element listy.
# ranking[0][1] pobiera z tej pary sam klucz, a nie entropię.
# Na końcu zamieniamy napis na bajty ASCII.
klucz = ranking[0][1].encode("ascii") #bajty

# Wyświetlamy automatycznie wybrany klucz.
# decode("ascii") zamienia bajty z powrotem na napis.
print("\nWybrany klucz:", klucz.decode("ascii")) #napis

# Wyświetlamy liczbę sprawdzonych kluczy.
# Powinno ich być 26 * 26 * 26 = 17576.
print("Liczba prób:", liczba_prob)

# Wyświetlamy czas przeszukiwania w sekundach, zaokr do 3 miejsc po przecinku.
print("Czas przeszukiwania:", round(czas, 3), "s")




#Program do szyfrowania obrazu z isod:
# >>> from BMPcrypt import encrypt_data
# >>> from BMPcrypt import encrypt_full
# >>> encrypt_data("demo24.bmp", "ECB", b"x" * 16) 
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
 
def nullpadding(data, length=16):
    return data + b"\x00"*(length-len(data) % length) 
 
def convert_to_RGB(data):
    pixels = []

    for i in range(0, len(data) - 1, 3):
        r = int(data[i])
        g = int(data[i+1])
        b = int(data[i+2])

        pixels.append((r,g,b))
    return pixels

def encrypt_full(input_filename, mode, key):
    img_in = open(input_filename, "rb")
    data = img_in.read()
    
    data_padded = nullpadding(data)

    if mode == "CBC":
        iv = get_random_bytes(16)
        aes = AES.new(key, AES.MODE_CBC, iv)
    elif mode == "ECB":
        aes = AES.new(key, AES.MODE_ECB)
 
    encrypted_data = aes.encrypt(data_padded)
    encrypted_data_unpadded = encrypted_data[:len(data)]
    
    name = ''.join(input_filename.split('.')[:-1])
    img_format = str(input_filename.split('.')[-1])

    output_filename = name + '_' + mode + '_encrypted.' + img_format

    img_out = open(output_filename, "wb")
    img_out.write(encrypted_data_unpadded)
    img_out.close()
    img_in.close()

def encrypt_data(input_filename, mode, key):
    img_in = Image.open(input_filename)
    data = img_in.convert("RGB").tobytes() 
 
    data_padded = nullpadding(data)

    if mode == "CBC":
        iv = get_random_bytes(16)
        aes = AES.new(key, AES.MODE_CBC, iv)
    elif mode == "ECB":
        aes = AES.new(key, AES.MODE_ECB)
 
    encrypted_data = aes.encrypt(data_padded)
    encrypted_data_unpadded = encrypted_data[:len(data)]
    img_out = Image.new(img_in.mode, img_in.size)
    img_out.putdata(convert_to_RGB(encrypted_data_unpadded))
    
    name = ''.join(input_filename.split('.')[:-1])
    img_format = str(input_filename.split('.')[-1])

    output_filename = name + '_' + mode + '_encrypted.' + img_format
    img_out.save(output_filename, img_format)




#RC4 z poprzedniego
import sys
import time
import math
import itertools
from collections import Counter


def rc4(dane, klucz):
    S = list(range(256))
    j = 0

    # KSA
    for i in range(256):
        j = (j + S[i] + klucz[i % len(klucz)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA i XOR
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


def entropia(dane):
    if len(dane) == 0:
        return 0.0

    licznik = Counter(dane)
    h = 0.0

    for liczba in licznik.values():
        p = liczba / len(dane)
        h -= p * math.log2(p)

    return h


if len(sys.argv) != 2:
    print("Użycie: python skrypt.py rc4.bin")
    sys.exit(1)

with open(sys.argv[1], "rb") as plik:
    kryptogram = plik.read()

# Test poprawności RC4
test = b"Test RC4"
klucz_testowy = b"abc"

print("Test RC4:",
      rc4(rc4(test, klucz_testowy), klucz_testowy) == test)

# Sprawdzanie wszystkich kluczy
poczatek = time.time()
ranking = []
fragment = kryptogram[:512]
liczba_prob = 0

for litery in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=3):
    klucz = "".join(litery).encode("ascii")
    tekst = rc4(fragment, klucz)
    h = entropia(tekst)

    ranking.append((h, klucz.decode("ascii")))
    liczba_prob += 1

ranking.sort()
czas = time.time() - poczatek

print("\nRanking pięciu kandydatów:")
for h, klucz in ranking[:5]:
    print(klucz, round(h, 6))

klucz = ranking[0][1].encode("ascii")

print("\nWybrany klucz:", klucz.decode("ascii"))
print("Liczba prób:", liczba_prob)
print("Czas przeszukiwania:", round(czas, 3), "s")

# Odszyfrowanie całego pliku
tekst = rc4(kryptogram, klucz)

with open("rc4.txt", "wb") as plik:
    plik.write(tekst)

print("\nPoczątek tekstu:")
print(repr(tekst[:200]))

print("\nEntropia kryptogramu:", round(entropia(kryptogram), 6))
print("Entropia tekstu:", round(entropia(tekst), 6))

print("Zgodność szyfrowania:",
      rc4(tekst, klucz) == kryptogram)



