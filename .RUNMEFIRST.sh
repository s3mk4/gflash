#!/bin/bash

# gFlash v0.3.2 - Build script for Linux/macOS

echo "[*] gFlash Builder v0.3.2"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Install Python 3.7+ first."
    exit 1
fi

echo "[*] Installing dependencies..."
pip3 install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo "[*] Building executables..."
python3 build.py

if [ $? -ne 0 ]; then
    echo "[ERROR] Build failed"
    exit 1
fi

echo
echo "[OK] Build complete! Check dist/ folder"
