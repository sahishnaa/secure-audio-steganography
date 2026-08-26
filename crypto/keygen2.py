import hashlib
from crypto.image_context import image_fingerprint

BRAILLE_MAP = {
    '0': '001010', '1': '010110', '2': '000001', '3': '011011',
    '4': '001001', '5': '010011', '6': '000011',
    '7': '011001', '8': '010001', '9': '001011'
}

SECRET = b"opsec_shared_secret"

def generate_K1(timestamp_window: int, image_path: str) -> bytes:
    ts = str(timestamp_window)
    braille_bits = ''.join(BRAILLE_MAP[d] for d in ts)

    img_hash = image_fingerprint(image_path)

    data = SECRET + braille_bits.encode() + img_hash
    return hashlib.sha256(data).digest()
