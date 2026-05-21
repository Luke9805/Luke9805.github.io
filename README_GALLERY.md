# 🖼️ Gallery Dinamica - Documentazione Completa

Sistema di sincronizzazione automatica tra Google Drive e GitHub Pages. Aggiungi/rimuovi foto dal Drive e il sito si aggiorna automaticamente.

---

## 📋 Indice

1. [🎯 Panoramica](#panoramica)
2. [🚀 Setup Iniziale (Una volta)](#setup-iniziale)
3. [💻 Uso Locale](#uso-locale)
4. [⚙️ Automazione GitHub Actions](#automazione-github-actions)
5. [🔧 Troubleshooting](#troubleshooting)
6. [❓ FAQ](#faq)

---

## 🎯 Panoramica

Questo sistema permette di:

✅ **Aggiungere/rimuovere foto dal Google Drive**
✅ **Rigenerare automaticamente il `gallery-config.json`**
✅ **Mantenere il sito sempre sincronizzato** senza toccare il codice
✅ **Aggiornamenti manuali o automatici** (ogni giorno)
✅ **Totalmente compatibile con GitHub Pages** (statico al 100%)

### Come funziona

```
Tu aggiungi foto su Google Drive
            ↓
GitHub Actions le legge (automaticamente o manualmente)
            ↓
Genera il gallery-config.json
            ↓
Il sito si aggiorna automaticamente con le foto nuove
```

---

## 🚀 Setup Iniziale (Una volta sola)

### 1️⃣ Creare Progetto Google Cloud (5 minuti)

#### Step A: Nuovo Progetto
1. Vai a: **https://console.cloud.google.com/**
2. Login con il tuo account Google
3. In alto a sinistra → **"Seleziona progetto"** → **"Nuovo progetto"**
4. Nome: `"Luca Photography Gallery"` (o come preferisci)
5. Clicca **"Crea"** e aspetta ~30 secondi

#### Step B: Attiva Google Drive API
1. Menu a sinistra → **"API e servizi"** → **"Libreria"**
2. Cerca: **"Google Drive API"**
3. Clicca sul risultato → **"Attiva"**

#### Step C: Crea Credenziali OAuth
1. Menu a sinistra → **"API e servizi"** → **"Credenziali"**
2. Clicca **"+ Crea credenziali"** → **"ID client OAuth"**
3. Se chiede "Schermata di consenso":
   - **"Configura schermata di consenso"**
   - Scegli **"Esterno"**
   - **"Crea"**
   - Riempi i campi: Nome app, email supporto
   - **"Salva e continua"** (saltando i rest)
4. Torna a **Credenziali** → **"+ Crea credenziali"** → **"ID client OAuth"**
5. Tipo: **"Applicazione desktop"** → **"Crea"**
6. **Scarica il file JSON**

#### Step D: Setup Utente di Test
1. Menu a sinistra → **"Schermata di consenso OAuth"**
2. Scorri a **"Utenti di test"**
3. **"+ Aggiungi utenti"**
4. Incolla la tua **email Google** → **"Aggiungi"**

#### Step E: Metti le Credenziali nel Progetto
1. Rinomina il file scaricato in: **`credentials.json`**
2. Mettilo nella **cartella principale** del progetto:

```
Luke9805.github.io/
├── credentials.json          ← QUI!
├── generate_gallery_config.py
├── gallery_folders.json
├── gallery-config.json
└── ... altri file
```

⚠️ **Importante**: `credentials.json` è nel `.gitignore`, non sarà mai pushato su GitHub

---

### 2️⃣ Configurare gli ID delle Cartelle Google Drive

1. Apri il file: **`gallery_folders.json`**
2. Per ogni categoria, prendi l'ID dalla URL del Drive:
   - Apri la cartella su Google Drive
   - URL: `https://drive.google.com/drive/folders/QUESTO_E_L_ID`
   - Copia l'ID e incollalo nel file

**Esempio:**
```json
{
  "folders": {
    "Compleanni": {
      "id": "1a2b3c4d5e6f7g8h9i0j",
      "description": "Foto di compleanni"
    },
    "Ritratti": {
      "id": "2b3c4d5e6f7g8h9i0j1k",
      "description": "Ritratti fotografici"
    },
    "Varie": {
      "id": "3c4d5e6f7g8h9i0j1k2l",
      "description": "Foto varie"
    },
    "Esibizioni": {
      "id": "4d5e6f7g8h9i0j1k2l3m",
      "description": "Esibizioni e eventi"
    }
  }
}
```

---

## 💻 Uso Locale

### Prima Esecuzione

#### Opzione 1: Windows (Più Facile)
1. Doppio click su **`update-gallery.bat`**
2. Si apre una finestra, aspetta che finisca
3. Se chiede di autenticarsi su Google:
   - Accedi con il tuo account Google
   - Autorizza l'accesso
4. ✅ File `gallery-config.json` generato

#### Opzione 2: Mac/Linux
```bash
chmod +x update-gallery.sh
./update-gallery.sh
```

#### Opzione 3: Manuale (Qualsiasi OS)
```bash
# Installa dipendenze
pip install -r requirements.txt

# Esegui lo script
python generate_gallery_config.py
```

### Cosa Fa lo Script

- Legge le foto da ogni cartella Google Drive configurata
- Estrae gli ID delle immagini
- Crea `gallery-config.json` con tutte le foto
- Salva le credenziali in `token.json` (per riusi futuri)

### Dopo la Prima Esecuzione

```bash
git add gallery-config.json
git commit -m "🖼️ Initial gallery config from Google Drive"
git push
```

---

## ⚙️ Automazione GitHub Actions

Il workflow si trova in: **`.github/workflows/update-gallery.yml`**

### Quando si Attiva

✅ **Ogni giorno a mezzanotte UTC** (0:00)
✅ **Quando fai push** di file di configurazione
✅ **Manualmente** da GitHub quando vuoi

### Come Attivare Manualmente

1. Vai su GitHub → Repository
2. Tab **"Actions"**
3. Seleziona **"🔄 Update Gallery Config"**
4. Clicca **"Run workflow"**
5. Aspetta 2-3 minuti
6. ✅ Sito aggiornato

### Opzione: Automazione Completa (GitHub Actions con Credenziali)

Se vuoi che il workflow aggiorni il sito **automaticamente** senza intervento:

1. **Copia il contenuto di `credentials.json`**
2. Vai su GitHub → Repository → **Settings** → **Secrets and variables** → **Actions**
3. **"New repository secret"**:
   - Nome: `GOOGLE_DRIVE_CREDENTIALS`
   - Valore: (incolla il contenuto di `credentials.json`)
4. **"Add secret"**
5. ✅ Il workflow adesso può autenticarsi automaticamente!

Adesso il workflow partirà automaticamente:
- **Ogni giorno a mezzanotte** e scansionerà le foto nuove
- **Quando modifichi** file di configurazione
- **Manualmente** quando lo attivi tu

### Controllare lo Stato del Workflow

1. GitHub → Repository
2. **"Actions"** tab
3. Vedrai lo storico di tutte le esecuzioni
4. Clicca su una per vedere i log dettagliati

---

## 🔧 Troubleshooting

### Errore: "Folder not found" o "Invalid folder ID"

**Causa**: L'ID cartella è sbagliato o la cartella non è accessibile

**Soluzione**:
1. Verifica l'ID dalla URL di Google Drive (copia bene!)
2. Verifica che la cartella sia nel tuo account e accessibile
3. Riprova lo script

---

### Errore: "Authentication failed"

**Causa**: Credenziali scadute o non configurate correttamente

**Soluzione**:
1. Elimina il file `token.json` se esiste
2. Elimina il file `credentials.json`
3. Scarica di nuovo `credentials.json` da Google Cloud
4. Esegui di nuovo lo script

---

### Il workflow non parte su GitHub

**Causa**: Secret non configurato o file di configurazione non sincronizzato

**Soluzione**:
1. Verifica che il secret `GOOGLE_DRIVE_CREDENTIALS` sia nel repository (Settings → Secrets)
2. Fai un push di un file di configurazione per triggerare il workflow
3. O attivalo manualmente da GitHub Actions

---

### Le foto non si vedono sul sito

**Causa**: Workflow ancora in elaborazione, cache del browser, o file non aggiornato

**Soluzione**:
1. Aspetta 2-3 minuti che il workflow finisca (controlla GitHub Actions)
2. Aggiorna il browser: **Ctrl+Shift+R** (Windows) o **Cmd+Shift+R** (Mac)
3. Verifica che `gallery-config.json` sia stato aggiornato
4. Controlla che le foto nel Drive siano immagini valide (jpg, png, gif, etc)

---

### Errore: "The caller does not have permission to access"

**Causa**: L'app Google non è autorizzata per il tuo account

**Soluzione**:
1. Torna a Google Cloud Console
2. **API e servizi** → **Schermata di consenso OAuth**
3. Scorri a **"Utenti di test"**
4. **"+ Aggiungi utenti"**
5. Aggiungi la tua email

---

## ❓ FAQ

### D: Quanto tempo impiega l'aggiornamento?

A: **2-3 minuti** per il workflow completo. Visualizza il progresso in GitHub Actions.

---

### D: Cosa succede se aggiungo una foto con lettere speciali nel nome?

A: **Funziona perfettamente!** UTF-8 è completamente supportato (accenti, emoji, etc).

---

### D: Posso avere sottocartelle dentro le cartelle?

A: Lo script legge solo le immagini nella **cartella radice**. Se metti foto in sottocartelle, non verranno trovate. Soluzione: metti tutte le foto direttamente nella cartella principale.

---

### D: Quante foto posso avere per cartella?

A: Google Drive API supporta fino a **1000 file per cartella**. Se ne hai più, contattami per una soluzione custom.

---

### D: Posso cambiare l'ordine delle foto?

A: Lo script le ordina **alfabeticamente per nome**. Se vuoi un ordine specifico, rinomina le foto con numeri all'inizio (01, 02, 03, etc).

---

### D: Cosa succede se elimino una foto dal Drive?

A: La prossima volta che il workflow parte, la foto viene rimossa da `gallery-config.json` e non appare più sul sito.

---

### D: Posso usare questo su siti diversi da GitHub Pages?

A: Sì! Lo script genera semplicemente un JSON. Puoi usarlo con qualsiasi hosting statico.

---

### D: È sicuro mettere il secret su GitHub?

A: **Totalmente sicuro**. GitHub cripta i secrets e li decripta solo durante l'esecuzione del workflow. Non vengono mai esposti nei log.

---

### D: Posso avere più siti con lo stesso progetto Google?

A: Sì, crea più repository e usa lo stesso progetto Google Cloud con secret diversi per ogni repo.

---

## 📁 Struttura del Progetto

```
Luke9805.github.io/
├── .github/
│   ├── workflows/
│   │   └── update-gallery.yml      # GitHub Actions workflow
│   └── README.md                    # Info workflow
├── credentials.json                 # 🔐 Google credentials (non committare!)
├── token.json                       # 🔐 Token cache (non committare!)
├── generate_gallery_config.py       # Script principale
├── gallery_folders.json             # Config cartelle Drive
├── gallery-config.json              # Output (foto da mostrare)
├── update-gallery.bat               # Helper Windows
├── update-gallery.sh                # Helper Mac/Linux
├── requirements.txt                 # Dipendenze Python
├── README_GALLERY.md                # 📖 Questa documentazione
├── gallery-window.html              # Viewer foto
├── index.html                       # Home page
├── about.html                       # Chi sono
├── contact.html                     # Contatti
├── equipment.html                   # Attrezzatura
└── readme.md                        # README del sito
```

---

## 🔐 Sicurezza e Best Practices

✅ **Credenziali**:
- `credentials.json` è nel `.gitignore` (non salvato su GitHub)
- `token.json` è nel `.gitignore` (non salvato su GitHub)
- Usa GitHub Secrets per l'automazione

✅ **API Quotas**:
- Google Drive API ha limiti generosi per uso personale
- Lo script è ottimizzato per non fare richieste inutili

✅ **Privacy**:
- Solo le foto nel Drive sono visibili sul sito
- Condividi il Drive solo con chi vuoi che veda le foto

---

## 🆘 Hai Problemi?

1. **Controlla i log**: GitHub → Actions → Workflow run → Logs
2. **Elimina cache**: Cancella `token.json` e riprova
3. **Verifica config**: Controlla che `gallery_folders.json` sia corretto
4. **Prova localmente**: Esegui lo script in locale per testare

---

## 📚 Risorse Esterne

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Drive API Docs](https://developers.google.com/drive)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitHub Pages Docs](https://pages.github.com/)

---

**Ultimo aggiornamento**: Maggio 2026
**Versione**: 1.0
