
import os
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

with open("klucz_podpisu.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

verifier = pss.new(
    public_key,
    mask_func=lambda seed, length: 
        pss.MGF1(seed, length, SHA256),
    salt_bytes=32
)

for filename in os.listdir("dokumenty"):

    if filename.endswith(".txt"):
        filepath = os.path.join("dokumenty", filename)
        signature_path = filepath + ".sig"

        try:
            with open(filepath, "rb") as f:
                hash = SHA256.new(f.read())

            with open(signature_path, "rb") as f:
                signature = f.read()

            verifier.verify(hash, signature)
            print(filename, "OK")

        except:
            print(filename, "BŁĄD")


# Podpis własnym kluczem
private_key = RSA.generate(3072)
public_key = private_key.public_key()

signer = pss.new(
    private_key,
    mask_func=lambda seed, length:
        pss.MGF1(seed, length, SHA256),
    salt_bytes=32
)

verifier = pss.new(
    public_key,
    mask_func=lambda seed, length: 
        pss.MGF1(seed, length, SHA256),
    salt_bytes=32
)

with open("moj_klucz_publiczny.pem", "wb") as f:
    f.write(public_key.export_key(format="PEM"))

message = "Laboratorium 8: AdamWieleba"

with open("podpis.txt", "wb") as f:
    f.write(message.encode("utf-8"))

with open("podpis.txt", "rb") as f:
    hash = SHA256.new(f.read())

signature = signer.sign(hash)

with open("podpis.txt.sig", "wb") as f:
    f.write(signature)

try:
    verifier.verify(hash, signature)
    print("\nWeryfikacja własnego podpisu: OK")
except:
    print("\nWeryfikacja własnego podpisu: BŁĄD")


# Zmiana jednego bajtu
with open("podpis.txt", "rb") as f:
    modified_message = bytearray(f.read())

modified_message[0] += 1

with open("podpis_kopia.txt", "wb") as f:
    f.write(modified_message)

modified_hash = SHA256.new(bytes(modified_message))

try:
    verifier.verify(modified_hash, signature)
    print("Weryfikacja zmienionego dokumentu: OK")
except:
    print("Weryfikacja zmienionego dokumentu: BŁĄD")
