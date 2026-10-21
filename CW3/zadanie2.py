from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

def encrypt_decrypt(data, password, salt, iv):
    key = PBKDF2(
        password,
        salt,
        dkLen=32,
        count=200_000,
        hmac_hash_module=SHA256
    )

    print("Dlugosc poczatkowa:", len(data))

    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(pad(data, AES.block_size))

    print("Dlugosc kryptogramu:", len(encrypted))
    print("Kryptogram:", encrypted.hex())

    decipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(
        decipher.decrypt(encrypted),
        AES.block_size
    )
    print("Czy jest takie samo po odszyfrowaniu:", data == plaintext)


password = "haslo testowe".encode("utf-8")
salt = get_random_bytes(16)
iv = get_random_bytes(16)

print("\nDane = puste dane:")
data = b""
encrypt_decrypt(data, password, salt, iv)

print("\nDane = 0123456789ABCDEF:")
data = b"0123456789ABCDEF"
encrypt_decrypt(data, password, salt, iv)

print("\nDane = wiadomosc.txt:")
data = open("wiadomosc.txt", "rb").read()
encrypt_decrypt(data, password, salt, iv)

print("\nDane = wiadomosc.txt z nową solą i iv:")
salt = get_random_bytes(16)
iv = get_random_bytes(16)
encrypt_decrypt(data, password, salt, iv)