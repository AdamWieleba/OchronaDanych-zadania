
# Test wczytania klucza prywatnego
# openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -aes-256-cbc -pass pass:test -out test.pem

from Crypto.PublicKey import RSA

with open("test.pem", "rb") as f:
    key_data = f.read()

# Wczytanie klucza z hasłem
private_key = RSA.import_key(
    key_data,
    passphrase=b"test"
)

print("Klucz wczytany poprawnie.")
print("Długość:", private_key.size_in_bits())
print("Czy zawiera klucz prywatny:", private_key.has_private())