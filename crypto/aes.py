import os
import struct

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def _validate_aes_key(key: bytes):
    # AES-256 kerkon çeles prej saktesisht 32 bytes
    if not isinstance(key, bytes):
        raise TypeError("AES key must be bytes")

    if len(key) != 32:
        raise ValueError("AES-256 key must be exactly 32 bytes")


def aes_encrypt(key: bytes, plaintext: bytes) -> tuple:
    # Enkripton te dhenat me AES-256-GCM
    _validate_aes_key(key)

    if not isinstance(plaintext, bytes):
        raise TypeError("Plaintext must be bytes")

    iv = os.urandom(12)

    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return iv, encryptor.tag, ciphertext


def aes_decrypt(key: bytes, iv: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    # Dekripton te dhenat me AES-256-GCM
    _validate_aes_key(key)

    if len(iv) != 12:
        raise ValueError("Invalid IV length for AES-GCM")

    if len(tag) != 16:
        raise ValueError("Invalid GCM tag length")

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()


def send_msg(sock, data: bytes) -> None:
    # Dergon mesazh permes socket duke ia vendosur gjatesine perpara
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")

    length = struct.pack(">I", len(data))
    sock.sendall(length + data)


def recv_msg(sock) -> bytes:
    # Merr mesazh nga socket duke lexuar se pari gjatësine
    raw_len = _recv_exactly(sock, 4)
    length = struct.unpack(">I", raw_len)[0]

    return _recv_exactly(sock, length)


def _recv_exactly(sock, n: int) -> bytes:
    # Lexon n bytes nga socket
    data = b""

    while len(data) < n:
        packet = sock.recv(n - len(data))

        if not packet:
            raise ConnectionError("Connection closed while receiving data")

        data += packet

    return data