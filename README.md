# Omar-tool Professional

Omar M. Etman - Comprehensive cybersecurity assessment and reconnaissance tool.

## Overview

Omar-tool Professional is an enhanced command-line utility for comprehensive domain and network reconnaissance. It provides:

- **DNS Analysis**: Complete DNS records (A, AAAA, MX, NS, TXT, CNAME)
- **GeoIP Lookup**: Detailed geographical information about servers
- **HTTP Headers Analysis**: Full header inspection with security assessment
- **Metadata Extraction**: Title, meta description, viewport, and charset
- **File Analysis**: robots.txt and sitemap.xml inspection
- **WHOIS Lookup**: Domain registration information
- **Port Scanning**: Common port scanning with threading
- **Subdomain Enumeration**: Common subdomain discovery
- **GitHub Integration**: Repository cloning functionality

---

## Installation on Termux

1. **Open Termux**

2. **Set up storage access:**
```bash
termux-setup-storage
Update and upgrade packages:

bash
pkg update -y
pkg upgrade -y
Install required core packages:

bash
pkg install git python nano -y
python3 -m ensurepip
Remove any old Omar-tool installation:

bash
rm -rf ~/omar-tool
Clone the repository:

bash
git clone https://github.com/omarmetman/omar-tool.git
cd omar-tool
Run the install script:

bash
bash install.sh
source ~/.bashrc
Running the Tool
Using the alias (recommended):

bash
omar
Directly with Python:

bash
python3 omar.py
Usage Examples
1. Complete DNS Analysis
text
Input domain: example.com
Output: A, AAAA, MX, NS, TXT, and CNAME records
2. Detailed GeoIP Lookup
text
Input domain: example.com
Output: IP, Country, Region, City, ISP, Coordinates, Timezone
3. HTTP Headers with Security Assessment
text
Input domain: example.com
Output: All headers plus security header analysis (HSTS, CSP, X-Frame-Options, etc.)
4. Website Metadata Extraction
text
Input domain: example.com
Output: Title, meta description, viewport, charset
5. File Analysis
text
Input domain: example.com
Output: Contents of robots.txt and sitemap.xml
6. WHOIS Lookup
text
Input domain: example.com
Output: Registrar information, creation/expiration dates, name servers
7. Port Scanning
text
Input domain: example.com
Output: List of open common ports (21, 22, 80, 443, etc.)
8. Subdomain Enumeration
text
Input domain: example.com
Output: List of discovered subdomains
9. GitHub Repository Cloning
text
Input: GitHub repository URL
Action: Clones the repository using git clone
New Professional Features
Threaded Operations: Faster port scanning and subdomain enumeration

Security Headers Analysis: Checks for important security headers

Comprehensive DNS: Full DNS record analysis beyond basic A/AAAA

Visual Enhancements: Professional UI with loading animations

Error Handling: Robust error handling with user-friendly messages

Performance: Optimized for speed with timeout management

Notes & Tips
Always use public repository URLs to avoid authentication issues

For best performance, ensure a stable internet connection

The tool includes timeouts to prevent hanging operations

Some features require additional libraries (automatically installed)

Use Ctrl+C to cancel any ongoing operation

Troubleshooting
ModuleNotFoundError: Run pip install -r requirements.txt

git clone failed: Verify the repository URL is correct and accessible

omar command not found: Run source ~/.bashrc or use python3 omar.py

Port scanning slow: This is normal behavior for comprehensive scanning

WHOIS lookup fails: This may happen with some TLDs or restricted domains

