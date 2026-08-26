import time
from crypto.keygen2 import generate_K1
from crypto.encrypt import encrypt_message
from stego.embed import embed_bits

def to_bits(data: bytes):
    return ''.join(f'{b:08b}' for b in data)

# Read message from frontend

message = b"Anandhi is getting married"
image_path = "image/context.jpg"

timestamp_window = int(time.time() // 10)

K1 = generate_K1(timestamp_window, image_path)
payload = encrypt_message(message, K1)

# Add payload size header (4 bytes)
payload_size = len(payload)
size_bytes = payload_size.to_bytes(4, byteorder='big')

full_payload = size_bytes + payload
bitstream = to_bits(full_payload)
embed_bits("audio/input.wav", "audio/stego.wav", bitstream)

print("Stego audio generated.")
print("Timestamp window:", timestamp_window)
print("Image context used:", image_path)
