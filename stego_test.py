from stego.embed import embed_bits
from stego.extract import extract_bits

def to_bits(data: bytes):
    return ''.join(f'{b:08b}' for b in data)

def bits_to_bytes(bits):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

# Simple known payload
original = b"HELLO"
bits = to_bits(original)

embed_bits("audio/input.wav", "audio/stego_test.wav", bits)
extracted_bits = extract_bits("audio/stego_test.wav", len(bits))
recovered = bits_to_bytes(extracted_bits)

print("Original:", original)
print("Recovered:", recovered)
print("Bits match:", bits == extracted_bits)
