#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Omar-tool Professional v4.0 - Ultimate OSINT & Social Media Intelligence Tool
Author: Omar M. Etman
Website: https://omarmetman.vercel.app
"""

import os
import sys
import re
import json
import time
import requests
import socket
import random
import threading
import csv
import sqlite3
import dns.resolver
import whois
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, quote, unquote
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Try to import arabic-reshaper if available
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False

# ANSI colors for mobile-friendly UI
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    PURPLE = "\033[95m"
    WHITE = "\033[97m"
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;205m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BG_BLUE = "\033[44m"
    BG_GRAY = "\033[100m"

# Mobile-friendly display functions
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header(text):
    print(f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD} {text} {Colors.RESET}")

def print_section(text):
    print(f"\n{Colors.BG_GRAY}{Colors.WHITE}{Colors.BOLD} {text} {Colors.RESET}")

def print_subsection(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD} {text} {Colors.RESET}")

def print_info(label, value):
    print(f"{Colors.GREEN}{label}:{Colors.RESET} {Colors.WHITE}{value}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}[!] {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}[✗] {text}{Colors.RESET}")

def print_success(text):
    print(f"{Colors.GREEN}[✓] {text}{Colors.RESET}")

def print_bullet(text):
    print(f"{Colors.WHITE}• {text}{Colors.RESET}")

def format_arabic(text):
    if ARABIC_SUPPORT and any('\u0600' <= c <= '\u06FF' for c in text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

def loading_animation(text, duration=2):
    end_time = time.time() + duration
    symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    i = 0
    while time.time() < end_time:
        progress = min(100, int((1 - (end_time - time.time()) / duration) * 100))
        sys.stdout.write(f"\r{Colors.YELLOW}{symbols[i]} {text} [{progress}%]{Colors.RESET}")
        sys.stdout.flush()
        i = (i + 1) % len(symbols)
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(text) + 15) + "\r")
    sys.stdout.flush()

def mobile_banner():
    clear_screen()
    print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}")
    print(" " + "="*50)
    print("            O M A R - T O O L  v4.0")
    print(" " + "="*50)
    print(f"{Colors.RESET}")
    print(f"{Colors.ORANGE}{Colors.BOLD}           Omar M. Etman{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}    Ultimate OSINT & Social Media Tool{Colors.RESET}")
    print(f"{Colors.YELLOW}    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.PURPLE}    Website: https://omarmetman.vercel.app{Colors.RESET}")
    print(f"{Colors.PURPLE}    " + "="*50 + f"{Colors.RESET}")

# Common User Agents for requests
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

# Database setup for storing collected information
def setup_database():
    conn = sqlite3.connect('osint_data.db')
    c = conn.cursor()
    
    # Create tables for different platforms
    c.execute('''CREATE TABLE IF NOT EXISTS facebook_data
                 (id INTEGER PRIMARY KEY, username TEXT, name TEXT, profile_url TEXT, 
                 about TEXT, location TEXT, joined_date TEXT, friends_count INTEGER,
                 extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS instagram_data
                 (id INTEGER PRIMARY KEY, username TEXT, full_name TEXT, bio TEXT,
                 followers_count INTEGER, following_count INTEGER, posts_count INTEGER,
                 is_private INTEGER, is_verified INTEGER, profile_pic_url TEXT,
                 extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tiktok_data
                 (id INTEGER PRIMARY KEY, username TEXT, nickname TEXT, signature TEXT,
                 followers_count INTEGER, following_count INTEGER, likes_count INTEGER,
                 videos_count INTEGER, verified INTEGER, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS website_data
                 (id INTEGER PRIMARY KEY, url TEXT, title TEXT, ip_address TEXT,
                 server TEXT, technologies TEXT, whois_data TEXT, dns_records TEXT,
                 extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS password_patterns
                 (id INTEGER PRIMARY KEY, username TEXT, platform TEXT, pattern TEXT,
                 generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    return conn

# ==================== FACEBOOK MODULE ====================
def facebook_module():
    print_header("FACEBOOK INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Extract information from profile URL")
    print("2. Search by username")
    print("3. View saved Facebook data")
    print("4. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        url = input(f"{Colors.YELLOW}Enter Facebook profile URL: {Colors.RESET}")
        username = extract_facebook_username(url)
        if username:
            print_info("Extracted username", username)
            get_facebook_data(username)
        else:
            print_error("Could not extract username from URL")
    
    elif choice == "2":
        username = input(f"{Colors.YELLOW}Enter Facebook username: {Colors.RESET}")
        get_facebook_data(username)
    
    elif choice == "3":
        view_facebook_data()
    
    elif choice == "4":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    facebook_module()

def extract_facebook_username(url):
    patterns = [
        r'facebook\.com/([^/?]+)',
        r'fb\.com/([^/?]+)',
        r'fb\.me/([^/?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def get_facebook_data(username):
    """Get real Facebook data using various OSINT techniques"""
    loading_animation("Collecting Facebook data", 3)
    
    data = {
        'username': username,
        'profile_url': f"https://facebook.com/{username}",
        'name': None,
        'about': None,
        'location': None,
        'joined_date': None,
        'friends_count': None
    }
    
    try:
        # Try to get data from various sources
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract name
            title_tag = soup.find('title')
            if title_tag:
                title_text = title_tag.text
                if '| Facebook' in title_text:
                    data['name'] = title_text.split('|')[0].strip()
            
            # Try to extract about section
            about_div = soup.find('div', string=re.compile('About', re.IGNORECASE))
            if about_div:
                about_text = about_div.find_next('div')
                if about_text:
                    data['about'] = about_text.text.strip()
            
            # Try to extract location
            location_pattern = re.compile(r'lives in|from|located in', re.IGNORECASE)
            location_elem = soup.find(string=location_pattern)
            if location_elem:
                data['location'] = location_elem.parent.text.strip() if location_elem.parent else None
            
            # Try to extract joined date
            joined_pattern = re.compile(r'joined|member since', re.IGNORECASE)
            joined_elem = soup.find(string=joined_pattern)
            if joined_elem:
                data['joined_date'] = joined_elem.find_next('span').text.strip() if joined_elem.find_next('span') else None
            
            # Try to extract friends count
            friends_pattern = re.compile(r'friends|أصدقاء', re.IGNORECASE)
            friends_elem = soup.find(string=friends_pattern)
            if friends_elem:
                friends_text = friends_elem.parent.text if friends_elem.parent else ''
                friends_match = re.search(r'(\d+[,.]?\d*)', friends_text)
                if friends_match:
                    data['friends_count'] = friends_match.group(1)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO facebook_data 
                    (username, name, profile_url, about, location, joined_date, friends_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['name'], data['profile_url'], 
                     data['about'], data['location'], data['joined_date'], data['friends_count']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Facebook data collected successfully!")
        print_info("Username", data['username'])
        print_info("Profile URL", data['profile_url'])
        print_info("Name", data['name'] or "Not found")
        print_info("About", data['about'] or "Not found")
        print_info("Location", data['location'] or "Not found")
        print_info("Joined Date", data['joined_date'] or "Not found")
        print_info("Friends Count", data['friends_count'] or "Not found")
        
    except Exception as e:
        print_error(f"Error collecting Facebook data: {str(e)}")

def view_facebook_data():
    conn = setup_database()
    c = conn.cursor()
    c.execute("SELECT * FROM facebook_data ORDER BY extracted_at DESC")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print_warning("No Facebook data found in database")
        return
    
    print_header("SAVED FACEBOOK DATA")
    for row in rows:
        print_info("ID", row[0])
        print_info("Username", row[1])
        print_info("Name", row[2] or "Not available")
        print_info("Profile URL", row[3])
        print_info("About", row[4] or "Not available")
        print_info("Location", row[5] or "Not available")
        print_info("Joined Date", row[6] or "Not available")
        print_info("Friends Count", row[7] or "Not available")
        print_info("Extracted At", row[8])
        print("-" * 50)

# ==================== INSTAGRAM MODULE ====================
def instagram_module():
    print_header("INSTAGRAM INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Extract information from profile URL")
    print("2. Search by username")
    print("3. View saved Instagram data")
    print("4. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        url = input(f"{Colors.YELLOW}Enter Instagram profile URL: {Colors.RESET}")
        username = extract_instagram_username(url)
        if username:
            print_info("Extracted username", username)
            get_instagram_data(username)
        else:
            print_error("Could not extract username from URL")
    
    elif choice == "2":
        username = input(f"{Colors.YELLOW}Enter Instagram username: {Colors.RESET}")
        get_instagram_data(username)
    
    elif choice == "3":
        view_instagram_data()
    
    elif choice == "4":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    instagram_module()

def extract_instagram_username(url):
    patterns = [
        r'instagram\.com/([^/?]+)',
        r'instagr\.am/([^/?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def get_instagram_data(username):
    """Get real Instagram data using various techniques"""
    loading_animation("Collecting Instagram data", 3)
    
    data = {
        'username': username,
        'profile_url': f"https://instagram.com/{username}",
        'full_name': None,
        'bio': None,
        'followers_count': None,
        'following_count': None,
        'posts_count': None,
        'is_private': None,
        'is_verified': None,
        'profile_pic_url': None
    }
    
    try:
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract data from meta tags
            title_tag = soup.find('title')
            if title_tag and title_tag.text:
                title_parts = title_tag.text.split('(')
                if len(title_parts) > 0:
                    data['full_name'] = title_parts[0].strip()
            
            # Try to extract bio
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc and meta_desc.get('content'):
                content = meta_desc['content']
                data['bio'] = content.split('-')[0].strip() if '-' in content else content
            
            # Try to extract counts
            meta_counters = soup.find_all('meta', property=lambda x: x and 'count' in x.lower())
            for meta in meta_counters:
                prop_name = meta.get('property', '').lower()
                content = meta.get('content', '')
                
                if 'follower' in prop_name:
                    data['followers_count'] = content
                elif 'following' in prop_name:
                    data['following_count'] = content
                elif 'post' in prop_name:
                    data['posts_count'] = content
            
            # Check if private
            private_text = soup.find(string=re.compile(r'private', re.IGNORECASE))
            data['is_private'] = "Yes" if private_text else "No"
            
            # Check if verified
            verified_elem = soup.find('span', text=re.compile(r'verified', re.IGNORECASE))
            data['is_verified'] = "Yes" if verified_elem else "No"
            
            # Try to extract profile picture
            meta_image = soup.find('meta', property='og:image')
            if meta_image and meta_image.get('content'):
                data['profile_pic_url'] = meta_image['content']
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO instagram_data 
                    (username, full_name, bio, followers_count, following_count, 
                     posts_count, is_private, is_verified, profile_pic_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['full_name'], data['bio'], 
                     data['followers_count'], data['following_count'], data['posts_count'],
                     data['is_private'], data['is_verified'], data['profile_pic_url']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Instagram data collected successfully!")
        print_info("Username", data['username'])
        print_info("Profile URL", data['profile_url'])
        print_info("Full Name", data['full_name'] or "Not found")
        print_info("Bio", data['bio'] or "Not found")
        print_info("Followers", data['followers_count'] or "Not found")
        print_info("Following", data['following_count'] or "Not found")
        print_info("Posts", data['posts_count'] or "Not found")
        print_info("Private", data['is_private'] or "Not found")
        print_info("Verified", data['is_verified'] or "Not found")
        print_info("Profile Picture", data['profile_pic_url'] or "Not found")
        
    except Exception as e:
        print_error(f"Error collecting Instagram data: {str(e)}")

def view_instagram_data():
    conn = setup_database()
    c = conn.cursor()
    c.execute("SELECT * FROM instagram_data ORDER BY extracted_at DESC")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print_warning("No Instagram data found in database")
        return
    
    print_header("SAVED INSTAGRAM DATA")
    for row in rows:
        print_info("ID", row[0])
        print_info("Username", row[1])
        print_info("Full Name", row[2] or "Not available")
        print_info("Bio", row[3] or "Not available")
        print_info("Followers", row[4] or "Not available")
        print_info("Following", row[5] or "Not available")
        print_info("Posts", row[6] or "Not available")
        print_info("Private", row[7] or "Not available")
        print_info("Verified", row[8] or "Not available")
        print_info("Profile Pic URL", row[9] or "Not available")
        print_info("Extracted At", row[10])
        print("-" * 50)

# ==================== TIKTOK MODULE ====================
def tiktok_module():
    print_header("TIKTOK INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Extract information from profile URL")
    print("2. Search by username")
    print("3. View saved TikTok data")
    print("4. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        url = input(f"{Colors.YELLOW}Enter TikTok profile URL: {Colors.RESET}")
        username = extract_tiktok_username(url)
        if username:
            print_info("Extracted username", username)
            get_tiktok_data(username)
        else:
            print_error("Could not extract username from URL")
    
    elif choice == "2":
        username = input(f"{Colors.YELLOW}Enter TikTok username: {Colors.RESET}")
        get_tiktok_data(username)
    
    elif choice == "3":
        view_tiktok_data()
    
    elif choice == "4":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    tiktok_module()

def extract_tiktok_username(url):
    patterns = [
        r'tiktok\.com/@([^/?]+)',
        r'tiktok\.com/([^/?]+)',
        r'vm\.tiktok\.com/[^/]+/([^/?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def get_tiktok_data(username):
    """Get real TikTok data using various techniques"""
    loading_animation("Collecting TikTok data", 3)
    
    data = {
        'username': username,
        'profile_url': f"https://tiktok.com/@{username}",
        'nickname': None,
        'signature': None,
        'followers_count': None,
        'following_count': None,
        'likes_count': None,
        'videos_count': None,
        'verified': None
    }
    
    try:
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract nickname
            title_tag = soup.find('title')
            if title_tag and title_tag.text:
                if '| TikTok' in title_tag.text:
                    data['nickname'] = title_tag.text.split('|')[0].strip()
            
            # Try to extract signature (bio)
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc and meta_desc.get('content'):
                data['signature'] = meta_desc['content']
            
            # Try to extract counts from JSON-LD
            json_ld = soup.find('script', type='application/ld+json')
            if json_ld:
                try:
                    json_data = json.loads(json_ld.string)
                    if 'interactionStatistic' in json_data:
                        for stat in json_data['interactionStatistic']:
                            if 'UserFollowers' in stat.get('interactionType', ''):
                                data['followers_count'] = stat.get('userInteractionCount')
                            elif 'UserFollows' in stat.get('interactionType', ''):
                                data['following_count'] = stat.get('userInteractionCount')
                except:
                    pass
            
            # Check if verified
            verified_elem = soup.find('svg', {'data-e2e': 'verified-icon'})
            data['verified'] = "Yes" if verified_elem else "No"
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO tiktok_data 
                    (username, nickname, signature, followers_count, following_count, 
                     likes_count, videos_count, verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['nickname'], data['signature'], 
                     data['followers_count'], data['following_count'], data['likes_count'],
                     data['videos_count'], data['verified']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("TikTok data collected successfully!")
        print_info("Username", data['username'])
        print_info("Profile URL", data['profile_url'])
        print_info("Nickname", data['nickname'] or "Not found")
        print_info("Signature", data['signature'] or "Not found")
        print_info("Followers", data['followers_count'] or "Not found")
        print_info("Following", data['following_count'] or "Not found")
        print_info("Likes", data['likes_count'] or "Not found")
        print_info("Videos", data['videos_count'] or "Not found")
        print_info("Verified", data['verified'] or "Not found")
        
    except Exception as e:
        print_error(f"Error collecting TikTok data: {str(e)}")

def view_tiktok_data():
    conn = setup_database()
    c = conn.cursor()
    c.execute("SELECT * FROM tiktok_data ORDER BY extracted_at DESC")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print_warning("No TikTok data found in database")
        return
    
    print_header("SAVED TIKTOK DATA")
    for row in rows:
        print_info("ID", row[0])
        print_info("Username", row[1])
        print_info("Nickname", row[2] or "Not available")
        print_info("Signature", row[3] or "Not available")
        print_info("Followers", row[4] or "Not available")
        print_info("Following", row[5] or "Not available")
        print_info("Likes", row[6] or "Not available")
        print_info("Videos", row[7] or "Not available")
        print_info("Verified", row[8] or "Not available")
        print_info("Extracted At", row[9])
        print("-" * 50)

# ==================== WEBSITE MODULE ====================
def website_module():
    print_header("WEBSITE INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Analyze website")
    print("2. View saved website data")
    print("3. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        url = input(f"{Colors.YELLOW}Enter website URL: {Colors.RESET}")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        get_website_info(url)
    
    elif choice == "2":
        view_website_data()
    
    elif choice == "3":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    website_module()

def get_website_info(url):
    """Get comprehensive website information"""
    loading_animation("Analyzing website", 5)
    
    data = {
        'url': url,
        'title': None,
        'ip_address': None,
        'server': None,
        'technologies': None,
        'whois_data': None,
        'dns_records': None
    }
    
    try:
        # Get website content
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                data['title'] = title_tag.text.strip()
            
            # Extract server information
            if 'server' in response.headers:
                data['server'] = response.headers['server']
            
            # Detect technologies
            data['technologies'] = detect_technologies(response.text, response.headers)
        
        # Get IP address
        try:
            domain = urlparse(url).netloc
            data['ip_address'] = socket.gethostbyname(domain)
        except:
            data['ip_address'] = "Could not resolve"
        
        # Get WHOIS data
        try:
            domain = urlparse(url).netloc
            whois_info = whois.whois(domain)
            data['whois_data'] = json.dumps(whois_info, default=str)
        except:
            data['whois_data'] = "Could not retrieve WHOIS data"
        
        # Get DNS records
        try:
            domain = urlparse(url).netloc
            dns_records = {}
            
            # A records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                dns_records['A'] = [str(record) for record in a_records]
            except:
                dns_records['A'] = []
            
            # MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                dns_records['MX'] = [str(record) for record in mx_records]
            except:
                dns_records['MX'] = []
            
            # NS records
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                dns_records['NS'] = [str(record) for record in ns_records]
            except:
                dns_records['NS'] = []
            
            data['dns_records'] = json.dumps(dns_records)
        except:
            data['dns_records'] = "Could not retrieve DNS records"
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO website_data 
                    (url, title, ip_address, server, technologies, whois_data, dns_records)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (data['url'], data['title'], data['ip_address'], data['server'],
                     data['technologies'], data['whois_data'], data['dns_records']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Website analysis completed successfully!")
        print_info("URL", data['url'])
        print_info("Title", data['title'] or "Not found")
        print_info("IP Address", data['ip_address'] or "Not found")
        print_info("Server", data['server'] or "Not found")
        
        if data['technologies']:
            print_info("Technologies", ", ".join(data['technologies']))
        else:
            print_info("Technologies", "Not detected")
        
        # Show partial WHOIS data
        if data['whois_data'] and data['whois_data'] != "Could not retrieve WHOIS data":
            try:
                whois_info = json.loads(data['whois_data'])
                if 'creation_date' in whois_info:
                    print_info("Creation Date", str(whois_info['creation_date']))
                if 'expiration_date' in whois_info:
                    print_info("Expiration Date", str(whois_info['expiration_date']))
                if 'registrar' in whois_info:
                    print_info("Registrar", str(whois_info['registrar']))
            except:
                print_info("WHOIS Data", "Available (view in database)")
        
        # Show DNS records
        if data['dns_records'] and data['dns_records'] != "Could not retrieve DNS records":
            try:
                dns_info = json.loads(data['dns_records'])
                if dns_info.get('A'):
                    print_info("A Records", ", ".join(dns_info['A']))
            except:
                print_info("DNS Records", "Available (view in database)")
        
    except Exception as e:
        print_error(f"Error analyzing website: {str(e)}")

def detect_technologies(html_content, headers):
    """Detect web technologies used by the website"""
    technologies = []
    
    # Check for common frameworks
    if re.search(r'react|react-dom', html_content, re.IGNORECASE):
        technologies.append("React")
    
    if re.search(r'angular|ng-', html_content, re.IGNORECASE):
        technologies.append("Angular")
    
    if re.search(r'vue\.js|v-bind|v-model', html_content, re.IGNORECASE):
        technologies.append("Vue.js")
    
    if re.search(r'jquery', html_content, re.IGNORECASE):
        technologies.append("jQuery")
    
    # Check for CMS
    if re.search(r'wp-content|wp-includes|wordpress', html_content, re.IGNORECASE):
        technologies.append("WordPress")
    
    if re.search(r'joomla', html_content, re.IGNORECASE):
        technologies.append("Joomla")
    
    if re.search(r'drupal', html_content, re.IGNORECASE):
        technologies.append("Drupal")
    
    # Check for server technologies
    if 'x-powered-by' in headers:
        technologies.append(headers['x-powered-by'])
    
    if 'server' in headers:
        technologies.append(headers['server'])
    
    # Check for analytics
    if re.search(r'google-analytics|ga\.js', html_content, re.IGNORECASE):
        technologies.append("Google Analytics")
    
    if re.search(r'gtm\.js|googletagmanager', html_content, re.IGNORECASE):
        technologies.append("Google Tag Manager")
    
    return technologies

def view_website_data():
    conn = setup_database()
    c = conn.cursor()
    c.execute("SELECT * FROM website_data ORDER BY extracted_at DESC")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print_warning("No website data found in database")
        return
    
    print_header("SAVED WEBSITE DATA")
    for row in rows:
        print_info("ID", row[0])
        print_info("URL", row[1])
        print_info("Title", row[2] or "Not available")
        print_info("IP Address", row[3] or "Not available")
        print_info("Server", row[4] or "Not available")
        
        if row[5]:
            try:
                tech_list = json.loads(row[5])
                print_info("Technologies", ", ".join(tech_list))
            except:
                print_info("Technologies", row[5])
        else:
            print_info("Technologies", "Not available")
        
        print_info("Extracted At", row[8])
        print("-" * 50)

# ==================== SNAPCHAT MODULE ====================
def snapchat_module():
    print_header("SNAPCHAT INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Search by username")
    print("2. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        username = input(f"{Colors.YELLOW}Enter Snapchat username: {Colors.RESET}")
        get_snapchat_data(username)
    
    elif choice == "2":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    snapchat_module()

def get_snapchat_data(username):
    """Get limited Snapchat data (Snapchat has strict privacy policies)"""
    loading_animation("Checking Snapchat username", 2)
    
    data = {
        'username': username,
        'profile_url': f"https://snapchat.com/add/{username}",
        'exists': None,
        'display_name': None
    }
    
    try:
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if profile exists
            error_msg = soup.find(string=re.compile(r'couldn\'t find|doesn\'t exist', re.IGNORECASE))
            data['exists'] = "No" if error_msg else "Yes"
            
            # Try to extract display name
            title_tag = soup.find('title')
            if title_tag and title_tag.text:
                if 'on Snapchat' in title_tag.text:
                    data['display_name'] = title_tag.text.split('on Snapchat')[0].strip()
        
        # Display results
        print_success("Snapchat data collected!")
        print_info("Username", data['username'])
        print_info("Profile URL", data['profile_url'])
        print_info("Exists", data['exists'] or "Unknown")
        print_info("Display Name", data['display_name'] or "Not found")
        
    except Exception as e:
        print_error(f"Error checking Snapchat: {str(e)}")

# ==================== PASSWORD GUESSING MODULE ====================
def password_module():
    print_header("PASSWORD PATTERN GENERATOR")
    print(f"{Colors.WHITE}1. Generate password patterns for username")
    print("2. View saved password patterns")
    print("3. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        username = input(f"{Colors.YELLOW}Enter username: {Colors.RESET}")
        platform = input(f"{Colors.YELLOW}Enter platform (e.g., facebook, instagram): {Colors.RESET}")
        guess_common_passwords(username, platform)
    
    elif choice == "2":
        view_password_patterns()
    
    elif choice == "3":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    password_module()

def guess_common_passwords(username, platform):
    """Generate common password patterns based on username and platform FOR EDUCATIONAL PURPOSES ONLY"""
    loading_animation("Generating password patterns", 2)
    
    patterns = []
    
    # Common number patterns
    number_patterns = [
        '', '123', '1234', '12345', '123456', 
        '1', '12', '1234567', '12345678', '123456789',
        '00', '000', '0000', '00000', '000000',
        '01', '02', '03', '04', '05',
        '10', '11', '12', '13', '14', '15',
        '69', '77', '88', '99', '100', '200', '300'
    ]
    
    # Special character patterns
    special_patterns = [
        '', '!', '@', '#', '$', '%', '^', '&', '*',
        '!@', '!@#', '!@#$', '@!', '#!', '$!',
        '!!', '!!!', '!!!!'
    ]
    
    # Year patterns
    current_year = datetime.now().year
    year_patterns = [
        str(current_year), str(current_year - 1), str(current_year - 2),
        str(current_year)[2:], str(current_year - 1)[2:], str(current_year - 2)[2:],
        '1990', '1991', '1992', '1993', '1994', '1995', 
        '1996', '1997', '1998', '1999', '2000', '2001',
        '2002', '2003', '2004', '2005', '2006', '2007',
        '2008', '2009', '2010', '2011', '2012', '2013',
        '2014', '2015', '2016', '2017', '2018', '2019',
        '2020', '2021', '2022', '2023', '2024'
    ]
    
    # Platform-specific patterns
    platform_patterns = {
        'facebook': ['fb', 'face', 'facebook', 'fbpass', 'fbpw'],
        'instagram': ['ig', 'insta', 'instagram', 'igpass', 'igpw'],
        'twitter': ['tw', 'tweet', 'twitter', 'twpass', 'twpw'],
        'tiktok': ['tt', 'tiktok', 'tik', 'tok', 'ttpass', 'ttpw'],
        'snapchat': ['sc', 'snap', 'snapchat', 'scpass', 'scpw']
    }
    
    # Generate patterns
    for num in number_patterns:
        for spec in special_patterns:
            for year in year_patterns:
                # Basic patterns
                patterns.append(f"{username}{num}{spec}")
                patterns.append(f"{username}{spec}{num}")
                patterns.append(f"{spec}{username}{num}")
                patterns.append(f"{num}{username}{spec}")
                
                # With year
                patterns.append(f"{username}{year}{spec}")
                patterns.append(f"{username}{spec}{year}")
                patterns.append(f"{year}{username}{spec}")
                patterns.append(f"{spec}{username}{year}")
                
                # Platform-specific patterns
                if platform.lower() in platform_patterns:
                    for plat in platform_patterns[platform.lower()]:
                        patterns.append(f"{username}{plat}{num}{spec}")
                        patterns.append(f"{plat}{username}{num}{spec}")
                        patterns.append(f"{username}{num}{plat}{spec}")
                        patterns.append(f"{plat}{num}{username}{spec}")
    
    # Remove duplicates and limit to 1000 patterns
    patterns = list(set(patterns))[:1000]
    
    # Save to database
    conn = setup_database()
    c = conn.cursor()
    
    for pattern in patterns:
        c.execute('''INSERT INTO password_patterns 
                    (username, platform, pattern)
                    VALUES (?, ?, ?)''',
                    (username, platform, pattern))
    
    conn.commit()
    conn.close()
    
    # Display results
    print_success(f"Generated {len(patterns)} password patterns!")
    print_info("Username", username)
    print_info("Platform", platform)
    print(f"\n{Colors.YELLOW}Sample patterns:{Colors.RESET}")
    
    for i, pattern in enumerate(patterns[:10]):
        print_bullet(pattern)
    
    if len(patterns) > 10:
        print_info("And more", f"{len(patterns) - 10} additional patterns...")
    
    print_warning("FOR EDUCATIONAL PURPOSES ONLY - Use responsibly!")

def view_password_patterns():
    conn = setup_database()
    c = conn.cursor()
    c.execute("SELECT * FROM password_patterns ORDER BY generated_at DESC")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print_warning("No password patterns found in database")
        return
    
    print_header("SAVED PASSWORD PATTERNS")
    for row in rows:
        print_info("ID", row[0])
        print_info("Username", row[1])
        print_info("Platform", row[2])
        print_info("Pattern", row[3])
        print_info("Generated At", row[4])
        print("-" * 50)

# ==================== DATABASE VIEW MODULE ====================
def view_database():
    print_header("DATABASE VIEWER")
    print(f"{Colors.WHITE}1. View Facebook data")
    print("2. View Instagram data")
    print("3. View TikTok data")
    print("4. View website data")
    print("5. View password patterns")
    print("6. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        view_facebook_data()
    elif choice == "2":
        view_instagram_data()
    elif choice == "3":
        view_tiktok_data()
    elif choice == "4":
        view_website_data()
    elif choice == "5":
        view_password_patterns()
    elif choice == "6":
        return
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    view_database()

# ==================== EXPORT DATA MODULE ====================
def export_data():
    print_header("DATA EXPORT")
    print(f"{Colors.WHITE}1. Export Facebook data")
    print("2. Export Instagram data")
    print("3. Export TikTok data")
    print("4. Export website data")
    print("5. Export password patterns")
    print("6. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    conn = setup_database()
    c = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if choice == "1":
        export_table(c, "facebook_data", "Facebook", timestamp)
    elif choice == "2":
        export_table(c, "instagram_data", "Instagram", timestamp)
    elif choice == "3":
        export_table(c, "tiktok_data", "TikTok", timestamp)
    elif choice == "4":
        export_table(c, "website_data", "Website", timestamp)
    elif choice == "5":
        export_table(c, "password_patterns", "Password_Patterns", timestamp)
    elif choice == "6":
        conn.close()
        return
    else:
        print_error("Invalid option")
        conn.close()
        return
    
    conn.close()
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    export_data()

def export_table(cursor, table_name, format_type, timestamp):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    if not rows:
        print_warning(f"No data found in {table_name}")
        return
    
    # Create exports directory if it doesn't exist
    if not os.path.exists("exports"):
        os.makedirs("exports")
    
    filename = f"exports/{table_name}_{timestamp}"
    
    # Export to CSV
    csv_filename = f"{filename}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerows(rows)
    
    # Export to JSON
    json_filename = f"{filename}.json"
    data = []
    for row in rows:
        data.append(dict(zip(column_names, row)))
    
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4, default=str)
    
    print_success(f"Exported {len(rows)} records from {table_name}")
    print_info("CSV file", csv_filename)
    print_info("JSON file", json_filename)

# ==================== MAIN MENU ====================
def main_menu():
    conn = setup_database()  # Initialize database
    conn.close()
    
    while True:
        mobile_banner()
        print(f"\n{Colors.WHITE}{Colors.BOLD}MAIN MENU{Colors.RESET}")
        print(f"{Colors.WHITE}1. Facebook Intelligence")
        print("2. Instagram Intelligence")
        print("3. TikTok Intelligence")
        print("4. Website Intelligence")
        print("5. Snapchat Intelligence")
        print("6. Password Pattern Generator")
        print("7. Database Viewer")
        print("8. Export Data")
        print("9. Exit{Colors.RESET}")
        
        choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
        
        if choice == "1":
            facebook_module()
        elif choice == "2":
            instagram_module()
        elif choice == "3":
            tiktok_module()
        elif choice == "4":
            website_module()
        elif choice == "5":
            snapchat_module()
        elif choice == "6":
            password_module()
        elif choice == "7":
            view_database()
        elif choice == "8":
            export_data()
        elif choice == "9":
            print(f"\n{Colors.GREEN}Thank you for using Omar-tool Professional v4.0!{Colors.RESET}")
            print(f"{Colors.CYAN}Visit: https://omarmetman.vercel.app{Colors.RESET}")
            break
        else:
            print_error("Invalid option")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Tool terminated by user{Colors.RESET}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")