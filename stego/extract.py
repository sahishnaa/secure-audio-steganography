from scipy.io import wavfile
import numpy as np

def extract_bits(audio_path, bit_len):
    rate, audio = wavfile.read(audio_path)

    # Use the same channel as embedding
    if audio.ndim == 2:
        audio = audio[:, 0]

    audio = audio.astype(np.int16)

    bits = ""
    START = 5000
    for i in range(bit_len):
        bits += str(audio[START + i] & 1)

    return bits
