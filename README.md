# Secure-File-Transfer

## Përshkrimi i Projektit

## Teknologjitë e Përdorura

- Python 3
- Socket Programming
- Cryptography Library
- JSON

## Algoritmet e Sigurisë

- **RSA-2048**  
  Përdoret për shkëmbimin e sigurt të çelësave.

- **AES-256-GCM**  
  Përdoret për enkriptimin dhe dekriptimin e skedarëve.

- **SHA-256**  
  Përdoret për verifikimin e integritetit të skedarëve.

- **RSA-PSS**  
  Përdoret për nënshkrime dixhitale dhe verifikim autenticiteti.

- **OAEP Padding**  
  Përdoret për siguri shtesë gjatë enkriptimit RSA.

## Struktura e Projektit

```
secure-file-transfer/
│
├── client.py
├── server.py
├── requirements.txt
│
├── crypto/
│   ├── aes.py
│   └── rsa.py
│
├── handlers/
│   ├── upload.py
│   └── download.py
│
├── server_storage/
│   └── (uploaded files)
│
├── client_downloads/
│   └── (downloaded files)
│
└── README.md
```

## Ekzekutimi i Projektit

## Shembuj të Ekzekutimit
