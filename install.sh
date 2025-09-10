#!/bin/bash
# Omar-tool Professional v3.0 Setup Script

echo -e "\033[1;34m[*] Updating system...\033[0m"
pkg update -y
pkg upgrade -y

echo -e "\033[1;34m[*] Installing core packages...\033[0m"
pkg install git python nano -y
python3 -m ensurepip --upgrade

echo -e "\033[1;34m[*] Removing old Omar-tool...\033[0m"
rm -rf ~/omar-tool

echo -e "\033[1;34m[*] Cloning Omar-tool...\033[0m"
git clone https://github.com/omarmetman/omar-tool.git
cd omar-tool || { echo -e "\033[1;31m❌ Folder not found!\033[0m"; exit 1; }

echo -e "\033[1;34m[*] Installing required Python packages...\033[0m"
pip install --upgrade pip
pip install -r requirements.txt

# Add alias
ALIAS="alias omar='python3 $(pwd)/omar.py'"
FILES=(~/.bashrc ~/.profile ~/.zshrc)
for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        grep -qxF "$ALIAS" "$f" || echo "$ALIAS" >> "$f"
    fi
done

echo -e "\033[1;32m[✅] Omar-tool Professional v3.0 setup completed!\033[0m"
echo -e "\033[1;33mRun the tool with: omar\033[0m"
echo -e "\033[1;33mActivate alias immediately: source ~/.bashrc\033[0m"
echo -e "\033[1;36mNew features: Comprehensive URL analysis, BeautifulSoup integration, enhanced scanning\033[0m"
