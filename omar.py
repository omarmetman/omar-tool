#!/usr/bin/env python3
# Omar-tool Professional Version
# Author: Omar M. Etman

import os
import sys
import socket
import requests
import subprocess
import json
import threading
import time
from datetime import datetime
from time import sleep

# Optional libraries
try:
    import dns.resolver
    DNSLIB = True
except ImportError:
    DNSLIB = False

try:
    import whois
    WHOISLIB = True
except ImportError:
    WHOISLIB = False

# ANSI colors for better UI
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    PURPLE = "\033[95m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

# Clear screen function
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

# Display a professional banner
def banner():
    clear_screen()
    print(f"{Colors.PURPLE}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║                 O M A R - T O O L  v2.0                      ║")
    print("║                 P R O F E S S I O N A L                      ║")
    print("║                                                              ║")
    print("║         Comprehensive Cybersecurity Assessment Tool          ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    print(f"{Colors.CYAN}Created by: Omar M. Etman{Colors.RESET}")
    print(f"{Colors.YELLOW}Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print()

# Loading animation
def loading_animation(message, duration=2):
    end_time = time.time() + duration
    symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.YELLOW}{symbols[i]} {message}{Colors.RESET}", end="")
        i = (i + 1) % len(symbols)
        time.sleep(0.1)
    print("\r" + " " * (len(message) + 2) + "\r", end="")

# DNS resolution function
def resolve_dns(domain):
    print(f"{Colors.YELLOW}[*] Resolving DNS records...{Colors.RESET}")
    loading_animation("Querying DNS servers")
    
    records = {
        'A': [], 'AAAA': [], 'MX': [], 'NS': [], 'TXT': [], 'CNAME': []
    }
    
    try:
        # A record
        try:
            a_record = socket.gethostbyname(domain)
            records['A'].append(a_record)
        except Exception:
            pass
        
        if DNSLIB:
            # AAAA record
            try:
                answers = dns.resolver.resolve(domain, 'AAAA')
                for rdata in answers:
                    records['AAAA'].append(str(rdata))
            except Exception:
                pass
            
            # MX records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    records['MX'].append(f"{rdata.preference} {rdata.exchange}")
            except Exception:
                pass
            
            # NS records
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                for rdata in answers:
                    records['NS'].append(str(rdata))
            except Exception:
                pass
            
            # TXT records
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    records['TXT'].append(''.join([s.decode() for s in rdata.strings]))
            except Exception:
                pass
            
            # CNAME record
            try:
                answers = dns.resolver.resolve(domain, 'CNAME')
                for rdata in answers:
                    records['CNAME'].append(str(rdata))
            except Exception:
                pass
        
        # Display results
        for record_type, values in records.items():
            if values:
                print(f"{Colors.GREEN}{record_type} records:{Colors.RESET}")
                for value in values:
                    print(f"  {value}")
            else:
                print(f"{Colors.RED}No {record_type} records found{Colors.RESET}")
                
    except Exception as e:
        print(f"{Colors.RED}Failed to resolve DNS: {e}{Colors.RESET}")

# GeoIP lookup
def geo_ip(domain):
    print(f"{Colors.YELLOW}[*] Looking up GeoIP information...{Colors.RESET}")
    loading_animation("Querying GeoIP database")
    
    try:
        ip = socket.gethostbyname(domain)
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
        
        if resp['status'] == 'success':
            print(f"{Colors.GREEN}IP Address: {Colors.RESET}{resp.get('query')}")
            print(f"{Colors.GREEN}Country: {Colors.RESET}{resp.get('country')} ({resp.get('countryCode')})")
            print(f"{Colors.GREEN}Region: {Colors.RESET}{resp.get('regionName')} ({resp.get('region')})")
            print(f"{Colors.GREEN}City: {Colors.RESET}{resp.get('city')}")
            print(f"{Colors.GREEN}ZIP: {Colors.RESET}{resp.get('zip')}")
            print(f"{Colors.GREEN}Lat/Lon: {Colors.RESET}{resp.get('lat')}, {resp.get('lon')}")
            print(f"{Colors.GREEN}Timezone: {Colors.RESET}{resp.get('timezone')}")
            print(f"{Colors.GREEN}ISP: {Colors.RESET}{resp.get('isp')}")
            print(f"{Colors.GREEN}Organization: {Colors.RESET}{resp.get('org')}")
            print(f"{Colors.GREEN}AS: {Colors.RESET}{resp.get('as')}")
        else:
            print(f"{Colors.RED}GeoIP lookup failed: {resp.get('message', 'Unknown error')}{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.RED}Failed to get GeoIP information: {e}{Colors.RESET}")

# HTTP headers analysis
def http_headers(domain):
    print(f"{Colors.YELLOW}[*] Retrieving HTTP headers...{Colors.RESET}")
    loading_animation("Connecting to server")
    
    try:
        # Try HTTPS first
        try:
            r = requests.get(f"https://{domain}", timeout=8, allow_redirects=True)
            protocol = "HTTPS"
        except:
            # Fall back to HTTP
            r = requests.get(f"http://{domain}", timeout=8, allow_redirects=True)
            protocol = "HTTP"
        
        print(f"{Colors.GREEN}Protocol: {Colors.RESET}{protocol}")
        print(f"{Colors.GREEN}Status Code: {Colors.RESET}{r.status_code}")
        print(f"{Colors.GREEN}Final URL: {Colors.RESET}{r.url}")
        print(f"{Colors.GREEN}Server: {Colors.RESET}{r.headers.get('server', 'Not specified')}")
        print(f"{Colors.GREEN}Content Type: {Colors.RESET}{r.headers.get('content-type', 'Not specified')}")
        print(f"{Colors.GREEN}Content Length: {Colors.RESET}{r.headers.get('content-length', 'Not specified')}")
        
        # Security headers check
        security_headers = [
            'strict-transport-security', 'x-frame-options', 'x-content-type-options',
            'x-xss-protection', 'content-security-policy', 'referrer-policy'
        ]
        
        print(f"\n{Colors.GREEN}Security Headers:{Colors.RESET}")
        for header in security_headers:
            value = r.headers.get(header, 'Not set')
            status = f"{Colors.GREEN}✓" if value != 'Not set' else f"{Colors.RED}✗"
            print(f"  {header}: {value} {status}{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.RED}Failed to retrieve HTTP headers: {e}{Colors.RESET}")

# Website metadata extraction
def meta_info(domain):
    print(f"{Colors.YELLOW}[*] Extracting website metadata...{Colors.RESET}")
    loading_animation("Analyzing page content")
    
    try:
        r = requests.get(f"http://{domain}", timeout=8)
        content = r.text.lower()
        
        # Extract title
        title = "Not found"
        if "<title>" in content:
            title_start = content.find("<title>") + 7
            title_end = content.find("</title>")
            title = content[title_start:title_end].strip()
        
        # Extract meta description
        description = "Not found"
        if 'name="description"' in content:
            desc_start = content.find('content="', content.find('name="description"')) + 9
            desc_end = content.find('"', desc_start)
            description = content[desc_start:desc_end].strip()
        
        # Extract viewport
        viewport = "Not found"
        if 'name="viewport"' in content:
            viewport_start = content.find('content="', content.find('name="viewport"')) + 9
            viewport_end = content.find('"', viewport_start)
            viewport = content[viewport_start:viewport_end].strip()
        
        # Extract charset
        charset = "Not found"
        if 'charset=' in content:
            charset_start = content.find('charset=') + 8
            charset_end = content.find('"', charset_start)
            if charset_end == -1:
                charset_end = content.find('>', charset_start)
                if charset_end == -1:
                    charset_end = content.find(' ', charset_start)
            charset = content[charset_start:charset_end].strip()
        
        print(f"{Colors.GREEN}Title: {Colors.RESET}{title}")
        print(f"{Colors.GREEN}Meta Description: {Colors.RESET}{description}")
        print(f"{Colors.GREEN}Viewport: {Colors.RESET}{viewport}")
        print(f"{Colors.GREEN}Charset: {Colors.RESET}{charset}")
        
    except Exception as e:
        print(f"{Colors.RED}Failed to extract metadata: {e}{Colors.RESET}")

# Robots.txt and sitemap.xml analysis
def read_robots_sitemap(domain):
    print(f"{Colors.YELLOW}[*] Analyzing robots.txt and sitemap.xml...{Colors.RESET}")
    
    # Check robots.txt
    print(f"\n{Colors.GREEN}=== robots.txt ==={Colors.RESET}")
    try:
        r = requests.get(f"http://{domain}/robots.txt", timeout=8)
        if r.status_code == 200:
            print(r.text)
        else:
            print(f"{Colors.RED}robots.txt not found (Status: {r.status_code}){Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Failed to retrieve robots.txt: {e}{Colors.RESET}")
    
    # Check sitemap.xml
    print(f"\n{Colors.GREEN}=== sitemap.xml ==={Colors.RESET}")
    try:
        r = requests.get(f"http://{domain}/sitemap.xml", timeout=8)
        if r.status_code == 200:
            # Try to parse as XML
            if '<?xml' in r.text:
                print("Valid XML sitemap found")
            else:
                print(r.text[:500] + "..." if len(r.text) > 500 else r.text)
        else:
            print(f"{Colors.RED}sitemap.xml not found (Status: {r.status_code}){Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Failed to retrieve sitemap.xml: {e}{Colors.RESET}")

# WHOIS lookup
def whois_lookup(domain):
    if not WHOISLIB:
        print(f"{Colors.RED}whois library not installed. Install it with: pip install python-whois{Colors.RESET}")
        return
    
    print(f"{Colors.YELLOW}[*] Performing WHOIS lookup...{Colors.RESET}")
    loading_animation("Querying WHOIS databases")
    
    try:
        w = whois.whois(domain)
        
        print(f"{Colors.GREEN}Domain Name: {Colors.RESET}{w.domain_name}")
        print(f"{Colors.GREEN}Registrar: {Colors.RESET}{w.registrar}")
        print(f"{Colors.GREEN}WHOIS Server: {Colors.RESET}{w.whois_server}")
        
        if w.creation_date:
            if isinstance(w.creation_date, list):
                print(f"{Colors.GREEN}Creation Date: {Colors.RESET}{w.creation_date[0]}")
            else:
                print(f"{Colors.GREEN}Creation Date: {Colors.RESET}{w.creation_date}")
        
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                print(f"{Colors.GREEN}Expiration Date: {Colors.RESET}{w.expiration_date[0]}")
            else:
                print(f"{Colors.GREEN}Expiration Date: {Colors.RESET}{w.expiration_date}")
        
        if w.updated_date:
            if isinstance(w.updated_date, list):
                print(f"{Colors.GREEN}Updated Date: {Colors.RESET}{w.updated_date[0]}")
            else:
                print(f"{Colors.GREEN}Updated Date: {Colors.RESET}{w.updated_date}")
        
        print(f"{Colors.GREEN}Name Servers: {Colors.RESET}")
        if w.name_servers:
            for ns in w.name_servers:
                print(f"  {ns}")
        
        print(f"{Colors.GREEN}Status: {Colors.RESET}")
        if w.status:
            for status in w.status:
                print(f"  {status}")
                
    except Exception as e:
        print(f"{Colors.RED}WHOIS lookup failed: {e}{Colors.RESET}")

# Port scanner
def port_scan(domain):
    print(f"{Colors.YELLOW}[*] Scanning common ports...{Colors.RESET}")
    
    try:
        ip = socket.gethostbyname(domain)
        print(f"{Colors.GREEN}Target IP: {Colors.RESET}{ip}")
        
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        open_ports = []
        
        def check_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((ip, port))
                    if result == 0:
                        open_ports.append(port)
            except:
                pass
        
        # Use threading for faster scanning
        threads = []
        for port in common_ports:
            t = threading.Thread(target=check_port, args=(port,))
            threads.append(t)
            t.start()
        
        # Show loading animation while scanning
        end_time = time.time() + 5  # Max 5 seconds for scanning
        symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        i = 0
        while any(t.is_alive() for t in threads) and time.time() < end_time:
            print(f"\r{Colors.YELLOW}{symbols[i]} Scanning ports...{Colors.RESET}", end="")
            i = (i + 1) % len(symbols)
            time.sleep(0.1)
        
        # Wait for all threads to complete
        for t in threads:
            t.join(timeout=0.1)
        
        print("\r" + " " * 30 + "\r", end="")
        
        if open_ports:
            print(f"{Colors.GREEN}Open ports: {Colors.RESET}{', '.join(map(str, sorted(open_ports)))}")
        else:
            print(f"{Colors.RED}No common open ports found{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.RED}Port scan failed: {e}{Colors.RESET}")

# Subdomain enumeration
def subdomain_scan(domain):
    print(f"{Colors.YELLOW}[*] Scanning for common subdomains...{Colors.RESET}")
    
    # Common subdomains list
    subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
        'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3',
        'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static',
        'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki',
        'web', 'media', 'email', 'images', 'img', 'www1', 'intranet', 'portal', 'video',
        'ipv4', 'api', 'cdn', 'stats', 'dns', 'pic', 'pic', 'ssl', 'search', 'staging'
    ]
    
    found_subdomains = []
    
    def check_subdomain(subdomain):
        try:
            full_domain = f"{subdomain}.{domain}"
            socket.gethostbyname(full_domain)
            found_subdomains.append(full_domain)
        except:
            pass
    
    # Use threading for faster scanning
    threads = []
    for subdomain in subdomains:
        t = threading.Thread(target=check_subdomain, args=(subdomain,))
        threads.append(t)
        t.start()
    
    # Show loading animation while scanning
    end_time = time.time() + 10  # Max 10 seconds for scanning
    symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    i = 0
    while any(t.is_alive() for t in threads) and time.time() < end_time:
        print(f"\r{Colors.YELLOW}{symbols[i]} Scanning subdomains... ({len(found_subdomains)} found){Colors.RESET}", end="")
        i = (i + 1) % len(symbols)
        time.sleep(0.1)
    
    # Wait for all threads to complete
    for t in threads:
        t.join(timeout=0.1)
    
    print("\r" + " " * 50 + "\r", end="")
    
    if found_subdomains:
        print(f"{Colors.GREEN}Found subdomains: {Colors.RESET}")
        for subdomain in found_subdomains:
            print(f"  {subdomain}")
    else:
        print(f"{Colors.RED}No common subdomains found{Colors.RESET}")

