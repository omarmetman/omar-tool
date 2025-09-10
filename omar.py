#!/usr/bin/env python3

# Omar-tool Professional v3.0 - Ultimate Reconnaissance Tool
# Author: Omar M. Etman

import os
import sys
import socket
import requests
import subprocess
import json
import threading
import time
import re
import urllib.parse
import ipaddress
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

try:
    from bs4 import BeautifulSoup
    BS4LIB = True
except ImportError:
    BS4LIB = False

# Enhanced ANSI colors for better UI
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
    ORANGE = "\033[38;5;208m"
    DARK_CYAN = "\033[38;5;30m"
    PINK = "\033[38;5;206m"

# Clear screen function
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

# Display a professional banner
def banner():
    clear_screen()
    print(f"{Colors.PURPLE}{Colors.BOLD}")
    print("                                                                              ")
    print(f"            {Colors.WHITE}╔═╗┌─┐┌┬┐┌─┐  ╔╦╗┌─┐┌─┐┌┬┐┌─┐┌─┐┌┬┐┬┌┐┌┌─┐{Colors.PURPLE}            ")
    print(f"            {Colors.WHITE}║ ╦├─┤ │ ├─┤   ║║├┤ ├─┤ │ ├┤ │ │ │││││├┤ {Colors.PURPLE}            ")
    print(f"            {Colors.WHITE}╚═╝┴ ┴ ┴ ┴ ┴  ═╩╝└─┘┴ ┴ ┴ └─┘└─┘─┴┘┴┘└┘└─┘{Colors.PURPLE}            ")
    print("                                                                              ")
    print(f"{Colors.RESET}")
    print(f"{Colors.ORANGE}{Colors.BOLD}                          Omar M. Etman{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}                   Ultimate Reconnaissance Tool{Colors.RESET}")
    print(f"{Colors.YELLOW}                   Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.PURPLE}                   ===================================={Colors.RESET}")
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

