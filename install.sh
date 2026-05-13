#!/bin/bash

echo "🔧 Rendszerfüggőségek telepítése..."
sudo apt update
sudo apt install -y python3 python3-pip python3-tk ffmpeg git

echo "📦 Python csomagok telepítése..."
python3 -m pip install --upgrade pip
python3 -m pip install --break-system-packages -r requirements.txt

echo "✅ Telepítés kész! Indíthatod a programot."

