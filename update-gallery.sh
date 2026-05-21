#!/bin/bash

# Script per aggiornare la galleria dal Google Drive (macOS/Linux)

echo ""
echo "============================================"
echo "     🖼️  Gallery Config Generator"
echo "============================================"
echo ""

# Verifica se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python non trovato!"
    echo "Installa Python da: https://www.python.org/"
    exit 1
fi

echo "✅ Python trovato"
echo ""

# Installa dipendenze
echo "📦 Controllando dipendenze Python..."
pip3 install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Errore nell'installazione dei pacchetti"
    exit 1
fi

echo "✅ Dipendenze aggiornate"
echo ""

# Esegui lo script
echo "🚀 Generando configurazione galleria..."
echo ""
python3 generate_gallery_config.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Errore durante la generazione"
    exit 1
fi

echo ""
echo "✅ Completato!"
echo ""
echo "📝 Prossimi passi:"
echo "   1. Verifica gallery-config.json"
echo "   2. Esegui: git add gallery-config.json"
echo "   3. Esegui: git commit -m 'Update gallery config'"
echo "   4. Esegui: git push"
echo ""
