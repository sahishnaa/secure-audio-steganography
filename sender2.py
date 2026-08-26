import time
from crypto.keygen2 import generate_K1
from crypto.encrypt import encrypt_message
from stego.embed import embed_bits
import wave
import numpy as np
import hashlib
def to_bits(data: bytes):
    return ''.join(f'{b:08b}' for b in data)

# Read message from frontend

with open("message.txt", "r") as f:
    message = f.read().encode()
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
import wave
import numpy as np
import hashlib

def analyze_audio():
    with wave.open("audio/input.wav", 'rb') as wf:
        orig = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)

    with wave.open("audio/stego.wav", 'rb') as wf:
        stego = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)

    diff = orig - stego

    print("\n--- AUDIO ANALYSIS ---")
    print("Total samples:", len(orig))
    print("Modified samples:", np.sum(orig != stego))
    print("Max difference:", np.max(np.abs(diff)))
    print("Min difference:", np.min(diff))

    # SNR
    noise = orig - stego
    snr = 10 * np.log10(np.sum(orig**2) / np.sum(noise**2))
    print("SNR:", round(snr, 2), "dB")

    # Hash comparison
    def file_hash(path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    print("\nOriginal SHA256:", file_hash("audio/input.wav"))
    print("Stego SHA256:   ", file_hash("audio/stego.wav"))

analyze_audio()


