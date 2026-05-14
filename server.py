import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def aes_encrypt(key: bytes, plaintext: bytes) -> tuple:
    # enkripton skedarin me AES-256-GCM
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv, encryptor.tag, ciphertext


def aes_decrypt(key: bytes, iv: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    # dekripton skedarin me AES-256-GCM
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()