# Extract domain from URL
def extract_domain(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.netloc:
            return parsed_url.netloc
        elif parsed_url.path:
            return parsed_url.path.split('/')[0]
        else:
            return url
    except:
        return url

# Enhanced DNS resolution function
def resolve_dns(domain):
    print(f"\n{Colors.GREEN}[+] DNS Resolution for {domain}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Resolving DNS records...{Colors.RESET}")
    loading_animation("Querying DNS servers")
    
    if not DNSLIB:
        print(f"{Colors.RED}dnspython library not installed. Install it with: pip install dnspython{Colors.RESET}")
        return
    
    try:
        # A Records
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            print(f"\n{Colors.GREEN}A Records:{Colors.RESET}")
            for record in a_records:
                print(f"  {record.address}")
        except:
            print(f"{Colors.RED}  No A records found{Colors.RESET}")
        
        # AAAA Records
        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            print(f"\n{Colors.GREEN}AAAA Records:{Colors.RESET}")
            for record in aaaa_records:
                print(f"  {record.address}")
        except:
            print(f"{Colors.RED}  No AAAA records found{Colors.RESET}")
        
        # MX Records
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            print(f"\n{Colors.GREEN}MX Records:{Colors.RESET}")
            for record in mx_records:
                print(f"  {record.exchange} (Priority: {record.preference})")
        except:
            print(f"{Colors.RED}  No MX records found{Colors.RESET}")
        
        # NS Records
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            print(f"\n{Colors.GREEN}NS Records:{Colors.RESET}")
            for record in ns_records:
                print(f"  {record.target}")
        except:
            print(f"{Colors.RED}  No NS records found{Colors.RESET}")
        
        # TXT Records
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            print(f"\n{Colors.GREEN}TXT Records:{Colors.RESET}")
            for record in txt_records:
                print(f"  {record.strings}")
        except:
            print(f"{Colors.RED}  No TXT records found{Colors.RESET}")
        
        # CNAME Records
        try:
            cname_records = dns.resolver.resolve(domain, 'CNAME')
            print(f"\n{Colors.GREEN}CNAME Records:{Colors.RESET}")
            for record in cname_records:
                print(f"  {record.target}")
        except:
            print(f"{Colors.RED}  No CNAME records found{Colors.RESET}")
        
        # SOA Records
        try:
            soa_records = dns.resolver.resolve(domain, 'SOA')
            print(f"\n{Colors.GREEN}SOA Records:{Colors.RESET}")
            for record in soa_records:
                print(f"  MNAME: {record.mname}")
                print(f"  RNAME: {record.rname}")
                print(f"  Serial: {record.serial}")
                print(f"  Refresh: {record.refresh}")
                print(f"  Retry: {record.retry}")
                print(f"  Expire: {record.expire}")
                print(f"  Minimum TTL: {record.minimum}")
        except:
            print(f"{Colors.RED}  No SOA records found{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.RED}Error in DNS resolution: {e}{Colors.RESET}")

# Enhanced GeoIP lookup
def geo_ip(domain):
    print(f"\n{Colors.GREEN}[+] GeoIP Lookup for {domain}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Looking up GeoIP information...{Colors.RESET}")
    loading_animation("Querying GeoIP database")
    
    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data["status"] == "success":
            print(f"\n{Colors.GREEN}IP Address:{Colors.RESET} {data['query']}")
            print(f"{Colors.GREEN}Country:{Colors.RESET} {data['country']} ({data['countryCode']})")
            print(f"{Colors.GREEN}Region:{Colors.RESET} {data['regionName']} ({data['region']})")
            print(f"{Colors.GREEN}City:{Colors.RESET} {data['city']}")
            print(f"{Colors.GREEN}ZIP Code:{Colors.RESET} {data['zip']}")
            print(f"{Colors.GREEN}Latitude:{Colors.RESET} {data['lat']}")
            print(f"{Colors.GREEN}Longitude:{Colors.RESET} {data['lon']}")
            print(f"{Colors.GREEN}Timezone:{Colors.RESET} {data['timezone']}")
            print(f"{Colors.GREEN}ISP:{Colors.RESET} {data['isp']}")
            print(f"{Colors.GREEN}Organization:{Colors.RESET} {data['org']}")
            print(f"{Colors.GREEN}AS:{Colors.RESET} {data['as']}")
        else:
            print(f"{Colors.RED}Failed to retrieve GeoIP information{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error in GeoIP lookup: {e}{Colors.RESET}")

# Enhanced HTTP headers analysis
def http_headers(domain):
    print(f"\n{Colors.GREEN}[+] HTTP Headers Analysis for {domain}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Retrieving HTTP headers...{Colors.RESET}")
    loading_animation("Connecting to server")
    
    try:
        # Try with HTTPS first
        try:
            response = requests.get(f"https://{domain}", timeout=10)
            protocol = "HTTPS"
        except:
            # Fallback to HTTP if HTTPS fails
            try:
                response = requests.get(f"http://{domain}", timeout=10)
                protocol = "HTTP"
            except Exception as e:
                print(f"{Colors.RED}Failed to connect: {e}{Colors.RESET}")
                return
        
        print(f"\n{Colors.GREEN}Protocol:{Colors.RESET} {protocol}")
        print(f"{Colors.GREEN}Status Code:{Colors.RESET} {response.status_code}")
        print(f"{Colors.GREEN}Server:{Colors.RESET} {response.headers.get('Server', 'Not specified')}")
        print(f"{Colors.GREEN}Content Type:{Colors.RESET} {response.headers.get('Content-Type', 'Not specified')}")
        print(f"{Colors.GREEN}Content Length:{Colors.RESET} {response.headers.get('Content-Length', 'Not specified')}")
        print(f"{Colors.GREEN}Connection:{Colors.RESET} {response.headers.get('Connection', 'Not specified')}")
        
        # Security headers check
        security_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy'
        ]
        
        print(f"\n{Colors.GREEN}Security Headers:{Colors.RESET}")
        for header in security_headers:
            value = response.headers.get(header, 'Not set')
            status = f"{Colors.GREEN}✓" if value != 'Not set' else f"{Colors.RED}✗"
            print(f"  {header}: {value} {status}{Colors.RESET}")
        
        # Print all headers
        print(f"\n{Colors.GREEN}All Headers:{Colors.RESET}")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
            
    except Exception as e:
        print(f"{Colors.RED}Error in HTTP headers analysis: {e}{Colors.RESET}")

