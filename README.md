# AURA-MCOMM

### Context-Aware Secure Audio Steganography for Covert Communication

AURA-MCOMM is a secure communication system that combines **AES encryption, audio steganography, contextual key derivation, and HMAC-SHA256 integrity verification** to hide encrypted messages inside ordinary audio files.

The system is designed around a simple idea:

> The message should be encrypted, hidden inside an ordinary audio file, and the encryption key should never need to be transmitted.

Instead of exchanging a conventional encryption key, the sender and receiver independently derive the same key using a shared **time window** and a **context-image fingerprint**. This allows the resulting audio file to be shared without carrying the encryption key with it.

---

## Features

- 🔐 **AES encryption** of the message before embedding
- 🎵 **LSB audio steganography** for hiding the encrypted payload inside WAV audio
- 🖼️ **Context-image fingerprinting** as part of key derivation
- ⏱️ **Time-based key derivation** using a shared time window
- 🛡️ **HMAC-SHA256 integrity verification**
- 🚫 **No explicit key exchange**
- ❌ Wrong context image or incorrect time window results in safe rejection
- 🌐 Web-based sender and receiver interfaces using Flask
- 📊 Audio modification analysis and waveform visualization
- 🔄 Complete sender → stego audio → receiver pipeline

---

## Problem

Conventional encryption protects the contents of a message, but the encrypted communication itself can still be visible.

Steganography solves a different part of the problem by hiding information inside an apparently ordinary media file. However, a steganographic system without strong encryption can expose the hidden message if the embedding mechanism is discovered.

AURA-MCOMM combines both approaches:

**Encryption + Steganography + Context-based Key Derivation + Integrity Verification**

The project specifically addresses the following requirements:

1. Hide the existence of the communication inside an ordinary audio file.
2. Encrypt the message before embedding it.
3. Avoid transmitting the encryption key.
4. Bind the key to shared contextual information.
5. Verify message integrity before attempting decryption.
6. Reject incorrect context without exposing plaintext.

---

## System Overview

The communication pipeline is:

```text
                    SENDER
                       │
                       ▼
              Plaintext Message
                       │
                       ▼
              Context + Time Window
                       │
                       ▼
                Key Derivation
                       │
                       ▼
                 AES Encryption
                       │
                       ▼
                 HMAC-SHA256
                       │
                       ▼
              Encrypted Payload
                       │
                       ▼
              LSB Audio Embedding
                       │
                       ▼
                 Stego Audio
                    (.wav)
                       │
                       │
                 Transfer
                       │
                       ▼
                   RECEIVER
                       │
                       ▼
             Context Image + Time
                       │
                       ▼
                Key Derivation
                       │
                       ▼
              LSB Payload Extraction
                       │
                       ▼
                HMAC Verification
                   /          \
                PASS          FAIL
                 │              │
                 ▼              ▼
          AES Decryption     Reject
                 │
                 ▼
          Recovered Message
