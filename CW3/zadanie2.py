from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

password = "haslo testowe".encode("utf-8")
salt = get_random_bytes(16)

def encrypt_decrypt(data, password, salt):
    key = PBKDF2(
        password,
        salt,
        dkLen=32,
        count=200_000,
        hmac_hash_module=SHA256
    )

    print(len(key))  # 32
    print(key.hex())

    print("Dlugosc poczatkowa:")
    print(len(data))

    iv = get_random_bytes(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(pad(data, AES.block_size))

    print("Dlugosc kryptogramu:")
    print(len(data))

    decipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(
        decipher.decrypt(encrypted),
        AES.block_size
    )
    print("Czy jest takie samo po odszyfrowaniu:")
    print(data == plaintext)


data = b""
encrypt_decrypt(data, password, salt)

data = b"0123456789ABCDEF"
encrypt_decrypt(data, password, salt)

data = open("wiadomosc.txt", "rb").read()
encrypt_decrypt(data, password, salt)