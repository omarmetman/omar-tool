#!/bin/bash
# Omar-tool Ultimate Installer for Termux
# Author: Omar M. Etman

echo "[*] تحديث النظام..."
pkg update -y && pkg upgrade -y

echo "[*] تثبيت git و python و nano..."
pkg install git python nano -y

echo "[*] تثبيت pip..."
python3 -m ensurepip --upgrade
pip install --upgrade pip

# استنساخ الريبو
REPO_URL=${1:-"https://github.com/username/omar-tool.git"}
if [ -d "omar-tool" ]; then
    echo "[*] المجلد موجود بالفعل، لن يتم الاستنساخ."
else
    echo "[*] استنساخ الريبو من: $REPO_URL"
    git clone "$REPO_URL"
fi

cd omar-tool || exit

echo "[*] تثبيت الحزم المطلوبة..."
pip install -r requirements.txt

# إضافة alias
ALIAS="alias omar='python3 $(pwd)/omar.py'"
FILES=(~/.bashrc ~/.profile ~/.zshrc)
for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        grep -qxF "$ALIAS" "$f" || echo "$ALIAS" >> "$f"
    fi
done

echo "تم الإعداد بنجاح!"
echo "لتفعيل alias: source ~/.bashrc أو إعادة تشغيل Termux"