# Enhanced Website metadata extraction
def meta_info(domain):
    print(f"\n{Colors.GREEN}[+] Website Metadata Extraction for {domain}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Extracting website metadata...{Colors.RESET}")
    loading_animation("Analyzing page content")
    
    if not BS4LIB:
        print(f"{Colors.RED}BeautifulSoup library not installed. Install it with: pip install beautifulsoup4{Colors.RESET}")
        return
    
    try:
        # Try with HTTPS first
        try:
            response = requests.get(f"https://{domain}", timeout=10)
        except:
            # Fallback to HTTP if HTTPS fails
            try:
                response = requests.get(f"http://{domain}", timeout=10)
            except Exception as e:
                print(f"{Colors.RED}Failed to connect: {e}{Colors.RESET}")
                return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Title
        title = soup.find('title')
        print(f"\n{Colors.GREEN}Title:{Colors.RESET} {title.string if title else 'Not found'}")
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        print(f"{Colors.GREEN}Meta Description:{Colors.RESET} {meta_desc['content'] if meta_desc and 'content' in meta_desc.attrs else 'Not found'}")
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        print(f"{Colors.GREEN}Meta Keywords:{Colors.RESET} {meta_keywords['content'] if meta_keywords and 'content' in meta_keywords.attrs else 'Not found'}")
        
        # Viewport
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        print(f"{Colors.GREEN}Viewport:{Colors.RESET} {viewport['content'] if viewport and 'content' in viewport.attrs else 'Not found'}")
        
        # Charset
        charset = soup.find('meta', attrs={'charset': True})
        if not charset:
            charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        print(f"{Colors.GREEN}Charset:{Colors.RESET} {charset['charset'] if charset and 'charset' in charset.attrs else charset['content'] if charset and 'content' in charset.attrs else 'Not found'}")
        
        # Open Graph tags
        print(f"\n{Colors.GREEN}Open Graph Tags:{Colors.RESET}")
        og_tags = soup.find_all('meta', attrs={'property': re.compile(r'^og:', re.I)})
        if og_tags:
            for tag in og_tags:
                print(f"  {tag['property']}: {tag['content']}")
        else:
            print(f"  {Colors.RED}No Open Graph tags found{Colors.RESET}")
        
        # Twitter Card tags
        print(f"\n{Colors.GREEN}Twitter Card Tags:{Colors.RESET}")
        twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:', re.I)})
        if twitter_tags:
            for tag in twitter_tags:
                print(f"  {tag['name']}: {tag['content']}")
        else:
            print(f"  {Colors.RED}No Twitter Card tags found{Colors.RESET}")
        
        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        print(f"\n{Colors.GREEN}Canonical URL:{Colors.RESET} {canonical['href'] if canonical and 'href' in canonical.attrs else 'Not found'}")
        
        # Language
        language = soup.html.get('lang') if soup.html else 'Not found'
        print(f"{Colors.GREEN}Language:{Colors.RESET} {language}")
        
    except Exception as e:
        print(f"{Colors.RED}Error in metadata extraction: {e}{Colors.RESET}")

