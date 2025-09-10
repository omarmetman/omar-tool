#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

try:
    import ssl
    SSLLIB = True
except ImportError:
    SSLLIB = False

try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    CRYPTOLIB = True
except ImportError:
    CRYPTOLIB = False

# Enhanced ANSI colors for professional UI
class Colors:
    RED = "\033[38;5;196m"
    GREEN = "\033[38;5;46m"
    BLUE = "\033[38;5;27m"
    YELLOW = "\033[38;5;226m"
    CYAN = "\033[38;5;51m"
    PURPLE = "\033[38;5;129m"
    WHITE = "\033[38;5;255m"
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;205m"
    DARK_CYAN = "\033[38;5;30m"
    GRAY = "\033[38;5;240m"
    DARK_GREEN = "\033[38;5;22m"
    
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    
    # Background colors
    BG_BLUE = "\033[48;5;17m"
    BG_DARK = "\033[48;5;233m"
    BG_GRAY = "\033[48;5;236m"

# Clear screen function
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

# Display a professional banner
def banner():
    clear_screen()
    print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}")
    print("                                                                              ")
    print("    ██████╗ ███╗   ███╗ █████╗ ██████╗         ████████╗ ██████╗  ██████╗ ██╗     ")
    print("   ██╔═══██╗████╗ ████║██╔══██╗██╔══██╗        ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ")
    print("   ██║   ██║██╔████╔██║███████║██████╔╝█████╗    ██║   ██║   ██║██║   ██║██║     ")
    print("   ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗╚════╝    ██║   ██║   ██║██║   ██║██║     ")
    print("   ╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║          ██║   ╚██████╔╝╚██████╔╝███████╗")
    print("    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝")
    print("                                                                              ")
    print(f"{Colors.RESET}")
    print(f"{Colors.ORANGE}{Colors.BOLD}                           Omar M. Etman{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}                    Ultimate Reconnaissance Tool v3.0{Colors.RESET}")
    print(f"{Colors.YELLOW}                    Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.PURPLE}                   ============================================{Colors.RESET}")
    print()

# Loading animation with progress
def loading_animation(message, duration=2):
    end_time = time.time() + duration
    symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    i = 0
    progress = 0
    while time.time() < end_time:
        progress = min(100, int((1 - (end_time - time.time()) / duration) * 100))
        print(f"\r{Colors.YELLOW}{symbols[i]} {message} [{progress}%]{Colors.RESET}", end="")
        i = (i + 1) % len(symbols)
        time.sleep(0.1)
    print("\r" + " " * (len(message) + 15) + "\r", end="")

# Print section header
def print_section_header(title):
    print(f"\n{Colors.BG_GRAY}{Colors.WHITE}{Colors.BOLD} {title} {Colors.RESET}")

# Print subsection header
def print_subsection_header(title):
    print(f"\n{Colors.DARK_CYAN}{Colors.BOLD} {title} {Colors.RESET}")

# Print information line
def print_info(label, value, color=Colors.WHITE):
    print(f"{Colors.GREEN}{label}:{Colors.RESET} {color}{value}{Colors.RESET}")

# Print warning line
def print_warning(message):
    print(f"{Colors.YELLOW}[!] {message}{Colors.RESET}")

# Print error line
def print_error(message):
    print(f"{Colors.RED}[✗] {message}{Colors.RESET}")

# Print success line
def print_success(message):
    print(f"{Colors.GREEN}[✓] {message}{Colors.RESET}")

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

# Get IP information
def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return data
    except:
        return None

# Check if website uses CDN
def check_cdn(headers):
    cdn_indicators = ['cloudflare', 'akamai', 'fastly', 'cloudfront', 'incapdns']
    server = headers.get('Server', '').lower()
    for cdn in cdn_indicators:
        if cdn in server:
            return cdn.capitalize()
    
    # Check for other CDN headers
    for header, value in headers.items():
        for cdn in cdn_indicators:
            if cdn in value.lower():
                return cdn.capitalize()
    
    return "Not detected"

