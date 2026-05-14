import os
import struct

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def aes_encrypt(key: bytes, plaintext: bytes) -> tuple:
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv, encryptor.tag, ciphertext


def aes_decrypt(key: bytes, iv: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def send_msg(sock, data: bytes) -> None:
    length = struct.pack('>I', len(data))
    sock.sendall(length + data)


def recv_msg(sock) -> bytes:
    raw_len = _recv_exactly(sock, 4)
    if not raw_len:
        return b''
    length = struct.unpack('>I', raw_len)[0]
    return _recv_exactly(sock, length)


def _recv_exactly(sock, n: int) -> bytes:
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return b''
        data += packet
    return data