# 🖼️ Gallery Config Setup Guide

Guida completa per configurare il sistema di sincronizzazione dinamica tra Google Drive e GitHub Pages.

## 📋 Panoramica

Questo sistema permette di:
- ✅ Aggiungere/rimuovere foto dal Google Drive
- ✅ Rigenerare automaticamente il `gallery-config.json`
- ✅ Mantenere il sito sempre sincronizzato senza toccare il codice
- ✅ Utilizzare GitHub Actions per automazione completa

## 🚀 Setup Iniziale (Una volta sola)

### Step 1: Creare un Progetto Google Cloud

1. Vai a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto (es. "Luca Photography Gallery")
3. **Attiva Google Drive API**:
   - Menu hamburger → API e servizi → Libreria
   - Cerca "Google Drive API"
   - Clicca e premi "Attiva"

### Step 2: Creare Credenziali OAuth

1. Vai a **API e servizi** → **Credenziali**
2. Clicca **+ Crea credenziali** → **ID client OAuth**
3. Seleziona **Applicazione desktop**
4. Scarica il file JSON (salva come `credentials.json`)
5. Metti il file nella **root del progetto**

```
Luke9805.github.io/
├── credentials.json          ← Metti qui!
├── generate_gallery_config.py
├── gallery_folders.json
└── gallery-config.json
```

### Step 3: Configurare gli ID delle Cartelle

1. Apri `gallery_folders.json`
2. Per ogni categoria, prendi l'ID della cartella dal Google Drive:
   - Apri la cartella in Google Drive
   - L'URL sarà: `https://drive.google.com/drive/folders/FOLDER_ID_QUI`
   - Copia l'ID

Esempio:
```json
{
  "folders": {
    "Compleanni": {
      "id": "1a2b3c4d5e6f7g8h9i0j",
      "description": "Foto di compleanni"
    },
    "Ritratti": {
      "id": "2b3c4d5e6f7g8h9i0j1k",
      "description": "Ritratti"
    }
  }
}
```

## 💻 Uso Locale (Prima volta)

### 1. Installa dipendenze Python
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Esegui lo script
```bash
python generate_gallery_config.py
```

Questo genererà il `gallery-config.json` da zero.

### 3. Commit e Push
```bash
git add gallery-config.json
git commit -m "🖼️ Initial gallery config from Google Drive"
git push
```

## ⚙️ Automazione con GitHub Actions

### Opzione 1: Automazione Completa (Consigliato)

Se vuoi che il sito si **aggiorni automaticamente** ogni volta che modifichi il Google Drive:

1. **Copia il contenuto di `credentials.json`**
2. Vai su GitHub → Repository → **Settings** → **Secrets and variables** → **Actions**
3. Crea un nuovo secret: 
   - Nome: `GOOGLE_DRIVE_CREDENTIALS`
   - Valore: Incolla il contenuto di `credentials.json`
4. Il workflow si avvierà **ogni giorno a mezzanotte** e ogni volta che fai push

### Opzione 2: Manuale (Più Sicuro)

Se preferisci aggiornare manualmente:
1. Non aggiungere il secret
2. Esegui localmente: `python generate_gallery_config.py`
3. Fai push dei cambiamenti

## 📅 Il Workflow Automatico

Quando è configurato, il GitHub Actions:
- ✅ Parte **ogni giorno a mezzanotte UTC** (0:00 UTC)
- ✅ Esegue automaticamente quando modifichi i file di configurazione
- ✅ Legge le foto dal Google Drive
- ✅ Aggiorna `gallery-config.json`
- ✅ Fa commit automaticamente in GitHub
- ✅ Il sito GitHub Pages si aggiorna automaticamente

### Controllare lo stato del workflow

1. Vai su GitHub → Repository
2. Clicca su **Actions**
3. Vedrai lo storico di esecuzioni e log dettagliati

## 🔐 Sicurezza

- ⚠️ **NON** committare `credentials.json` su GitHub
- ⚠️ Aggiungi `credentials.json` al `.gitignore` (già fatto)
- ✅ Usa GitHub Secrets per le credenziali
- ✅ Le credenziali rimangono private nel GitHub Actions runner

## 🔧 Troubleshooting

### Errore: "Folder not found"
- Verifica che l'ID cartella sia corretto
- Verifica che la cartella sia condivisa/accessibile al tuo account

### Errore: "Authentication failed"
- Elimina `token.json` e rifai l'autenticazione
- Verifica che `credentials.json` sia nel posto giusto

### Il workflow non parte
- Controlla che il secret `GOOGLE_DRIVE_CREDENTIALS` sia configurato
- Vai su Actions per vedere i log di errore

### Le foto non si vedono sul sito
- Attendi 2-3 minuti che il GitHub Actions finisca
- Aggiorna la cache del browser (Ctrl+Shift+R)
- Verifica che le foto siano immagini (jpg, png, etc)

## 📝 Workflow Tipico (Dopo Setup)

**Quando vuoi aggiungere nuove foto:**

1. Vai su Google Drive
2. Apri la cartella (es. "Compleanni")
3. **Aggiungi le nuove foto** normalmente
4. **Aspetta**: Il workflow automatico partirà a mezzanotte (UTC)
   - Oppure attiva manualmente: GitHub → Actions → "🔄 Update Gallery Config" → "Run workflow"
5. **Fatto!** Il sito si aggiorna automaticamente

## 🎯 Dettagli Tecnici

- **Linguaggio**: Python 3
- **API**: Google Drive API v3
- **CI/CD**: GitHub Actions
- **Frequenza aggiornamento**: Giornaliera (mezzanotte UTC)
- **Trigger aggiuntivi**: Push su config file, workflow dispatch manuale

## ❓ Domande Frequenti

**D: Quanto tempo impiega l'aggiornamento?**
A: ~2-3 minuti. Visualizza i progressi in GitHub Actions.

**D: Cosa succede se aggiungo una foto con lettere speciali nel nome?**
A: Funziona perfettamente, UTF-8 è supportato.

**D: Posso avere sottocartelle dentro le cartelle?**
A: Lo script legge solo le immagini nella cartella radice. Sottocartelle vengono ignorate.

**D: Quante foto posso avere?**
A: Google Drive API supporta fino a 1000 file per cartella. Se ne hai più, faccelo sapere.