# Check security headers
def check_security_headers(headers):
    security_headers = {
        'Strict-Transport-Security': 'HSTS enabled',
        'Content-Security-Policy': 'CSP implemented',
        'X-Content-Type-Options': 'MIME sniffing protection',
        'X-Frame-Options': 'Clickjacking protection',
        'X-XSS-Protection': 'XSS protection',
        'Referrer-Policy': 'Referrer policy set',
        'Permissions-Policy': 'Permissions policy set',
        'Feature-Policy': 'Feature policy set'
    }
    
    results = {}
    for header, description in security_headers.items():
        if header in headers:
            results[header] = f"{Colors.GREEN}✓ {description}: {headers[header]}{Colors.RESET}"
        else:
            results[header] = f"{Colors.RED}✗ {description} missing{Colors.RESET}"
    
    return results

# Check SSL certificate
def check_ssl_certificate(domain):
    if not SSLLIB:
        return None
    
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                
                if CRYPTOLIB:
                    cert_obj = x509.load_der_x509_certificate(cert, default_backend())
                    issuer = cert_obj.issuer.rfc4514_string()
                    subject = cert_obj.subject.rfc4514_string()
                    not_before = cert_obj.not_valid_before
                    not_after = cert_obj.not_valid_after
                    
                    return {
                        'issuer': issuer,
                        'subject': subject,
                        'valid_from': not_before,
                        'valid_to': not_after,
                        'days_remaining': (not_after - datetime.now()).days
                    }
                else:
                    return {'raw': cert}
    except:
        return None

# Get website technologies
def get_technologies(headers, html_content):
    technologies = []
    
    # Check server header
    server = headers.get('Server', '')
    if server:
        technologies.append(f"Server: {server}")
    
    # Check powered by header
    powered_by = headers.get('X-Powered-By', '')
    if powered_by:
        technologies.append(f"Powered By: {powered_by}")
    
    # Check common framework indicators
    if BS4LIB:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for WordPress
        if soup.find('meta', attrs={'name': 'generator', 'content': re.compile('wordpress', re.I)}):
            technologies.append("WordPress")
        elif soup.find('link', attrs={'href': re.compile('/wp-content/', re.I)}):
            technologies.append("WordPress")
        elif soup.find('script', attrs={'src': re.compile('/wp-includes/', re.I)}):
            technologies.append("WordPress")
        
        # Check for Joomla
        if soup.find('meta', attrs={'name': 'generator', 'content': re.compile('joomla', re.I)}):
            technologies.append("Joomla")
        elif soup.find('script', attrs={'src': re.compile('/media/system/', re.I)}):
            technologies.append("Joomla")
        
        # Check for Drupal
        if soup.find('meta', attrs={'name': 'generator', 'content': re.compile('drupal', re.I)}):
            technologies.append("Drupal")
        elif soup.find('script', attrs={'src': re.compile('/sites/all/', re.I)}):
            technologies.append("Drupal")
        
        # Check for jQuery
        if soup.find('script', attrs={'src': re.compile('jquery', re.I)}):
            technologies.append("jQuery")
        
        # Check for Bootstrap
        if soup.find('link', attrs={'href': re.compile('bootstrap', re.I)}):
            technologies.append("Bootstrap")
    
    return technologies

# Get social media links
def get_social_links(html_content):
    social_links = {}
    
    if BS4LIB:
        soup = BeautifulSoup(html_content, 'html.parser')
        social_patterns = {
            'facebook': r'facebook\.com',
            'twitter': r'twitter\.com',
            'instagram': r'instagram\.com',
            'linkedin': r'linkedin\.com',
            'youtube': r'youtube\.com',
            'pinterest': r'pinterest\.com',
            'tiktok': r'tiktok\.com'
        }
        
        for platform, pattern in social_patterns.items():
            links = soup.find_all('a', href=re.compile(pattern, re.I))
            if links:
                social_links[platform] = [link.get('href') for link in links[:3]]  # Limit to 3 links per platform
    
    return social_links

# Get email addresses
def get_emails(html_content):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html_content)
    return list(set(emails))  # Remove duplicates

# Get phone numbers
def get_phone_numbers(html_content):
    phone_patterns = [
        r'\+?[0-9][0-9\s\-\(\)]{7,}[0-9]',  # International format
        r'\([0-9]{3}\)\s?[0-9]{3}-[0-9]{4}',  # US format (123) 456-7890
        r'[0-9]{3}-[0-9]{3}-[0-9]{4}'  # US format 123-456-7890
    ]
    
    phones = []
    for pattern in phone_patterns:
        phones.extend(re.findall(pattern, html_content))
    
    return list(set(phones))