# GitHub repository cloning
def clone_repo():
    url = input("Enter GitHub repository URL: ")
    if not url:
        print(f"{Colors.RED}No URL provided{Colors.RESET}")
        return
    
    print(f"{Colors.YELLOW}[*] Cloning repository...{Colors.RESET}")
    try:
        result = subprocess.run(['git', 'clone', url], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"{Colors.GREEN}Repository cloned successfully{Colors.RESET}")
        else:
            print(f"{Colors.RED}Failed to clone repository: {result.stderr}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Failed to clone repository: {e}{Colors.RESET}")

# Main menu
def main_menu():
    while True:
        banner()
        print(f"{Colors.BOLD}Select an option:{Colors.RESET}")
        print(f"{Colors.CYAN} 1){Colors.RESET} DNS Resolution (A, AAAA, MX, NS, TXT, CNAME)")
        print(f"{Colors.CYAN} 2){Colors.RESET} GeoIP Lookup")
        print(f"{Colors.CYAN} 3){Colors.RESET} HTTP Headers Analysis")
        print(f"{Colors.CYAN} 4){Colors.RESET} Website Metadata Extraction")
        print(f"{Colors.CYAN} 5){Colors.RESET} Robots.txt and Sitemap Analysis")
        print(f"{Colors.CYAN} 6){Colors.RESET} WHOIS Lookup")
        print(f"{Colors.CYAN} 7){Colors.RESET} Port Scanner")
        print(f"{Colors.CYAN} 8){Colors.RESET} Subdomain Scanner")
        print(f"{Colors.CYAN} 9){Colors.RESET} Clone GitHub Repository")
        print(f"{Colors.CYAN} 0){Colors.RESET} Exit")
        print()

        try:
            choice = input(f"{Colors.YELLOW}Enter your choice: {Colors.RESET}")
            
            if choice == "1":
                domain = input("Enter domain: ")
                resolve_dns(domain)
            elif choice == "2":
                domain = input("Enter domain: ")
                geo_ip(domain)
            elif choice == "3":
                domain = input("Enter domain: ")
                http_headers(domain)
            elif choice == "4":
                domain = input("Enter domain: ")
                meta_info(domain)
            elif choice == "5":
                domain = input("Enter domain: ")
                read_robots_sitemap(domain)
            elif choice == "6":
                domain = input("Enter domain: ")
                whois_lookup(domain)
            elif choice == "7":
                domain = input("Enter domain: ")
                port_scan(domain)
            elif choice == "8":
                domain = input("Enter domain: ")
                subdomain_scan(domain)
            elif choice == "9":
                clone_repo()
            elif choice == "0":
                print(f"{Colors.GREEN}Goodbye!{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}Invalid choice!{Colors.RESET}")
            
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}Operation cancelled{Colors.RESET}")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Tool terminated by user{Colors.RESET}")
