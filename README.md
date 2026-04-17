# Sprint 4: Gestor de Llibres
Fer per Javier Barberà

Aquest projecte consisteix a fer una aplicació per a la gestió d'1 dels 5 dominis que hi havia a l'enunciat. En aquest cas, és el domini d'un gestor de pel·lícules. Utilitzarem una arquitectura que utilitzarà un front-end (pàgina web) i back-end (api) per comunicar-nos amb una database al núvol.
Software utilitzat: Python11, FastAPI, MongoDB, Skeleton CSS.

---

# Estructura del projecte
```text
.
├── Comprovació del frontend.mp4   # Vídeo que demostra el funcionament
├── backend/
│   ├── app.py                 # Lògica del servidor FastAPI
│   └── requirements.txt       # Dependències del servidor FastAPI
├── frontend/
│   ├── index.html             # Interfície d'usuari
│   ├── style.css              # L'estil visual de la pàgina
│   ├── style_original.css     # L'estil original del front-end, sense el backbone de skeleton
│   └── app.js                 # Lògica de consum de l'API (Fetch)
└── tests/
    └── postman_API_tests.json  # Tests de l'API per a Postman
```

---

# Passos per a la instal·lació
El primer prerequisit seria tenir Python, jo tinc la versió 11 i pel que he comprovat és l'única que funciona, així que recomano instal·lar aquesta versió.

Una vegada tens Python 11, ves a la PowerShell i ubicat a la carpeta real del projecte per crear l'entorn virtual de Python. Una vegada allí, executa:

```text
py -m venv venv

.\venv\Scripts\Activate
```

Una vegada activat l'entorn, passem a instal·lar les dependències.
```text
pip install -r backend/requirements.txt
```

Ara ja ho tindríem tot preparat per a posar-ho en marxa, així que anirem dintre de la carpeta de back-end i l'executarem l'api amb aquestes comendes:
```text
cd backend

uvicorn app:app --reload
```

Si tot ha anat bé, quan obris el index.html podràs utilitzar-ho, com es mostra al vídeo de prova. En cas que uvicorn o altra dependència doni problemes, prova d'instal·lar-lo de manera manual:
```text
pip install fastapi uvicorn pymongo pydantic pydantic-settings email-validator certifi
```

---

# Postman
A la carpeta test hi ha un JSON per importar una col·lecció que conté un test CRUD de l'api, està configurat perquè no calgui canviar la id dels elements cada vegada als PATCH i DELETE.
