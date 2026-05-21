@echo off
REM Script per aggiornare la galleria dal Google Drive (Windows)
REM

echo.
echo ============================================
echo     🖼️  Gallery Config Generator
echo ============================================
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trovato!
    echo Scaricalo da: https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python trovato
echo.

REM Installa dipendenze se necessario
echo 📦 Controllando dipendenze Python...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Errore nell'installazione dei pacchetti
    pause
    exit /b 1
)

echo ✅ Dipendenze aggiornate
echo.

REM Esegui lo script
echo 🚀 Generando configurazione galleria...
echo.
python generate_gallery_config.py

if errorlevel 1 (
    echo.
    echo ❌ Errore durante la generazione
    pause
    exit /b 1
)

echo.
echo ✅ Completato!
echo.
echo 📝 Prossimi passi:
echo    1. Verifica gallery-config.json
echo    2. Esegui: git add gallery-config.json
echo    3. Esegui: git commit -m "Update gallery config"
echo    4. Esegui: git push
echo.
pause
