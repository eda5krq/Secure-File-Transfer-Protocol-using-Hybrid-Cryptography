import socket
import os
import json

from crypto.rsa import generate_rsa_keys, serialize_public_key, load_public_key_from_bytes, rsa_decrypt
from crypto.aes import send_msg, recv_msg
from handlers.upload import server_upload
from handlers.download import server_download

HOST = '127.0.0.1'
PORT = 5005
STORAGE_DIR = "server_storage"

def exchange_keys(conn, server_private_key, server_public_key):
    print("[*] Faza 1: Shkëmbimi i çelësave...")
    send_msg(conn, serialize_public_key(server_public_key))
    print("    -> Çelësi publik i serverit u dërgua.")

    client_public_key = load_public_key_from_bytes(recv_msg(conn))
    print("    -> Çelësi publik i klientit u mor.")

    aes_key = rsa_decrypt(server_private_key, recv_msg(conn))
    print("    -> Çelësi AES u dekriptua.")
    print("[+] Faza 1 KOMPLETUAR!\n")

    return aes_key, client_public_key