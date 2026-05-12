import os
import json
import hashlib

from crypto.rsa import sign_data, verify_signature
from crypto.aes import aes_encrypt, aes_decrypt, send_msg, recv_msg

STORAGE_DIR = "server_storage"

def client_upload(sock, aes_key: bytes, client_private_key, file_path: str):
    #klienti enkriton dhe e dergon skedarin te serveri
    filename = os.path.basename(file_path)

    if not os.path.exists(file_path):
        print(f"[!] Skedari '{file_path}' nuk ekziston!")
        return

    with open(file_path, 'rb') as f:
        plaintext = f.read()
    print(f"[*] '{filename}' u lexua ({len(plaintext)} bytes).")

    file_hash = hashlib.sha256(plaintext).hexdigest()
    print(f"[*] SHA-256: {file_hash[:32]}...")

    signature = sign_data(client_private_key, bytes.fromhex(file_hash))
    print("[*] Nënshkrimi dixhital u gjenerua.")

    command = {"action": "upload", "filename": filename}
    send_msg(sock, json.dumps(command).encode())

    meta = {"hash": file_hash, "signature": signature.hex()}
    send_msg(sock, json.dumps(meta).encode())

    iv, tag, ciphertext = aes_encrypt(aes_key, plaintext)
    print(f"[*] '{filename}' u enkriptua me AES-256-GCM.")
    send_msg(sock, iv)
    send_msg(sock, tag.hex().encode())
    send_msg(sock, ciphertext)

    response = recv_msg(sock).decode()
    if response.startswith("OK"):
        print(f"[+] '{filename}' u ngarkua me sukses!")
    else:
        print(f"[!] Gabim: {response}")


def server_upload(conn, aes_key: bytes, client_public_key, filename: str):
    #serveri e merr e dekripton verifikon dhe run skedarin
    print(f"[*] Duke marrë '{filename}'...")

    meta = json.loads(recv_msg(conn).decode())
    file_hash_hex = meta["hash"]
    signature_hex = meta["signature"]

    iv = recv_msg(conn)
    tag = bytes.fromhex(recv_msg(conn).decode())
    ciphertext = recv_msg(conn)

    plaintext = aes_decrypt(aes_key, iv, tag, ciphertext)
    print(f"    -> Skedari u dekriptua ({len(plaintext)} bytes).")

    computed_hash = hashlib.sha256(plaintext).hexdigest()
    if computed_hash != file_hash_hex:
        print("[!] GABIM: Hash nuk përputhet!")
        send_msg(conn, b"ERROR: Hash mismatch")
        return
    print("    -> Hash SHA-256: VERIFIKUAR")

    signature = bytes.fromhex(signature_hex)
    if not verify_signature(client_public_key, signature, bytes.fromhex(file_hash_hex)):
        print("[!] GABIM: Nënshkrimi i pavlefshëm!")
        send_msg(conn, b"ERROR: Invalid signature")
        return
    print("    -> Nënshkrimi dixhital: VERIFIKUAR")

    os.makedirs(STORAGE_DIR, exist_ok=True)
    save_path = os.path.join(STORAGE_DIR, os.path.basename(filename))
    with open(save_path, 'wb') as f:
        f.write(plaintext)
    print(f"[+] Skedari u ruajt: {save_path}")

    send_msg(conn, b"OK: File uploaded successfully")