# Enhanced DNS resolution function
def resolve_dns(domain):
    print_section_header(f"DNS RESOLUTION FOR {domain}")
    print(f"{Colors.YELLOW}[*] Resolving DNS records...{Colors.RESET}")
    loading_animation("Querying DNS servers")
    
    if not DNSLIB:
        print_error("dnspython library not installed. Install it with: pip install dnspython")
        return
    
    try:
        # A Records
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            print_subsection_header("A RECORDS")
            for record in a_records:
                ip_info = get_ip_info(record.address)
                if ip_info and ip_info.get('status') == 'success':
                    print_info("IP", f"{record.address} ({ip_info.get('city', 'Unknown')}, {ip_info.get('country', 'Unknown')})")
                else:
                    print_info("IP", record.address)
        except:
            print_error("No A records found")
        
        # AAAA Records
        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            print_subsection_header("AAAA RECORDS (IPv6)")
            for record in aaaa_records:
                print_info("IPv6", record.address)
        except:
            print_warning("No AAAA records found")
        
        # MX Records
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            print_subsection_header("MX RECORDS (MAIL SERVERS)")
            for record in mx_records:
                print_info("Mail Server", f"{record.exchange} (Priority: {record.preference})")
        except:
            print_warning("No MX records found")
        
        # NS Records
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            print_subsection_header("NS RECORDS (NAME SERVERS)")
            for record in ns_records:
                print_info("Name Server", record.target)
        except:
            print_error("No NS records found")
        
        # TXT Records
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            print_subsection_header("TXT RECORDS")
            for record in txt_records:
                for string in record.strings:
                    print_info("TXT", string.decode() if isinstance(string, bytes) else string)
        except:
            print_warning("No TXT records found")
        
        # CNAME Records
        try:
            cname_records = dns.resolver.resolve(domain, 'CNAME')
            print_subsection_header("CNAME RECORDS")
            for record in cname_records:
                print_info("CNAME", record.target)
        except:
            print_warning("No CNAME records found")
        
        # SOA Records
        try:
            soa_records = dns.resolver.resolve(domain, 'SOA')
            print_subsection_header("SOA RECORDS")
            for record in soa_records:
                print_info("Primary NS", record.mname)
                print_info("Admin Email", record.rname)
                print_info("Serial", record.serial)
                print_info("Refresh", record.refresh)
                print_info("Retry", record.retry)
                print_info("Expire", record.expire)
                print_info("Minimum TTL", record.minimum)
        except:
            print_warning("No SOA records found")
            
    except Exception as e:
        print_error(f"DNS resolution error: {e}")

# Enhanced GeoIP lookup
def geo_ip(domain):
    print_section_header(f"GEOIP LOOKUP FOR {domain}")
    print(f"{Colors.YELLOW}[*] Looking up GeoIP information...{Colors.RESET}")
    loading_animation("Querying GeoIP database")
    
    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data["status"] == "success":
            print_subsection_header("LOCATION INFORMATION")
            print_info("IP Address", data['query'])
            print_info("Country", f"{data['country']} ({data['countryCode']})")
            print_info("Region", f"{data['regionName']} ({data['region']})")
            print_info("City", data['city'])
            print_info("ZIP Code", data['zip'])
            print_info("Coordinates", f"{data['lat']}, {data['lon']}")
            print_info("Timezone", data['timezone'])
            
            print_subsection_header("NETWORK INFORMATION")
            print_info("ISP", data['isp'])
            print_info("Organization", data['org'])
            print_info("AS", data['as'])
        else:
            print_error("Failed to retrieve GeoIP information")
    except Exception as e:
        print_error(f"GeoIP lookup error: {e}")

