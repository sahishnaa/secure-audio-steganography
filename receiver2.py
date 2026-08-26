import time, hmac, hashlib
from crypto.keygen2 import generate_K1
from crypto.decrypt import decrypt_message
from stego.extract import extract_bits

def bits_to_bytes(bits):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

START = 5000

# Step 1: Extract first 32 bits (payload size)
size_bits = extract_bits("audio/stego.wav", 32)
size_bytes = bits_to_bytes(size_bits)
payload_size = int.from_bytes(size_bytes, byteorder='big')

print("Payload size:", payload_size)

# Step 2: Extract full payload
total_bits = 32 + payload_size * 8
bits = extract_bits("audio/stego.wav", total_bits)
payload = bits_to_bytes(bits[32:])

payload_core = payload[:-32]
recv_tag = payload[-32:]

image_path = "image/context.jpg"
current_window = int(time.time() // 10)

for delta in range(-30, 31):
    candidate_ts = current_window + delta
    K1 = generate_K1(candidate_ts, image_path)

    calc_tag = hmac.new(K1, payload_core, hashlib.sha256).digest()
    if not hmac.compare_digest(calc_tag, recv_tag):
        continue

    message = decrypt_message(payload_core, K1)
    print("Recovered message:", message.decode())
    print("Timestamp window used:", candidate_ts)
    print("Image context:", image_path)
    break
else:
    print("Decryption failed.")
