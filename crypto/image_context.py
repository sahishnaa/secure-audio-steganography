import hashlib

def image_fingerprint(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).digest()
