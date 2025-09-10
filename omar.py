#!/usr/bin/env python3
# Omar-tool main script (Arabic)
# Author: Omar M. Etman

import os
import sys
import socket
import requests
from time import sleep

# Optional: dnspython
try:
    import dns.resolver
    DNSLIB = True
except ImportError:
    DNSLIB = False

# ANSI colors
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    clear_screen()
    print(f"{CYAN}")
    print("=====================================")
    print("       Omar M. Etman")
    print("        TOOL v2.0")
    print("=====================================")
    print(f"{RESET}")

def input_ar(msg):
    try:
        return input(msg[::-1])  # Reverse Arabic text for proper display
    except KeyboardInterrupt:
        print(f"\n{RED}تم إلغاء العملية{RESET}")
        sys.exit()

def resolve_dns(domain):
    print(f"{YELLOW}[*] جلب سجلات DNS...{RESET}")
    try:
        a_record = socket.gethostbyname(domain)
        print(f"IP Address (A): {a_record}")
    except Exception:
        print(f"{RED}فشل في جلب A record{RESET}")
    if DNSLIB:
        try:
            answers = dns.resolver.resolve(domain, 'AAAA')
            for rdata in answers:
                print(f"IP Address (AAAA): {rdata}")
        except Exception:
            print(f"{RED}فشل في جلب AAAA record{RESET}")
    else:
        print(f"{RED}مكتبة dnspython غير مثبتة، سجلات AAAA لن تعمل{RESET}")

def geo_ip(domain):
    print(f"{YELLOW}[*] جلب GeoIP...{RESET}")
    try:
        ip = socket.gethostbyname(domain)
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
        print(f"IP: {resp.get('query')}")
        print(f"Country: {resp.get('country')}")
        print(f"Region: {resp.get('regionName')}")
        print(f"City: {resp.get('city')}")
        print(f"ISP: {resp.get('isp')}")
    except Exception:
        print(f"{RED}فشل في جلب بيانات GeoIP{RESET}")

def http_headers(domain):
    print(f"{YELLOW}[*] جلب HTTP headers...{RESET}")
    try:
        r = requests.get(f"http://{domain}", timeout=8)
        for k, v in r.headers.items():
            print(f"{k}: {v}")
    except Exception:
        print(f"{RED}فشل في جلب HTTP headers{RESET}")

def meta_info(domain):
    print(f"{YELLOW}[*] جلب Title و Meta description...{RESET}")
    try:
        r = requests.get(f"http://{domain}", timeout=8).text
        title = ""
        description = ""
        if "<title>" in r:
            title = r.split("<title>")[1].split("</title>")[0]
        if 'name="description"' in r:
            description = r.split('name="description"')[1].split('content="')[1].split('"')[0]
        print(f"Title: {title}")
        print(f"Meta description: {description}")
    except Exception:
        print(f"{RED}فشل في جلب Title/Meta{RESET}")

def read_robots_sitemap(domain):
    print(f"{YELLOW}[*] قراءة robots.txt و sitemap.xml...{RESET}")
    urls = ["/robots.txt", "/sitemap.xml"]
    for path in urls:
        try:
            r = requests.get(f"http://{domain}{path}", timeout=8)
            if r.status_code == 200:
                print(f"{path}:\n{r.text}\n")
            else:
                print(f"{path} غير موجودة")
        except Exception:
            print(f"فشل في جلب {path}")

def clone_repo():
    url = input_ar("أدخل رابط GitHub للاستنساخ: ")
    os.system(f"git clone {url}")

def main_menu():
    while True:
        banner()
        print("اختر وظيفة:")
        print("1) معرفة IP و DNS (A / AAAA)")
        print("2) جلب GeoIP للموقع")
        print("3) جلب HTTP Headers")
        print("4) جلب <title> و meta description")
        print("5) قراءة /robots.txt و /sitemap.xml")
        print("6) استنساخ GitHub Repo")
        print("0) خروج")

        choice = input_ar("أدخل رقم الخيار: ")

        if choice == "1":
            domain = input_ar("أدخل اسم الموقع: ")
            resolve_dns(domain)
        elif choice == "2":
            domain = input_ar("أدخل اسم الموقع: ")
            geo_ip(domain)
        elif choice == "3":
            domain = input_ar("أدخل اسم الموقع: ")
            http_headers(domain)
        elif choice == "4":
            domain = input_ar("أدخل اسم الموقع: ")
            meta_info(domain)
        elif choice == "5":
            domain = input_ar("أدخل اسم الموقع: ")
            read_robots_sitemap(domain)
        elif choice == "6":
            clone_repo()
        elif choice == "0":
            print(f"{GREEN}وداعًا!{RESET}")
            break
        else:
            print(f"{RED}خيار غير صالح!{RESET}")
        input_ar("اضغط Enter للعودة للقائمة...")

if __name__ == "__main__":
    main_menu()
