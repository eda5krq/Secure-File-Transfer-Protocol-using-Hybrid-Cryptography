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


def handle_client(conn, addr, server_private_key, server_public_key):
    # koordinon krejt fazat per ni klient
    print(f"\n{'─' * 50}")
    print(f"[+] Klienti u lidh: {addr}")

    try:
        aes_key, client_public_key = exchange_keys(conn, server_private_key, server_public_key)

        print("[*] Faza 2: Duke pritur komandën...")
        command = json.loads(recv_msg(conn).decode())

        action = command.get("action")
        filename = command.get("filename")

        print(f"    -> {action.upper()} | '{filename}'")

        if action == "upload":
            server_upload(conn, aes_key, client_public_key, filename)

        elif action == "download":
            server_download(conn, aes_key, server_private_key, filename)

        else:
            send_msg(conn, b"ERROR: Unknown command")

    except Exception as e:
        print(f"[!] Gabim: {e}")

    finally:
        conn.close()
        print(f"[-] Lidhja me {addr} u mbyll.")
        print(f"{'─' * 50}")


def main():
    print("=" * 55)
    print("   Secure File Transfer SERVER")
    print("   RSA-2048 + AES-256-GCM + SHA-256 + RSA-PSS")
    print("=" * 55)

    print("[*] Duke gjeneruar çelësat RSA...")
    server_private_key, server_public_key = generate_rsa_keys()
    print("[+] Çelësat u gjeneruan.")

    os.makedirs(STORAGE_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)

        print(f"\n[*] Serveri po punon në {HOST}:{PORT}")
        print("[*] Duke pritur lidhje...\n")

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr, server_private_key, server_public_key)


if __name__ == "__main__":
    main()