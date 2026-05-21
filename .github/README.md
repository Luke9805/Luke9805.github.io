# 🔄 GitHub Actions Workflows

## Update Gallery Config

**File**: `workflows/update-gallery.yml`

### Cosa fa
Automaticamente legge le foto dal Google Drive e aggiorna il `gallery-config.json`

### Quando si attiva
- ⏰ **Giornalmente** a mezzanotte UTC (0:00)
- 🔄 Quando fai push di file di configurazione
- 🖱️ Manualmente da GitHub → Actions

### Come attivare manualmente
1. Vai su GitHub repository
2. **Actions** tab
3. Seleziona "🔄 Update Gallery Config"
4. Clicca "Run workflow"
5. Aspetta 2-3 minuti

### Configurazione richiesta
Nel repository settings → Secrets and variables → Actions:
```
GOOGLE_DRIVE_CREDENTIALS = <contenuto di credentials.json>
```

### Log e debug
Visualizza lo stato e gli errori in: **Actions** → Workflow run → Logs
