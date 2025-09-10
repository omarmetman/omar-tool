#!/usr/bin/env python3
# Omar-tool: Enhanced domain/site reconnaissance tool
# Author: Omar M. Etman

import sys, os, subprocess, socket, requests
from urllib.parse import urlparse

try:
    import dns.resolver
except ImportError:
    dns = None

BANNER = """
==========================================
|       Omar M. Etman - أداة المعلومات       |
|      Domain / Site Reconnaissance       |
|         نسخة مطوّرة ومحدثة 2025          |
==========================================
"""

MENU = """
اختر وظيفة:
1) معرفة IP و DNS (A / AAAA / MX / NS)
2) جلب GeoIP للموقع
3) جلب HTTP Headers
4) جلب <title> و meta description
5) قراءة /robots.txt و /sitemap.xml
6) استنساخ GitHub Repo
0) خروج
"""

def check_dependencies():
    missing = []
    if dns is None:
        missing.append("dnspython (اختياري لكن يضيف وظائف DNS متقدمة)")
    try:
        import requests
    except ImportError:
        missing.append("requests")
    if missing:
        print("\nتحذير: بعض المكتبات مفقودة:", ", ".join(missing))
        print("لتثبيتها: pip install -r requirements.txt\n")

def resolve_dns(domain):
    print(f"\n[+] محاولة جلب IP و DNS لـ: {domain}")
    try:
        ips = socket.getaddrinfo(domain, None)
        print("IPs الموجودة:")
        for ip in set([r[4][0] for r in ips]):
            print("  ", ip)
    except Exception as e:
        print("خطأ أثناء جلب IP:", str(e))
    if dns:
        for record_type in ['A','AAAA','MX','NS']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                print(f"\nسجلات {record_type}:")
                for r in answers:
                    print("  ", r.to_text())
            except Exception:
                print(f"  لم يتم العثور على سجلات {record_type} أو حدث خطأ.")
    else:
        print("تنبيه: dnspython غير مثبت. بعض سجلات DNS لن تظهر.")

def geoip_lookup(ip_or_domain):
    print(f"\n[+] جلب GeoIP لـ: {ip_or_domain}")
    try:
        url = f"http://ip-api.com/json/{ip_or_domain}"
        resp = requests.get(url, timeout=8)
        data = resp.json()
        if data['status'] == 'success':
            print(f"IP: {data.get('query','-')}")
            print(f"الدولة: {data.get('country','-')}")
            print(f"المنطقة: {data.get('regionName','-')}")
            print(f"المدينة: {data.get('city','-')}")
            print(f"ISP: {data.get('isp','-')}")
            print(f"Organization: {data.get('org','-')}")
            print(f"Latitude / Longitude: {data.get('lat','-')}, {data.get('lon','-')}")
        else:
            print("تعذر جلب بيانات GeoIP")
    except Exception as e:
        print("خطأ أثناء جلب GeoIP:", str(e))

def fetch_headers(url):
    print(f"\n[+] جلب HTTP Headers لـ: {url}")
    try:
        resp = requests.get(url, timeout=8)
        for k,v in resp.headers.items():
            print(f"{k}: {v}")
    except Exception as e:
        print("خطأ أثناء جلب الهيدرز:", str(e))

def fetch_title_meta(url):
    print(f"\n[+] جلب <title> و meta description لـ: {url}")
    try:
        resp = requests.get(url, timeout=8)
        html = resp.text
        title = "-"
        meta_desc = "-"
        if "<title>" in html:
            start = html.find("<title>")+7
            end = html.find("</title>", start)
            title = html[start:end].strip()
        lower_html = html.lower()
        if 'name="description"' in lower_html:
            start = lower_html.find('name="description"')
            start_content = lower_html.find('content="', start)+9
            end_content = lower_html.find('"', start_content)
            meta_desc = html[start_content:end_content]
        print("Title:", title)
        print("Meta Description:", meta_desc)
    except Exception as e:
        print("خطأ أثناء جلب العنوان والوصف:", str(e))

def fetch_robots_sitemap(domain):
    print(f"\n[+] قراءة /robots.txt و /sitemap.xml لـ: {domain}")
    base = f"http://{domain}"
    for file in ["/robots.txt","/sitemap.xml"]:
        try:
            resp = requests.get(base+file, timeout=8)
            if resp.status_code == 200:
                content = resp.text
                print(f"\n{file} موجود (أول 500 حرف):\n{content[:500]}{'...' if len(content)>500 else ''}")
            else:
                print(f"{file} غير موجود أو غير قابل للقراءة (Status: {resp.status_code})")
        except Exception as e:
            print(f"خطأ أثناء جلب {file}:", str(e))

def clone_github():
    url = input("أدخل رابط GitHub repo: ").strip()
    if not url.startswith("http"):
        print("رابط غير صالح.")
        return
    try:
        subprocess.run(["git","clone",url], check=True)
        print("تم استنساخ المستودع بنجاح.")
    except subprocess.CalledProcessError as e:
        print("خطأ أثناء الاستنساخ:", str(e))

def main():
    check_dependencies()
    print(BANNER)
    while True:
        print(MENU)
        choice = input("أدخل اختيارك: ").strip()
        if choice=="1":
            domain = input("أدخل اسم النطاق (domain.com): ").strip()
            resolve_dns(domain)
        elif choice=="2":
            ip_or_domain = input("أدخل IP أو اسم النطاق: ").strip()
            geoip_lookup(ip_or_domain)
        elif choice=="3":
            url = input("أدخل رابط الموقع (https://example.com): ").strip()
            fetch_headers(url)
        elif choice=="4":
            url = input("أدخل رابط الموقع (https://example.com): ").strip()
            fetch_title_meta(url)
        elif choice=="5":
            domain = input("أدخل اسم النطاق (domain.com): ").strip()
            fetch_robots_sitemap(domain)
        elif choice=="6":
            clone_github()
        elif choice=="0":
            print("وداعًا! شكرًا لاستخدام Omar M. Etman tool.")
            sys.exit(0)
        else:
            print("اختيار غير صالح، حاول مرة أخرى.")

if __name__=="__main__":
    main()
