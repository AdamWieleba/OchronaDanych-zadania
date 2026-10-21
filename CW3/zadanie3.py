from Crypto.Cipher import AES
from collections import Counter
from math import log2

def entropy(data):

    byte_counts = Counter(data)
    total = len(data)
    entropy = 0.0

    for byte_count in byte_counts.values():

        probability = byte_count / total
        entropy -= probability * log2(probability)

    return round(entropy, 4)


data = open("slaby_ecb.bin", "rb").read()

chars = "abcdefghijklmnopqrstuvwxyz0123456789"

results = []

for char in chars:
    key = char.encode("ascii") * 16
    ecb_decipher = AES.new(key, AES.MODE_ECB)
    plaintext = ecb_decipher.decrypt(data[:4096])
    results.append((entropy(plaintext), char))

results.sort()

for h, char in results[:5]:
    print(f"Entropia: {h}, znak: {char}")

print(f"\nNajlepszy kandydat - entropia: {results[0][0]}, znak: {results[0][1]}")

key = results[0][1].encode("ascii") * 16
ecb_decipher = AES.new(key, AES.MODE_ECB)
plaintext = ecb_decipher.decrypt(data[:4096])

print("Odszyfrowany tekst:", plaintext.decode("ascii"))


