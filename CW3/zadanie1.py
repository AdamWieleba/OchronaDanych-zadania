from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


key = b"000102030405060708090a0b0c0d0e0f"

data = "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF".encode("ascii")


ecb = AES.new(key, AES.MODE_ECB)
ecb_encrypted = ecb.encrypt(data)

iv = get_random_bytes(16)
cbc = AES.new(key, AES.MODE_CBC, iv)
cbc_encrypted = cbc.encrypt(data)

print(ecb_encrypted.hex())
print(cbc_encrypted.hex())

ecb_decipher = AES.new(key, AES.MODE_ECB)
plaintext = ecb_decipher.decrypt(ecb_encrypted)
print(plaintext)

cbc_decipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cbc_decipher.decrypt(cbc_encrypted)
print(plaintext)