# Enhanced Robots.txt and sitemap.xml analysis
def read_robots_sitemap(domain):
    print(f"\n{Colors.GREEN}[+] Robots.txt and Sitemap Analysis for {domain}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Analyzing robots.txt and sitemap.xml...{Colors.RESET}")
    
    # Check robots.txt
    try:
        response = requests.get(f"http://{domain}/robots.txt", timeout=10)
        if response.status_code == 200:
            print(f"\n{Colors.GREEN}robots.txt found:{Colors.RESET}")
            print(response.text)
        else:
            print(f"{Colors.RED}robots.txt not found or not accessible{Colors.RESET}")
    except:
        print(f"{Colors.RED}Failed to retrieve robots.txt{Colors.RESET}")
    
    # Check sitemap.xml
    try:
        response = requests.get(f"http://{domain}/sitemap.xml", timeout=10)
        if response.status_code == 200:
            print(f"\n{Colors.GREEN}sitemap.xml found:{Colors.RESET}")
            
            # Try to parse the sitemap
            try:
                soup = BeautifulSoup(response.content, 'xml')
                urls = soup.find_all('url')
                if urls:
                    print(f"Found {len(urls)} URLs in sitemap:")
                    for url in urls[:5]:  # Show first 5 URLs
                        loc = url.find('loc')
                        if loc:
                            print(f"  {loc.text}")
                    if len(urls) > 5:
                        print(f"  ... and {len(urls) - 5} more")
                else:
                    print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            except:
                print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        else:
            print(f"{Colors.RED}sitemap.xml not found or not accessible{Colors.RESET}")
    except:
        print(f"{Colors.RED}Failed to retrieve sitemap.xml{Colors.RESET}")

# Enhanced WHOIS lookup
def whois_lookup(domain):
    print(f"\n{Colors.GREEN}[+] WHOIS Lookup for {domain}{Colors.RESET}")
    
    if not WHOISLIB:
        print(f"{Colors.RED}whois library not installed. Install it with: pip install python-whois{Colors.RESET}")
        return
    
    print(f"{Colors.YELLOW}[*] Performing WHOIS lookup...{Colors.RESET}")
    loading_animation("Querying WHOIS database")
    
    try:
        w = whois.whois(domain)
        
        if w.domain_name:
            print(f"\n{Colors.GREEN}Domain Name:{Colors.RESET} {w.domain_name}")
        if w.registrar:
            print(f"{Colors.GREEN}Registrar:{Colors.RESET} {w.registrar}")
        if w.whois_server:
            print(f"{Colors.GREEN}WHOIS Server:{Colors.RESET} {w.whois_server}")
        if w.creation_date:
            print(f"{Colors.GREEN}Creation Date:{Colors.RESET} {w.creation_date}")
        if w.expiration_date:
            print(f"{Colors.GREEN}Expiration Date:{Colors.RESET} {w.expiration_date}")
        if w.updated_date:
            print(f"{Colors.GREEN}Updated Date:{Colors.RESET} {w.updated_date}")
        if w.name_servers:
            print(f"{Colors.GREEN}Name Servers:{Colors.RESET}")
            for ns in w.name_servers:
                print(f"  {ns}")
        if w.status:
            print(f"{Colors.GREEN}Status:{Colors.RESET} {w.status}")
        if w.emails:
            print(f"{Colors.GREEN}Emails:{Colors.RESET} {w.emails}")
        if w.org:
            print(f"{Colors.GREEN}Organization:{Colors.RESET} {w.org}")
        if w.address:
            print(f"{Colors.GREEN}Address:{Colors.RESET} {w.address}")
        if w.city:
            print(f"{Colors.GREEN}City:{Colors.RESET} {w.city}")
        if w.state:
            print(f"{Colors.GREEN}State:{Colors.RESET} {w.state}")
        if w.zipcode:
            print(f"{Colors.GREEN}ZIP Code:{Colors.RESET} {w.zipcode}")
        if w.country:
            print(f"{Colors.GREEN}Country:{Colors.RESET} {w.country}")
            
    except Exception as e:
        print(f"{Colors.RED}Error in WHOIS lookup: {e}{Colors.RESET}")

