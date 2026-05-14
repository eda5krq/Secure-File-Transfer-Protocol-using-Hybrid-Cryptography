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