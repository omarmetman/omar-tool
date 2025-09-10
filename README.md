# Omar-tool Ultimate 2025
أداة معلومات عامة متقدمة عن المواقع، بلغة Python 3، قابلة للتشغيل على Termux.

## المتطلبات
- Termux على Android
- Python 3
- git

## خطوات التثبيت والاستخدام

### 1️⃣ تجهيز Termux
```bash
termux-setup-storage
pkg update -y && pkg upgrade -y
pkg install git python nano -y
python3 -m ensurepip --upgrade
pip install --upgrade pip
