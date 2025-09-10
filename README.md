# Omar-tool

Omar M. Etman - Command line tool for site/domain reconnaissance.

## Overview

Omar-tool is a command line utility that allows you to:

- Resolve DNS (A/AAAA)
- Get IP addresses
- GeoIP lookup
- Fetch HTTP headers
- Extract <title> and meta description
- Read /robots.txt and /sitemap.xml
- Clone GitHub repositories

The main script (`omar.py`) is in Arabic, but all supporting files are in English.

---

## Installation on Termux

1. **Open Termux**.

2. **Set up storage access:**
```bash
termux-setup-storage
Update and upgrade packages:

bash
نسخ الكود
pkg update -y
pkg upgrade -y
Install required core packages:

bash
نسخ الكود
pkg install git python nano -y
python3 -m ensurepip
Remove any old Omar-tool installation:

bash
نسخ الكود
rm -rf ~/omar-tool
Clone the Omar-tool repository:

bash
نسخ الكود
git clone https://github.com/omarmetman/omar-tool.git
cd omar-tool
Run the install script (adds alias and installs Python dependencies):

bash
نسخ الكود
bash install.sh
source ~/.bashrc
Running the Tool
Using the alias (recommended):

bash
نسخ الكود
omar
Directly with Python:

bash
نسخ الكود
python3 omar.py
Usage Examples
Resolve DNS and get IP:

Input domain: example.com

Output: A record, AAAA record (if dnspython installed)

GeoIP lookup:

Input domain: example.com

Output: IP, Country, Region, City, ISP

Fetch HTTP headers:

Input domain: example.com

Output: All HTTP response headers

Title & meta description:

Input domain: example.com

Output: <title> and meta description from HTML

Read /robots.txt and /sitemap.xml:

Input domain: example.com

Output: Contents if available

Clone GitHub repository:

Input GitHub repo URL

Command executes git clone <url>

Notes & Tips
Always use the public repository URL for cloning to avoid authentication prompts.

Do not enter sensitive tokens in scripts.

If dnspython is not installed, AAAA records will not be fetched.

To troubleshoot common errors:

ModuleNotFoundError: Run pip install -r requirements.txt

git clone failed: Check the repo URL is public

omar command not found: Run source ~/.bashrc or use python3 omar.py