# Enhanced Port scanner
def port_scan(domain):
    print(f"\n{Colors.GREEN}[+] Port Scanner for {domain}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Scanning common ports...{Colors.RESET}")
    loading_animation("Scanning ports")
    
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n{Colors.GREEN}Target IP:{Colors.RESET} {ip}")
        
        # Common ports to scan
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        print(f"{Colors.GREEN}Port\tStatus\tService{Colors.RESET}")
        print(f"{Colors.PURPLE}----\t------\t-------{Colors.RESET}")
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    service = socket.getservbyport(port, 'tcp') if port in [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995] else "Unknown"
                    print(f"{port}\t{Colors.GREEN}Open{Colors.RESET}\t{service}")
                else:
                    print(f"{port}\t{Colors.RED}Closed{Colors.RESET}\t-")
            except:
                print(f"{port}\t{Colors.RED}Error{Colors.RESET}\t-")
        
        # Scan ports sequentially for simplicity
        for port in ports:
            scan_port(port)
            
    except Exception as e:
        print(f"{Colors.RED}Error in port scanning: {e}{Colors.RESET}")

# Enhanced Subdomain enumeration
def subdomain_scan(domain):
    print(f"\n{Colors.GREEN}[+] Subdomain Scanner for {domain}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Scanning for common subdomains...{Colors.RESET}")
    loading_animation("Enumerating subdomains")
    
    # Common subdomains list
    subdomains = [
        "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk", "ns2",
        "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test", "ns", "blog", "pop3",
        "dev", "www2", "admin", "forum", "news", "vpn", "ns3", "mail2", "new", "mysql", "old",
        "lists", "support", "mobile", "mx", "static", "docs", "beta", "shop", "sql", "secure",
        "demo", "cp", "calendar", "wiki", "web", "media", "email", "images", "img", "www1",
        "intranet", "portal", "video", "sip", "dns2", "api", "cdn", "stats", "dns1", "search",
        "staging", "server", "mx1", "chat", "download", "remote", "db", "forums", "store", "ad",
        "newsite", "mirror", "apps", "host", "feeds", "files", "ssl", "crm", "webadmin", "cdn2",
        "dns", "cdn1", "backup", "monitor", "mail1", "mx2", "cloud", "payment", "ftp2", "git",
        "owa", "exchange", "app", "archive", "streaming", "irc", "vps", "svn", "ssh", "cms",
        "web1", "squirrelmail", "roundcube", "help", "mysql2", "mysql1", "direct", "direct-connect",
        "reports", "smtp2", "smtp1", "panel", "photos", "pic", "pics", "photo", "image", "img2"
    ]
    
    found_subdomains = []
    
    print(f"\n{Colors.GREEN}Checking subdomains...{Colors.RESET}")
    
    def check_subdomain(subdomain):
        full_domain = f"{subdomain}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            found_subdomains.append((full_domain, ip))
            print(f"{Colors.GREEN}[+] Found: {full_domain} -> {ip}{Colors.RESET}")
        except:
            pass
    
    # Check subdomains with threading for faster results
    threads = []
    for subdomain in subdomains:
        t = threading.Thread(target=check_subdomain, args=(subdomain,))
        threads.append(t)
        t.start()
        
        # Limit concurrent threads to avoid overwhelming the system
        if len(threads) >= 50:
            for t in threads:
                t.join()
            threads = []
    
    # Wait for remaining threads
    for t in threads:
        t.join()
    
    if found_subdomains:
        print(f"\n{Colors.GREEN}Found {len(found_subdomains)} subdomains:{Colors.RESET}")
        for subdomain, ip in found_subdomains:
            print(f"  {subdomain} -> {ip}")
    else:
        print(f"{Colors.RED}No subdomains found{Colors.RESET}")

