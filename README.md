# Django Trainingsplaner

## 🚀 Projekt-Setup & Lokale Entwicklung

### Repository klonen & in das Projektverzeichnis wechseln
```bash
git checkout django-initial-push
```

### Virtuelle Umgebung erstellen und aktivieren
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### Datenbank vorbereiten
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional für Admin-Zugang
```

### Server starten
```bash
python manage.py runserver
```
Die App läuft jetzt unter **http://127.0.0.1:8000/** 🚀

## 📁 Wichtige Ordner & Dateien
```bash
.
├── config/         # Django-Projektkonfiguration
├── training/       # Haupt-App mit Views, Models, Templates
├── templates/      # HTML-Templates
├── static/         # Statische Dateien (CSS, JS, Bilder)
├── manage.py       # Django-CLI-Tool
├── requirements.txt # Paketabhängigkeiten
└── README.md       # Diese Datei
```

## 🛠 Nützliche Befehle
### Django Shell starten
```bash
python manage.py shell
```

### Django Admin-Panel aufrufen
```bash
http://127.0.0.1:8000/admin/
```

