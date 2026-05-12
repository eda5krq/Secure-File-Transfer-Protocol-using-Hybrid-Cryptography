import socket
import os

from crypto.rsa import generate_rsa_keys, serialize_public_key, load_public_key_from_bytes, rsa_encrypt
from crypto.aes import send_msg, recv_msg
from handlers.upload import client_upload
from handlers.download import client_download

HOST = '127.0.0.1'
PORT = 5005

def exchange_keys(sock, client_private_key, client_public_key):
    #shkembimi i qelsave me serverin
    print("[*] Faza 1: Shkëmbim çelësash...")

    server_public_key = load_public_key_from_bytes(recv_msg(sock))
    print("    -> Çelësi publik i serverit u mor.")

    send_msg(sock, serialize_public_key(client_public_key))
    print("    -> Çelësi publik i klientit u dërgua.")

    aes_key = os.urandom(32)
    send_msg(sock, rsa_encrypt(server_public_key, aes_key))
    print("    -> Çelësi AES u enkriptua dhe u dërgua.")
    print("[+] Faza 1 KOMPLETUAR!\n")

    return aes_key, server_public_key