from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import hmac
import hashlib

def encrypt_message(message: bytes, K1: bytes):
    nonce = get_random_bytes(16)
    K2 = hashlib.sha256(nonce).digest()
    key = hashlib.sha256(K1 + K2).digest()

    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message, AES.block_size))

    payload_core = cipher.iv + nonce + ciphertext

    tag = hmac.new(K1, payload_core, hashlib.sha256).digest()

    return payload_core + tag