# Enhanced HTTP headers analysis
def http_headers(domain):
    print_section_header(f"HTTP HEADERS ANALYSIS FOR {domain}")
    print(f"{Colors.YELLOW}[*] Retrieving HTTP headers...{Colors.RESET}")
    loading_animation("Connecting to server")
    
    try:
        # Try with HTTPS first
        try:
            response = requests.get(f"https://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            protocol = "HTTPS"
        except:
            # Fallback to HTTP if HTTPS fails
            try:
                response = requests.get(f"http://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
                protocol = "HTTP"
            except Exception as e:
                print_error(f"Failed to connect: {e}")
                return
        
        print_subsection_header("BASIC INFORMATION")
        print_info("Protocol", protocol)
        print_info("Status Code", response.status_code)
        print_info("Server", response.headers.get('Server', 'Not specified'))
        print_info("Content Type", response.headers.get('Content-Type', 'Not specified'))
        print_info("Content Length", response.headers.get('Content-Length', 'Not specified'))
        print_info("Connection", response.headers.get('Connection', 'Not specified'))
        
        # Check CDN
        cdn = check_cdn(response.headers)
        print_info("CDN", cdn)
        
        # SSL Certificate Info
        if protocol == "HTTPS":
            ssl_info = check_ssl_certificate(domain)
            if ssl_info:
                print_subsection_header("SSL CERTIFICATE INFORMATION")
                if 'issuer' in ssl_info:
                    print_info("Issuer", ssl_info['issuer'])
                    print_info("Subject", ssl_info['subject'])
                    print_info("Valid From", ssl_info['valid_from'].strftime('%Y-%m-%d'))
                    print_info("Valid To", ssl_info['valid_to'].strftime('%Y-%m-%d'))
                    print_info("Days Remaining", ssl_info['days_remaining'])
        
        # Security headers check
        security_headers = check_security_headers(response.headers)
        print_subsection_header("SECURITY HEADERS")
        for header, status in security_headers.items():
            print(f"  {header}: {status}")
        
        # Print all headers
        print_subsection_header("ALL HEADERS")
        for header, value in response.headers.items():
            print(f"  {Colors.GRAY}{header}: {Colors.WHITE}{value}{Colors.RESET}")
            
    except Exception as e:
        print_error(f"HTTP headers analysis error: {e}")

# Enhanced Website metadata extraction
def meta_info(domain):
    print_section_header(f"WEBSITE METADATA EXTRACTION FOR {domain}")
    print(f"{Colors.YELLOW}[*] Extracting website metadata...{Colors.RESET}")
    loading_animation("Analyzing page content")
    
    if not BS4LIB:
        print_error("BeautifulSoup library not installed. Install it with: pip install beautifulsoup4")
        return
    
    try:
        # Try with HTTPS first
        try:
            response = requests.get(f"https://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        except:
            # Fallback to HTTP if HTTPS fails
            try:
                response = requests.get(f"http://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            except Exception as e:
                print_error(f"Failed to connect: {e}")
                return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Title
        title = soup.find('title')
        print_subsection_header("PAGE INFORMATION")
        print_info("Title", title.string if title else 'Not found')
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        print_info("Meta Description", meta_desc['content'] if meta_desc and 'content' in meta_desc.attrs else 'Not found')
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        print_info("Meta Keywords", meta_keywords['content'] if meta_keywords and 'content' in meta_keywords.attrs else 'Not found')
        
        # Viewport
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        print_info("Viewport", viewport['content'] if viewport and 'content' in viewport.attrs else 'Not found')
        
        # Charset
        charset = soup.find('meta', attrs={'charset': True})
        if not charset:
            charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        print_info("Charset", charset['charset'] if charset and 'charset' in charset.attrs else charset['content'] if charset and 'content' in charset.attrs else 'Not found')
        
        # Language
        language = soup.html.get('lang') if soup.html else 'Not found'
        print_info("Language", language)
        
        # Open Graph tags
        print_subsection_header("OPEN GRAPH TAGS")
        og_tags = soup.find_all('meta', attrs={'property': re.compile(r'^og:', re.I)})
        if og_tags:
            for tag in og_tags:
                print_info(tag['property'], tag['content'] if 'content' in tag.attrs else 'No content')
        else:
            print_warning("No Open Graph tags found")
        
        # Twitter Card tags
        print_subsection_header("TWITTER CARD TAGS")
        twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:', re.I)})
        if twitter_tags:
            for tag in twitter_tags:
                print_info(tag['name'], tag['content'] if 'content' in tag.attrs else 'No content')
        else:
            print_warning("No Twitter Card tags found")
        
        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        print_info("Canonical URL", canonical['href'] if canonical and 'href' in canonical.attrs else 'Not found')
        
        # Technologies
        technologies = get_technologies(response.headers, response.text)
        if technologies:
            print_subsection_header("DETECTED TECHNOLOGIES")
            for tech in technologies:
                print_info("Technology", tech)
        
        # Social Media Links
        social_links = get_social_links(response.text)
        if social_links:
            print_subsection_header("SOCIAL MEDIA LINKS")
            for platform, links in social_links.items():
                for link in links:
                    print_info(platform.capitalize(), link)
        
        # Email addresses
        emails = get_emails(response.text)
        if emails:
            print_subsection_header("EMAIL ADDRESSES")
            for email in emails:
                print_info("Email", email)
        
        # Phone numbers
        phones = get_phone_numbers(response.text)
        if phones:
            print_subsection_header("PHONE NUMBERS")
            for phone in phones:
                print_info("Phone", phone)
        
    except Exception as e:
        print_error(f"Metadata extraction error: {e}")

# Enhanced Robots.txt and sitemap.xml analysis
def read_robots_sitemap(domain):
    print_section_header(f"ROBOTS.TXT AND SITEMAP ANALYSIS FOR {domain}")
    
    # Check robots.txt
    try:
        response = requests.get(f"http://{domain}/robots.txt", timeout=10)
        if response.status_code == 200:
            print_subsection_header("ROBOTS.TXT FOUND")
            print(f"{Colors.WHITE}{response.text}{Colors.RESET}")
            
            # Analyze robots.txt
            disallowed = []
            allowed = []
            sitemaps = []
            
            for line in response.text.split('\n'):
                line = line.strip()
                if line.startswith('Disallow:'):
                    disallowed.append(line.split(':', 1)[1].strip())
                elif line.startswith('Allow:'):
                    allowed.append(line.split(':', 1)[1].strip())
                elif line.startswith('Sitemap:'):
                    sitemaps.append(line.split(':', 1)[1].strip())
            
            if disallowed:
                print_subsection_header("DISALLOWED PATHS")
                for path in disallowed:
                    print_info("Disallowed", path)
            
            if allowed:
                print_subsection_header("ALLOWED PATHS")
                for path in allowed:
                    print_info("Allowed", path)
            
            if sitemaps:
                print_subsection_header("SITEMAP REFERENCES")
                for sitemap in sitemaps:
                    print_info("Sitemap", sitemap)
        else:
            print_error("robots.txt not found or not accessible")
    except:
        print_error("Failed to retrieve robots.txt")
    
    # Check sitemap.xml
    try:
        response = requests.get(f"http://{domain}/sitemap.xml", timeout=10)
        if response.status_code == 200:
            print_subsection_header("SITEMAP.XML FOUND")
            
            # Try to parse the sitemap
            try:
                soup = BeautifulSoup(response.content, 'xml')
                urls = soup.find_all('url')
                if urls:
                    print_info("URLs in sitemap", len(urls))
                    print("First 10 URLs:")
                    for url in urls[:10]:
                        loc = url.find('loc')
                        if loc:
                            print(f"  {Colors.GRAY}{loc.text}{Colors.RESET}")
                    if len(urls) > 10:
                        print(f"  {Colors.GRAY}... and {len(urls) - 10} more{Colors.RESET}")
                else:
                    print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            except:
                print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        else:
            print_error("sitemap.xml not found or not accessible")
    except:
        print_error("Failed to retrieve sitemap.xml")

# Enhanced WHOIS lookup
def whois_lookup(domain):
    print_section_header(f"WHOIS LOOKUP FOR {domain}")
    
    if not WHOISLIB:
        print_error("whois library not installed. Install it with: pip install python-whois")
        return
    
    print(f"{Colors.YELLOW}[*] Performing WHOIS lookup...{Colors.RESET}")
    loading_animation("Querying WHOIS database")
    
    try:
        w = whois.whois(domain)
        
        print_subsection_header("DOMAIN INFORMATION")
        if w.domain_name:
            if isinstance(w.domain_name, list):
                print_info("Domain Name", w.domain_name[0])
            else:
                print_info("Domain Name", w.domain_name)
        
        if w.registrar:
            print_info("Registrar", w.registrar)
        
        if w.whois_server:
            print_info("WHOIS Server", w.whois_server)
        
        print_subsection_header("DATES")
        if w.creation_date:
            if isinstance(w.creation_date, list):
                print_info("Creation Date", w.creation_date[0])
            else:
                print_info("Creation Date", w.creation_date)
        
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                print_info("Expiration Date", w.expiration_date[0])
            else:
                print_info("Expiration Date", w.expiration_date)
        
        if w.updated_date:
            if isinstance(w.updated_date, list):
                print_info("Updated Date", w.updated_date[0])
            else:
                print_info("Updated Date", w.updated_date)
        
        print_subsection_header("NAME SERVERS")
        if w.name_servers:
            for ns in w.name_servers:
                print_info("Name Server", ns)
        
        print_subsection_header("STATUS")
        if w.status:
            if isinstance(w.status, list):
                for status in w.status:
                    print_info("Status", status)
            else:
                print_info("Status", w.status)
        
        print_subsection_header("REGISTRANT INFORMATION")
        if w.emails:
            if isinstance(w.emails, list):
                for email in w.emails:
                    print_info("Email", email)
            else:
                print_info("Email", w.emails)
        
        if w.org:
            print_info("Organization", w.org)
        
        if w.address:
            print_info("Address", w.address)
        
        if w.city:
            print_info("City", w.city)
        
        if w.state:
            print_info("State", w.state)
        
        if w.zipcode:
            print_info("ZIP Code", w.zipcode)
        
        if w.country:
            print_info("Country", w.country)
            
    except Exception as e:
        print_error(f"WHOIS lookup error: {e}")

# Enhanced Port scanner
def port_scan(domain):
    print_section_header(f"PORT SCANNER FOR {domain}")
    print(f"{Colors.YELLOW}[*] Scanning common ports...{Colors.RESET}")
    loading_animation("Scanning ports")
    
    try:
        ip = socket.gethostbyname(domain)
        print_info("Target IP", ip)
        
        # Common ports to scan with service names
        ports = [
            (21, "FTP"),
            (22, "SSH"),
            (23, "Telnet"),
            (25, "SMTP"),
            (53, "DNS"),
            (80, "HTTP"),
            (110, "POP3"),
            (111, "RPCbind"),
            (135, "MSRPC"),
            (139, "NetBIOS-SSN"),
            (143, "IMAP"),
            (443, "HTTPS"),
            (445, "SMB"),
            (993, "IMAPS"),
            (995, "POP3S"),
            (1723, "PPTP"),
            (3306, "MySQL"),
            (3389, "RDP"),
            (5900, "VNC"),
            (8080, "HTTP-Alt")
        ]
        
        open_ports = []
        
        print_subsection_header("PORT SCAN RESULTS")
        print(f"{Colors.GREEN}Port\tStatus\tService{Colors.RESET}")
        print(f"{Colors.PURPLE}----\t------\t-------{Colors.RESET}")
        
        def scan_port(port_info):
            port, service = port_info
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    print(f"{port}\t{Colors.GREEN}Open{Colors.RESET}\t{service}")
                    open_ports.append((port, service))
                else:
                    print(f"{port}\t{Colors.RED}Closed{Colors.RESET}\t{service}")
            except:
                print(f"{port}\t{Colors.RED}Error{Colors.RESET}\t{service}")
        
        # Scan ports with threading for faster results
        threads = []
        for port_info in ports:
            t = threading.Thread(target=scan_port, args=(port_info,))
            threads.append(t)
            t.start()
            
            # Limit concurrent threads to avoid overwhelming the system
            if len(threads) >= 10:
                for t in threads:
                    t.join()
                threads = []
        
        # Wait for remaining threads
        for t in threads:
            t.join()
        
        if open_ports:
            print_subsection_header("SUMMARY")
            print_info("Open ports found", len(open_ports))
            for port, service in open_ports:
                print_info(f"Port {port}", service)
        else:
            print_warning("No open ports found")
            
    except Exception as e:
        print_error(f"Port scanning error: {e}")

# Enhanced Subdomain enumeration
def subdomain_scan(domain):
    print_section_header(f"SUBDOMAIN SCANNER FOR {domain}")
    print(f"{Colors.YELLOW}[*] Scanning for common subdomains...{Colors.RESET}")
    loading_animation("Enumerating subdomains")
    
    # Extended common subdomains list
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
        "reports", "smtp2", "smtp1", "panel", "photos", "pic", "pics", "photo", "image", "img2",
        "assets", "cdn3", "cdn4", "cdn5", "cdn6", "cdn7", "cdn8", "cdn9", "cdn10", "cdn11",
        "cdn12", "cdn13", "cdn14", "cdn15", "cdn16", "cdn17", "cdn18", "cdn19", "cdn20", "cdn21",
        "cdn22", "cdn23", "cdn24", "cdn25", "cdn26", "cdn27", "cdn28", "cdn29", "cdn30", "cdn31",
        "cdn32", "cdn33", "cdn34", "cdn35", "cdn36", "cdn37", "cdn38", "cdn39", "cdn40", "cdn41",
        "cdn42", "cdn43", "cdn44", "cdn45", "cdn46", "cdn47", "cdn48", "cdn49", "cdn50", "cdn51",
        "cdn52", "cdn53", "cdn54", "cdn55", "cdn56", "cdn57", "cdn58", "cdn59", "cdn60", "cdn61",
        "cdn62", "cdn63", "cdn64", "cdn65", "cdn66", "cdn67", "cdn68", "cdn69", "cdn70", "cdn71",
        "cdn72", "cdn73", "cdn74", "cdn75", "cdn76", "cdn77", "cdn78", "cdn79", "cdn80", "cdn81",
        "cdn82", "cdn83", "cdn84", "cdn85", "cdn86", "cdn87", "cdn88", "cdn89", "cdn90", "cdn91",
        "cdn92", "cdn93", "cdn94", "cdn95", "cdn96", "cdn97", "cdn98", "cdn99", "cdn100", "cdn101"
    ]
    
    found_subdomains = []
    
    print_subsection_header("SUBDOMAIN SCAN RESULTS")
    
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
        print_subsection_header("SUMMARY")
        print_info("Subdomains found", len(found_subdomains))
        for subdomain, ip in found_subdomains:
            print_info(subdomain, ip)
    else:
        print_warning("No subdomains found")

# Enhanced GitHub repository cloning
def clone_repo():
    url = input(f"\n{Colors.CYAN}Enter GitHub repository URL: {Colors.RESET}")
    if not url:
        print_error("No URL provided")
        return
    
    print_section_header(f"CLONING GITHUB REPOSITORY")
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
            print_success(f"Repository cloned successfully to cloned_repos/{repo_name}")
            
            # Show repo info
            os.chdir(repo_name)
            
            print_subsection_header("REPOSITORY INFORMATION")
            
            # Get last 5 commits
            result = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True)
            if result.returncode == 0:
                print_info("Last 5 commits", "")
                print(f"{Colors.GRAY}{result.stdout}{Colors.RESET}")
            
            # Get remote info
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if result.returncode == 0:
                print_info("Remote info", "")
                print(f"{Colors.GRAY}{result.stdout}{Colors.RESET}")
            
            # Get branch info
            result = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True)
            if result.returncode == 0:
                print_info("Branches", "")
                print(f"{Colors.GRAY}{result.stdout}{Colors.RESET}")
                
        else:
            print_error(f"Error cloning repository: {result.stderr}")
        
        # Change back to original directory
        os.chdir("../..")
            
    except Exception as e:
        print_error(f"Error cloning repository: {e}")

# Comprehensive URL information gathering
def comprehensive_url_info(url):
    print_section_header(f"COMPREHENSIVE ANALYSIS FOR {url}")
    
    domain = extract_domain(url)
    print_info("Extracted domain", domain)
    
    # Perform all checks
    resolve_dns(domain)
    geo_ip(domain)
    http_headers(domain)
    meta_info(domain)
    read_robots_sitemap(domain)
    whois_lookup(domain)
    port_scan(domain)
    subdomain_scan(domain)
    
    print_success("Comprehensive analysis completed!")

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
            print_success("Thank you for using Omar-tool Professional!")
            sys.exit(0)
        else:
            print_error("Invalid choice. Please try again.")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Tool terminated by user{Colors.RESET}")