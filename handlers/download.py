import os
import json
import hashlib

from crypto.rsa import sign_data, verify_signature
from crypto.aes import aes_encrypt, aes_decrypt, send_msg, recv_msg

STORAGE_DIR  = "server_storage"
DOWNLOAD_DIR = "client_downloads"


def server_download(conn, aes_key: bytes, server_private_key, filename: str):
    
    print(f"[*] Klienti kërkon '{filename}'...")
    file_path = os.path.join(STORAGE_DIR, os.path.basename(filename))

    if not os.path.exists(file_path):
        send_msg(conn, b"ERROR: File not found")
        print(f"[!] Skedari '{filename}' nuk u gjet.")
        return

    send_msg(conn, b"OK")

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    file_hash = hashlib.sha256(plaintext).hexdigest()
    signature = sign_data(server_private_key, bytes.fromhex(file_hash))

    meta = {"hash": file_hash, "signature": signature.hex()}
    send_msg(conn, json.dumps(meta).encode())

    iv, tag, ciphertext = aes_encrypt(aes_key, plaintext)
    send_msg(conn, iv)
    send_msg(conn, tag.hex().encode())
    send_msg(conn, ciphertext)
    print(f"[+] Skedari '{filename}' u dërgua.")


def client_download(sock, aes_key: bytes, server_public_key, filename: str):
    
    command = {"action": "download", "filename": filename}
    send_msg(sock, json.dumps(command).encode())

    response = recv_msg(sock).decode()
    if response.startswith("ERROR"):
        print(f"[!] {response}")
        return
    print(f"[*] Serveri po dërgon '{filename}'...")

    meta = json.loads(recv_msg(sock).decode())
    file_hash_hex = meta["hash"]
    signature_hex = meta["signature"]

    iv = recv_msg(sock)
    tag = bytes.fromhex(recv_msg(sock).decode())
    ciphertext = recv_msg(sock)

    plaintext = aes_decrypt(aes_key, iv, tag, ciphertext)
    print(f"    -> Skedari u dekriptua ({len(plaintext)} bytes).")

    computed_hash = hashlib.sha256(plaintext).hexdigest()
    if computed_hash != file_hash_hex:
        print("[!] GABIM: Hash nuk përputhet!")
        return
    print("[+] Hash SHA-256: VERIFIKUAR")

    signature = bytes.fromhex(signature_hex)
    if not verify_signature(server_public_key, signature, bytes.fromhex(file_hash_hex)):
        print("[!] GABIM: Nënshkrimi i serverit nuk është valid!")
        return
    print("[+] Nënshkrimi i serverit: VERIFIKUAR")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    save_path = os.path.join(DOWNLOAD_DIR, filename)
    with open(save_path, 'wb') as f:
        f.write(plaintext)
    print(f"[+] Skedari u ruajt: {save_path}")