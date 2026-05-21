# ⚡ Quick Start - Setup 5 Minuti

## Step 1️⃣ Google Cloud Setup (2 minuti)

```
1. Vai a: https://console.cloud.google.com/
2. Crea nuovo progetto
3. Attiva "Google Drive API"
4. Crea credenziali OAuth → Desktop app
5. Scarica JSON e salva come `credentials.json`
```

## Step 2️⃣ Configurazione Cartelle (1 minuto)

Apri `gallery_folders.json`:
```json
{
  "folders": {
    "Compleanni": {
      "id": "COPIA_ID_DALLA_URL",
      "description": "..."
    }
  }
}
```

Come trovare l'ID:
- Apri cartella su Google Drive
- URL: `https://drive.google.com/drive/folders/QUESTO_E_L_ID`

## Step 3️⃣ Esecuzione Locale (1 minuto)

### Windows
```bash
update-gallery.bat
```

### Mac/Linux
```bash
chmod +x update-gallery.sh
./update-gallery.sh
```

### Manuale (qualsiasi OS)
```bash
pip install -r requirements.txt
python generate_gallery_config.py
```

## Step 4️⃣ Automazione (1 minuto - Opzionale)

Se vuoi aggiornamenti automatici:

1. Copia il contenuto di `credentials.json`
2. Vai su GitHub → Repo → Settings → Secrets
3. Nuovo secret: `GOOGLE_DRIVE_CREDENTIALS` = (incolla contenuto)
4. ✅ Fatto! Si aggiornerà ogni giorno automaticamente

## 🎯 Pronto!

Da adesso:
- ✅ Aggiungi foto al Google Drive
- ✅ Il sito si aggiorna automaticamente (o manualmente eseguendo update-gallery)
- ✅ Niente da modificare a mano nel sito

---

📚 Per documentazione completa: vedi `GALLERY_SETUP.md`
