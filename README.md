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
2️⃣ استنساخ المشروع
bash
نسخ الكود
git clone https://github.com/username/omar-tool.git
cd omar-tool
3️⃣ تثبيت الحزم المطلوبة
bash
نسخ الكود
pip install -r requirements.txt
4️⃣ تشغيل سكربت التثبيت
bash
نسخ الكود
chmod +x install.sh
bash install.sh
5️⃣ تفعيل alias
bash
نسخ الكود
source ~/.bashrc
6️⃣ تشغيل الأداة
bash
نسخ الكود
omar
خيارات الأداة
معرفة IP و DNS (A / AAAA / MX / NS)

جلب GeoIP

جلب HTTP Headers

جلب <title> و meta description

قراءة /robots.txt و /sitemap.xml

استنساخ GitHub Repo

خروج

مشاكل شائعة
ModuleNotFoundError: نفذ pip install -r requirements.txt

pip not found: تأكد من تثبيت Python3 و pip

git clone failed: تحقق من الرابط أو إذا كان private repo

أمان
لا تدخل توكنات أو بيانات حساسة في GitHub Repo غير موثوق.

الأداة للاستعلامات العامة فقط، وليست للاختراق.

مثال عملي كامل على Termux
bash
نسخ الكود
termux-setup-storage
pkg update -y && pkg upgrade -y
pkg install git python nano -y
python3 -m ensurepip --upgrade
pip install --upgrade pip
git clone https://github.com/username/omar-tool.git
cd omar-tool
chmod +x install.sh
bash install.sh
source ~/.bashrc
omar
yaml
نسخ الكود

---

=== FILE: LICENSE (size approx 20 lines) ===
```text
MIT License

Copyright (c) 2025 Omar M. Etman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

