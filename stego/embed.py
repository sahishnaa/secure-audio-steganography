from scipy.io import wavfile
import numpy as np

def embed_bits(audio_path, output_path, bitstream):
    rate, audio = wavfile.read(audio_path)

    # Use only one channel if stereo
    if audio.ndim == 2:
        audio = audio[:, 0]

    audio = audio.astype(np.int16).copy()

    if len(bitstream) > len(audio):
        raise ValueError("Audio too short for payload")

    START = 5000
    for i, bit in enumerate(bitstream):
        audio[START + i] = (audio[START + i] & ~1) | int(bit)

    wavfile.write(output_path, rate, audio)
