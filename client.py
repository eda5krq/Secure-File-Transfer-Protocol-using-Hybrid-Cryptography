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

def main():
    print("=" * 55)
    print("   Secure File Transfer CLIENT")
    print("   RSA-2048 + AES-256-GCM + SHA-256 + RSA-PSS")
    print("=" * 55)

    print("[*] Duke gjeneruar çelësat RSA...")
    client_private_key, client_public_key = generate_rsa_keys()
    print("[+] Çelësat u gjeneruan.")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"[+] Lidhja e suksesshme me {HOST}:{PORT}\n")

            aes_key, server_public_key = exchange_keys(s, client_private_key, client_public_key)

            print("Zgjidhni një operacion:")
            print("  1. Ngarko skedar (Upload)")
            print("  2. Shkarko skedar (Download)")
            choice = input("\nZgjidhja juaj (1/2): ").strip()

            if choice == "1":
                file_path = input("Rruga e skedarit: ").strip()
                client_upload(s, aes_key, client_private_key, file_path)
            elif choice == "2":
                filename = input("Emri i skedarit: ").strip()
                client_download(s, aes_key, server_public_key, filename)
            else:
                print("[!] Zgjidhje e pavlefshme.")

    except ConnectionRefusedError:
        print(f"[!] Nuk mund të lidhemi me {HOST}:{PORT}.")
        print("[!] Sigurohuni që server.py është duke punuar.")
    except Exception as e:
        print(f"[!] Gabim: {e}")

if __name__ == "__main__":
    main()


    