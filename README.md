# Secure-File-Transfer

## Përshkrimi i Projektit

Secure File Transfer është një aplikacion client-server i zhvilluar në Python që mundëson transferimin e sigurt të file-ve përmes komunikimit me sockets. Projekti është ndërtuar duke përdorur konceptin e hybrid encryption, ku RSA-2048 përdoret për shkëmbimin e sigurt të çelësave, ndërsa AES-256-GCM përdoret për enkriptimin dhe dekriptimin e file-ve gjatë transferimit.

Gjatë procesit të komunikimit, klienti dhe serveri gjenerojnë çelësa RSA publik dhe privat. Pas shkëmbimit të çelësave publik, klienti krijon një AES session key i cili enkriptohet me RSA dhe dërgohet te serveri. Pas kësaj, të gjitha të dhënat transferohen duke përdorur AES encryption për siguri dhe performancë më të lartë.

Për të garantuar integritetin dhe autenticitetin e file-ve, projekti përdor SHA-256 hashing dhe RSA-PSS digital signatures. Para transferimit gjenerohet hash i file-it dhe nënshkruhet dixhitalisht, ndërsa pala pranuese verifikon hash-in dhe nënshkrimin për të siguruar që file nuk është modifikuar gjatë transmetimit.

Aplikacioni mbështet upload dhe download të file-ve midis klientit dhe serverit dhe është i organizuar në module të ndara për kriptografi, komunikim dhe menaxhim të file-ve për ta bërë kodin më të pastër dhe më të lehtë për mirëmbajtje.

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

Fillimisht startojmë serverin në një terminal:

https://github.com/user-attachments/assets/1165855b-bf9e-4a49-8dd7-1feb8cc701da

Pastaj startojmë klientin në terminalin tjetër:

https://github.com/user-attachments/assets/3b6f92e2-7676-45c6-a6ae-d5c2d325e426

Pas lidhjes së suksesshme me serverin, përdoruesi mund të zgjedhë një nga operacionet e mëposhtme:

- **Ngarko file (Upload)**  

  Nëse përdoruesi zgjedh opsionin `1`, aplikacioni kërkon rrugën e file që dëshiron të ngarkojë. Pas zgjedhjes së file, klienti e lexon përmbajtjen e tij, gjeneron hash-in SHA-256 dhe krijon nënshkrimin dixhital. Më pas file enkriptohet me AES-256-GCM dhe dërgohet në mënyrë të sigurt te serveri. Pas pranimit dhe verifikimit të file, serveri e ruan atë në folderin `server_storage`, i cili krijohet automatikisht nëse nuk ekziston.

  <img width="526" height="246" alt="image" src="https://github.com/user-attachments/assets/a035b182-e247-4955-841d-054bc7e1f7a0" />


- **Shkarko file (Download)**  

  Nëse përdoruesi zgjedh opsionin `2`, aplikacioni kërkon emrin e file që dëshiron të shkarkojë nga serveri. Serveri e gjen file, e enkripton me AES-256-GCM dhe e dërgon te klienti së bashku me hash-in SHA-256 dhe nënshkrimin dixhital. Klienti e dekripton file, verifikon integritetin dhe autenticitetin e tij, dhe më pas e ruan në folderin `client_downloads`, i cili krijohet automatikisht nëse nuk ekziston.

  <img width="705" height="239" alt="image" src="https://github.com/user-attachments/assets/923458c4-40f2-4608-8809-91d415f63f28" />

Në anën e serverit, pas lidhjes së klientit fillon faza e shkëmbimit të çelësave, ku serveri dërgon çelësin publik RSA, pranon çelësin publik të klientit dhe dekripton AES session key të dërguar nga klienti. Pas përfundimit të kësaj faze, krijohet një komunikim i sigurt midis klientit dhe serverit.

Në rastin e operacionit `UPLOAD`, serveri pret file-in nga klienti, e dekripton atë duke përdorur AES-256-GCM dhe verifikon hash-in SHA-256 dhe nënshkrimin dixhital për të siguruar integritetin dhe autenticitetin e file-it. Pas verifikimit, file ruhet në folderin `server_storage`.

  <img width="568" height="351" alt="image" src="https://github.com/user-attachments/assets/d40e87bf-01c4-4456-9356-7b18492eb45d" />

Në rastin e operacionit `DOWNLOAD`, serveri pranon kërkesën e klientit për një file specifik, e lexon skedarin nga `server_storage`, e enkripton dhe e dërgon te klienti së bashku me hash-in dhe nënshkrimin dixhital për verifikim.

  <img width="543" height="284" alt="image" src="https://github.com/user-attachments/assets/d57416f1-2198-46b0-8b4f-4c5741cc8c47" />