# Enhanced GitHub repository cloning
def clone_repo():
    url = input(f"\n{Colors.CYAN}Enter GitHub repository URL: {Colors.RESET}")
    if not url:
        print(f"{Colors.RED}No URL provided{Colors.RESET}")
        return
    
    print(f"{Colors.YELLOW}[*] Cloning repository...{Colors.RESET}")
    loading_animation("Cloning from GitHub")
    
    try:
        # Extract repo name from URL
        repo_name = url.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        
        # Create a directory for the cloned repo
        if not os.path.exists("cloned_repos"):
            os.makedirs("cloned_repos")
        
        # Change to cloned_repos directory
        os.chdir("cloned_repos")
        
        # Clone the repository
        result = subprocess.run(['git', 'clone', url], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}[+] Repository cloned successfully to cloned_repos/{repo_name}{Colors.RESET}")
            
            # Show repo info
            os.chdir(repo_name)
            result = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"\n{Colors.GREEN}Last 5 commits:{Colors.RESET}")
                print(result.stdout)
            
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.GREEN}Remote info:{Colors.RESET}")
                print(result.stdout)
                
        else:
            print(f"{Colors.RED}Error cloning repository: {result.stderr}{Colors.RESET}")
        
        # Change back to original directory
        os.chdir("../..")
            
    except Exception as e:
        print(f"{Colors.RED}Error cloning repository: {e}{Colors.RESET}")

# Comprehensive URL information gathering
def comprehensive_url_info(url):
    print(f"\n{Colors.GREEN}[+] Comprehensive Analysis for {url}{Colors.RESET}")
    
    domain = extract_domain(url)
    print(f"{Colors.YELLOW}[*] Extracted domain: {domain}{Colors.RESET}")
    
    # Perform all checks
    resolve_dns(domain)
    geo_ip(domain)
    http_headers(domain)
    meta_info(domain)
    read_robots_sitemap(domain)
    whois_lookup(domain)
    port_scan(domain)
    subdomain_scan(domain)
    
    print(f"\n{Colors.GREEN}[+] Comprehensive analysis completed!{Colors.RESET}")

# Main menu
def main_menu():
    while True:
        banner()
        print(f"{Colors.BOLD}Select an option:{Colors.RESET}")
        print(f"{Colors.CYAN} 1){Colors.RESET} DNS Resolution (A, AAAA, MX, NS, TXT, CNAME, SOA)")
        print(f"{Colors.CYAN} 2){Colors.RESET} GeoIP Lookup")
        print(f"{Colors.CYAN} 3){Colors.RESET} HTTP Headers Analysis")
        print(f"{Colors.CYAN} 4){Colors.RESET} Website Metadata Extraction")
        print(f"{Colors.CYAN} 5){Colors.RESET} Robots.txt and Sitemap Analysis")
        print(f"{Colors.CYAN} 6){Colors.RESET} WHOIS Lookup")
        print(f"{Colors.CYAN} 7){Colors.RESET} Port Scanner")
        print(f"{Colors.CYAN} 8){Colors.RESET} Subdomain Scanner")
        print(f"{Colors.CYAN} 9){Colors.RESET} Clone GitHub Repository")
        print(f"{Colors.CYAN}10){Colors.RESET} Comprehensive URL Analysis (ALL IN ONE)")
        print(f"{Colors.CYAN} 0){Colors.RESET} Exit")
        print()
        
        choice = input(f"{Colors.WHITE}Enter your choice: {Colors.RESET}")
        
        if choice == "1":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            resolve_dns(domain)
        elif choice == "2":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            geo_ip(domain)
        elif choice == "3":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            http_headers(domain)
        elif choice == "4":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            meta_info(domain)
        elif choice == "5":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            read_robots_sitemap(domain)
        elif choice == "6":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            whois_lookup(domain)
        elif choice == "7":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            port_scan(domain)
        elif choice == "8":
            domain = input(f"{Colors.CYAN}Enter domain: {Colors.RESET}")
            subdomain_scan(domain)
        elif choice == "9":
            clone_repo()
        elif choice == "10":
            url = input(f"{Colors.CYAN}Enter URL: {Colors.RESET}")
            comprehensive_url_info(url)
        elif choice == "0":
            print(f"{Colors.GREEN}Thank you for using Omar-tool Professional!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Tool terminated by user{Colors.RESET}")