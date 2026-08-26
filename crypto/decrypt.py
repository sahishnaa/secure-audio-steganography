import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_message(payload: bytes, K1: bytes):
    iv = payload[:16]
    nonce = payload[16:32]
    ciphertext = payload[32:]

    K2 = hashlib.sha256(nonce).digest()
    key = hashlib.sha256(K1 + K2).digest()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)
