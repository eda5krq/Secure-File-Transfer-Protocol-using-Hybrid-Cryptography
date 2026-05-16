# Secure-File-Transfer

## Përshkrimi i Projektit

Secure File Transfer është një aplikacion client-server i zhvilluar në Python që mundëson transferimin e sigurt të file-ve përmes komunikimit me sockets. Projekti është ndërtuar duke përdorur konceptin e hybrid encryption, ku RSA-2048 përdoret për shkëmbimin e sigurt të çelësave, ndërsa AES-256-GCM përdoret për enkriptimin dhe dekriptimin e skedarëve gjatë transferimit.

Gjatë procesit të komunikimit, klienti dhe serveri gjenerojnë çelësa RSA publik dhe privat. Pas shkëmbimit të çelësave publik, klienti krijon një AES session key i cili enkriptohet me RSA dhe dërgohet te serveri. Pas kësaj, të gjitha të dhënat transferohen duke përdorur AES encryption për siguri dhe performancë më të lartë.

Për të garantuar integritetin dhe autenticitetin e file-ve, projekti përdor SHA-256 hashing dhe RSA-PSS digital signatures. Para transferimit gjenerohet hash i file-it dhe nënshkruhet dixhitalisht, ndërsa pala pranuese verifikon hash-in dhe nënshkrimin për të siguruar që file nuk është modifikuar gjatë transmetimit.

Aplikacioni mbështet upload dhe download të skedarëve midis klientit dhe serverit dhe është i organizuar në module të ndara për kriptografi, komunikim dhe menaxhim të file-ve për ta bërë kodin më të pastër dhe më të lehtë për mirëmbajtje.

## Teknologjitë e Përdorura

- Python 3
- Socket Programming
- Cryptography Library
- JSON

## Algoritmet e Sigurisë

- **RSA-2048**  
  Përdoret për shkëmbimin e sigurt të çelësave.

- **AES-256-GCM**  
  Përdoret për enkriptimin dhe dekriptimin e file-ve.

- **SHA-256**  
  Përdoret për verifikimin e integritetit të file-ve.

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
├── test.txt
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
├── .gitignore
└── README.md
```

## Ekzekutimi i Projektit

### 1. Krijimi i Virtual Environment

```bash
python -m venv venv
```

### 2. Aktivizimi i Virtual Environment

```
venv\Scripts\activate
```

### 3. Instalimi i Dependencies

```
pip install -r requirements.txt
```

### 4. Nisja e Serverit

Hapni një terminal dhe ekzekutoni:

```
python server.py
```

### 5. Nisja e Klientit

Hapni një terminal tjetër dhe ekzekutoni:

```
python client.py
```

## Shembuj të Ekzekutimit

