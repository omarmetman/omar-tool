#!/bin/bash
# Omar-tool setup script for Termux (English)

echo "[*] Updating system..."
pkg update -y
pkg upgrade -y

echo "[*] Installing core packages..."
pkg install git python nano -y
python3 -m ensurepip

echo "[*] Removing old Omar-tool..."
rm -rf ~/omar-tool

echo "[*] Cloning Omar-tool..."
git clone https://github.com/omarmetman/omar-tool.git
cd omar-tool || { echo "❌ Folder not found!"; exit 1; }

echo "[*] Installing required Python packages..."
pip install -r requirements.txt

# Add alias
ALIAS="alias omar='python3 $(pwd)/omar.py'"
FILES=(~/.bashrc ~/.profile ~/.zshrc)
for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        grep -qxF "$ALIAS" "$f" || echo "$ALIAS" >> "$f"
    fi
done

echo "[✅] Setup completed!"
echo "Run the tool with: omar"
echo "Activate alias immediately: source ~/.bashrc"
