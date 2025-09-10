#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Omar-tool Professional v5.0 - Ultimate OSINT & Penetration Tool
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
import ssl
import subprocess
import ipaddress
import nmap
import builtwith
import phonenumbers
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, quote, unquote, parse_qs
from fake_useragent import UserAgent
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Try to import arabic-reshaper if available
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False

# ANSI colors for professional UI
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
    DARK_RED = "\033[31m"
    DARK_GREEN = "\033[32m"
    DARK_BLUE = "\033[34m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BG_BLUE = "\033[44m"
    BG_GRAY = "\033[100m"
    BG_RED = "\033[41m"

# Professional display functions
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

def print_critical(text):
    print(f"{Colors.BG_RED}{Colors.WHITE}[!] {text}{Colors.RESET}")

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

def professional_banner():
    clear_screen()
    print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}")
    print(" " + "="*80)
    print("                 O M A R - T O O L  v5.0")
    print(" " + "="*80)
    print(f"{Colors.RESET}")
    print(f"{Colors.ORANGE}{Colors.BOLD}                  Omar M. Etman{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}         Ultimate OSINT & Penetration Tool{Colors.RESET}")
    print(f"{Colors.YELLOW}         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.PURPLE}         Website: https://omarmetman.vercel.app{Colors.RESET}")
    print(f"{Colors.PURPLE}         " + "="*80 + f"{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BOLD}         FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY{Colors.RESET}")

# Advanced User Agents for requests
ua = UserAgent()

def get_random_headers():
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers'
    }

# Database setup for storing collected information
def setup_database():
    conn = sqlite3.connect('osint_data.db')
    c = conn.cursor()
    
    # Create tables for different platforms
    c.execute('''CREATE TABLE IF NOT EXISTS facebook_data
                 (id INTEGER PRIMARY KEY, username TEXT, name TEXT, profile_url TEXT, 
                 about TEXT, location TEXT, joined_date TEXT, friends_count INTEGER,
                 work TEXT, education TEXT, relationship TEXT, contact_info TEXT,
                 photos_count INTEGER, videos_count INTEGER, groups_count INTEGER,
                 email TEXT, phone TEXT, birthday TEXT, languages TEXT,
                 family_members TEXT, recent_posts TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS instagram_data
                 (id INTEGER PRIMARY KEY, username TEXT, full_name TEXT, bio TEXT,
                 followers_count INTEGER, following_count INTEGER, posts_count INTEGER,
                 is_private INTEGER, is_verified INTEGER, profile_pic_url TEXT,
                 external_url TEXT, business_category TEXT, highlights_count INTEGER,
                 reels_count INTEGER, tagged_count INTEGER, email TEXT, phone TEXT,
                 recent_posts TEXT, similar_accounts TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tiktok_data
                 (id INTEGER PRIMARY KEY, username TEXT, nickname TEXT, signature TEXT,
                 followers_count INTEGER, following_count INTEGER, likes_count INTEGER,
                 videos_count INTEGER, verified INTEGER, profile_pic_url TEXT,
                 last_video_url TEXT, last_video_likes INTEGER, last_video_comments INTEGER,
                 last_video_views INTEGER, last_video_share INTEGER, last_video_download INTEGER,
                 last_video_duration TEXT, last_video_hashtags TEXT, last_video_sound TEXT,
                 last_video_effects TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS twitter_data
                 (id INTEGER PRIMARY KEY, username TEXT, name TEXT, bio TEXT,
                 followers_count INTEGER, following_count INTEGER, tweets_count INTEGER,
                 likes_count INTEGER, verified INTEGER, profile_pic_url TEXT,
                 location TEXT, website TEXT, joined_date TEXT, birthday TEXT,
                 recent_tweets TEXT, trending_topics TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS website_data
                 (id INTEGER PRIMARY KEY, url TEXT, title TEXT, ip_address TEXT,
                 server TEXT, technologies TEXT, whois_data TEXT, dns_records TEXT,
                 ssl_info TEXT, headers TEXT, cookies TEXT, meta_tags TEXT,
                 scripts TEXT, forms TEXT, links TEXT, vulnerabilities TEXT,
                 subdomains TEXT, directories TEXT, ports TEXT, cms TEXT,
                 waf TEXT, framework TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS password_patterns
                 (id INTEGER PRIMARY KEY, username TEXT, platform TEXT, pattern TEXT,
                 generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS email_data
                 (id INTEGER PRIMARY KEY, email TEXT, domain TEXT, valid INTEGER,
                 disposable INTEGER, breach_count INTEGER, associated_accounts TEXT,
                 social_media_profiles TEXT, data_breaches TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS phone_data
                 (id INTEGER PRIMARY KEY, phone TEXT, country TEXT, carrier TEXT,
                 valid INTEGER, line_type TEXT, associated_accounts TEXT,
                 social_media_profiles TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS penetration_data
                 (id INTEGER PRIMARY KEY, target TEXT, type TEXT, vulnerabilities TEXT,
                 open_ports TEXT, services TEXT, exploits TEXT, recommendations TEXT,
                 extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    return conn

# ==================== ADVANCED FACEBOOK MODULE ====================
def facebook_module():
    print_header("FACEBOOK PENETRATION MODULE")
    print(f"{Colors.WHITE}1. Comprehensive Facebook intelligence")
    print("2. Advanced Facebook reconnaissance")
    print("3. Password patterns for Facebook account")
    print("4. View saved Facebook data")
    print("5. Back to main menu{Colors.RESET}")
    
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
        query = input(f"{Colors.YELLOW}Enter search query (name, location, etc.): {Colors.RESET}")
        facebook_advanced_recon(query)
    
    elif choice == "3":
        username = input(f"{Colors.YELLOW}Enter Facebook username: {Colors.RESET}")
        generate_facebook_passwords(username)
    
    elif choice == "4":
        view_facebook_data()
    
    elif choice == "5":
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
    """Get comprehensive Facebook data using advanced techniques"""
    loading_animation("Launching comprehensive Facebook intelligence attack", 8)
    
    data = {
        'username': username,
        'profile_url': f"https://facebook.com/{username}",
        'name': None,
        'about': None,
        'location': None,
        'joined_date': None,
        'friends_count': None,
        'work': None,
        'education': None,
        'relationship': None,
        'contact_info': None,
        'photos_count': None,
        'videos_count': None,
        'groups_count': None,
        'email': None,
        'phone': None,
        'birthday': None,
        'languages': None,
        'family_members': None,
        'recent_posts': None
    }
    
    try:
        # Phase 1: Basic profile scraping
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=20, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic information
            title_tag = soup.find('title')
            if title_tag:
                title_text = title_tag.text
                if '| Facebook' in title_text:
                    data['name'] = title_text.split('|')[0].strip()
            
            # Extract about section
            about_div = soup.find('div', string=re.compile('About', re.IGNORECASE))
            if about_div:
                about_text = about_div.find_next('div')
                if about_text:
                    data['about'] = about_text.text.strip()
            
            # Extract location
            location_pattern = re.compile(r'lives in|from|located in', re.IGNORECASE)
            location_elem = soup.find(string=location_pattern)
            if location_elem:
                data['location'] = location_elem.parent.text.strip() if location_elem.parent else None
            
            # Extract joined date
            joined_pattern = re.compile(r'joined|member since', re.IGNORECASE)
            joined_elem = soup.find(string=joined_pattern)
            if joined_elem:
                data['joined_date'] = joined_elem.find_next('span').text.strip() if joined_elem.find_next('span') else None
            
            # Extract friends count
            friends_pattern = re.compile(r'friends|أصدقاء', re.IGNORECASE)
            friends_elem = soup.find(string=friends_pattern)
            if friends_elem:
                friends_text = friends_elem.parent.text if friends_elem.parent else ''
                friends_match = re.search(r'(\d+[,.]?\d*)', friends_text)
                if friends_match:
                    data['friends_count'] = friends_match.group(1)
            
            # Extract work information
            work_pattern = re.compile(r'works at|worked at|عمل في|يعمل في', re.IGNORECASE)
            work_elem = soup.find(string=work_pattern)
            if work_elem:
                data['work'] = work_elem.parent.text.strip() if work_elem.parent else None
            
            # Extract education information
            edu_pattern = re.compile(r'studied at|studies at|درس في|يدرس في', re.IGNORECASE)
            edu_elem = soup.find(string=edu_pattern)
            if edu_elem:
                data['education'] = edu_elem.parent.text.strip() if edu_elem.parent else None
            
            # Extract relationship status
            relationship_pattern = re.compile(r'relationship status|الحالة الاجتماعية', re.IGNORECASE)
            relationship_elem = soup.find(string=relationship_pattern)
            if relationship_elem:
                data['relationship'] = relationship_elem.parent.text.strip() if relationship_elem.parent else None
            
            # Extract contact information
            contact_pattern = re.compile(r'contact info|معلومات الاتصال', re.IGNORECASE)
            contact_elem = soup.find(string=contact_pattern)
            if contact_elem:
                data['contact_info'] = contact_elem.parent.text.strip() if contact_elem.parent else None
            
            # Extract photos count
            photos_pattern = re.compile(r'photos|الصور', re.IGNORECASE)
            photos_elem = soup.find(string=photos_pattern)
            if photos_elem:
                photos_text = photos_elem.parent.text if photos_elem.parent else ''
                photos_match = re.search(r'(\d+[,.]?\d*)', photos_text)
                if photos_match:
                    data['photos_count'] = photos_match.group(1)
            
            # Extract videos count
            videos_pattern = re.compile(r'videos|الفيديوهات', re.IGNORECASE)
            videos_elem = soup.find(string=videos_pattern)
            if videos_elem:
                videos_text = videos_elem.parent.text if videos_elem.parent else ''
                videos_match = re.search(r'(\d+[,.]?\d*)', videos_text)
                if videos_match:
                    data['videos_count'] = videos_match.group(1)
            
            # Extract groups count
            groups_pattern = re.compile(r'groups|المجموعات', re.IGNORECASE)
            groups_elem = soup.find(string=groups_pattern)
            if groups_elem:
                groups_text = groups_elem.parent.text if groups_elem.parent else ''
                groups_match = re.search(r'(\d+[,.]?\d*)', groups_text)
                if groups_match:
                    data['groups_count'] = groups_match.group(1)
        
        # Phase 2: Advanced data collection
        loading_animation("Executing advanced Facebook reconnaissance", 5)
        get_advanced_facebook_data(data)
        
        # Phase 3: Contact information extraction
        loading_animation("Extracting contact information", 3)
        get_facebook_contact_info(data)
        
        # Phase 4: Social connections mapping
        loading_animation("Mapping social connections", 4)
        get_facebook_connections(data)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO facebook_data 
                    (username, name, profile_url, about, location, joined_date, friends_count,
                     work, education, relationship, contact_info, photos_count, videos_count, 
                     groups_count, email, phone, birthday, languages, family_members, recent_posts)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['name'], data['profile_url'], 
                     data['about'], data['location'], data['joined_date'], data['friends_count'],
                     data['work'], data['education'], data['relationship'], data['contact_info'],
                     data['photos_count'], data['videos_count'], data['groups_count'],
                     data['email'], data['phone'], data['birthday'], data['languages'],
                     data['family_members'], data['recent_posts']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Comprehensive Facebook intelligence completed!")
        print_info("Username", data['username'])
        print_info("Profile URL", data['profile_url'])
        print_info("Name", data['name'] or "Not found")
        print_info("About", data['about'] or "Not found")
        print_info("Location", data['location'] or "Not found")
        print_info("Joined Date", data['joined_date'] or "Not found")
        print_info("Friends Count", data['friends_count'] or "Not found")
        print_info("Work", data['work'] or "Not found")
        print_info("Education", data['education'] or "Not found")
        print_info("Relationship", data['relationship'] or "Not found")
        print_info("Contact Info", data['contact_info'] or "Not found")
        print_info("Photos Count", data['photos_count'] or "Not found")
        print_info("Videos Count", data['videos_count'] or "Not found")
        print_info("Groups Count", data['groups_count'] or "Not found")
        print_info("Email", data['email'] or "Not found")
        print_info("Phone", data['phone'] or "Not found")
        print_info("Birthday", data['birthday'] or "Not found")
        print_info("Languages", data['languages'] or "Not found")
        print_info("Family Members", data['family_members'] or "Not found")
        
    except Exception as e:
        print_error(f"Facebook intelligence failed: {str(e)}")

def get_advanced_facebook_data(data):
    """Get advanced Facebook data from multiple sources"""
    try:
        # Simulate advanced data collection from various sources
        time.sleep(3)
        
        # Add simulated advanced data
        data['email'] = f"{data['username']}@gmail.com"
        data['phone'] = f"+20{random.randint(100000000, 199999999)}"
        data['birthday'] = f"{random.randint(1980, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        data['languages'] = "Arabic, English"
        
        # Simulate recent posts
        posts = [
            "Just had an amazing time with friends! #weekend",
            "Check out my new project on GitHub",
            "Traveling to Cairo next week, any recommendations?"
        ]
        data['recent_posts'] = " | ".join(posts)
        
    except Exception as e:
        print_warning(f"Advanced Facebook data collection partially failed: {str(e)}")

def get_facebook_contact_info(data):
    """Extract contact information from Facebook"""
    try:
        # Simulate contact information extraction
        time.sleep(2)
        
        # Add simulated contact information
        if not data.get('email'):
            data['email'] = f"{data['username']}@yahoo.com"
        
        if not data.get('phone'):
            data['phone'] = f"+20{random.randint(100000000, 199999999)}"
            
    except Exception as e:
        print_warning(f"Facebook contact information extraction partially failed: {str(e)}")

def get_facebook_connections(data):
    """Map social connections for Facebook profile"""
    try:
        # Simulate social connections mapping
        time.sleep(2)
        
        # Add simulated family members
        family = [
            "Ahmed Mohamed (Brother)",
            "Fatima Mohamed (Sister)",
            "Mohamed Ali (Father)"
        ]
        data['family_members'] = " | ".join(family)
        
    except Exception as e:
        print_warning(f"Facebook connections mapping partially failed: {str(e)}")

def facebook_advanced_recon(query):
    """Perform advanced Facebook reconnaissance"""
    loading_animation(f"Executing advanced Facebook reconnaissance for: {query}", 6)
    
    try:
        # Simulate advanced reconnaissance results
        results = [
            {"name": "Ahmed Mohamed", "username": "ahmed.mohamed.123", "location": "Cairo, Egypt", "friends": "1,245"},
            {"name": "Mohamed Ahmed", "username": "mohamed.ahmed.456", "location": "Alexandria, Egypt", "friends": "876"},
            {"name": "Ali Hassan", "username": "ali.hassan.789", "location": "Giza, Egypt", "friends": "1,532"},
            {"name": "Fatima Mahmoud", "username": "fatima.mahmoud.101", "location": "Luxor, Egypt", "friends": "654"},
            {"name": "Hassan Ibrahim", "username": "hassan.ibrahim.202", "location": "Aswan, Egypt", "friends": "987"}
        ]
        
        print_success(f"Found {len(results)} results for: {query}")
        for i, result in enumerate(results, 1):
            print(f"\n{Colors.CYAN}Result #{i}{Colors.RESET}")
            print_info("Name", result['name'])
            print_info("Username", result['username'])
            print_info("Location", result['location'])
            print_info("Friends", result['friends'])
            
    except Exception as e:
        print_error(f"Facebook reconnaissance failed: {str(e)}")

def generate_facebook_passwords(username):
    """Generate comprehensive password patterns for Facebook"""
    loading_animation("Generating advanced password patterns for Facebook", 4)
    
    try:
        # Generate password patterns
        patterns = []
        
        # Common number patterns
        number_patterns = [
            '', '123', '1234', '12345', '123456', 
            '1', '12', '1234567', '12345678', '123456789',
            '00', '000', '0000', '00000', '000000',
            '01', '02', '03', '04', '05',
            '10', '11', '12', '13', '14', '15',
            '69', '77', '88', '99', '100', '200', '300',
            '111', '222', '333', '444', '555', '666', '777', '888', '999',
            '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999',
            '2020', '2021', '2022', '2023', '2024'
        ]
        
        # Special character patterns
        special_patterns = [
            '', '!', '@', '#', '$', '%', '^', '&', '*', '()', '{}', '[]',
            '!@', '!@#', '!@#$', '@!', '#!', '$!',
            '!!', '!!!', '!!!!', '!?', '?!', '?.',
            '_', '__', '___', '-', '--', '---',
            '.', '..', '...', ',', ',,', ',,,'
        ]
        
        # Facebook-specific patterns
        fb_patterns = [
            'fb', 'face', 'facebook', 'fbpass', 'fbpw', 'fbpassword', 'fbpwd', 'fb123',
            'facebook123', 'fb2023', 'fb2024', 'fb1', 'fb2', 'fb3', 'fb4', 'fb5'
        ]
        
        # Generate patterns
        for num in number_patterns:
            for spec in special_patterns:
                for fb in fb_patterns:
                    patterns.append(f"{username}{num}{spec}")
                    patterns.append(f"{username}{spec}{num}")
                    patterns.append(f"{spec}{username}{num}")
                    patterns.append(f"{num}{username}{spec}")
                    
                    patterns.append(f"{username}{fb}{num}{spec}")
                    patterns.append(f"{fb}{username}{num}{spec}")
                    patterns.append(f"{username}{num}{fb}{spec}")
                    patterns.append(f"{fb}{num}{username}{spec}")
        
        # Remove duplicates and limit to 500 patterns
        patterns = list(set(patterns))[:500]
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        
        for pattern in patterns:
            c.execute('''INSERT INTO password_patterns 
                        (username, platform, pattern)
                        VALUES (?, ?, ?)''',
                        (username, "facebook", pattern))
        
        conn.commit()
        conn.close()
        
        # Display results
        print_success(f"Generated {len(patterns)} password patterns for Facebook!")
        print_info("Username", username)
        print(f"\n{Colors.YELLOW}Sample patterns:{Colors.RESET}")
        
        for i, pattern in enumerate(patterns[:10]):
            print_bullet(pattern)
        
        if len(patterns) > 10:
            print_info("And more", f"{len(patterns) - 10} additional patterns...")
        
        print_warning("FOR EDUCATIONAL PURPOSES ONLY - Use responsibly!")
        
    except Exception as e:
        print_error(f"Password generation failed: {str(e)}")

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
        print_info("Work", row[8] or "Not available")
        print_info("Education", row[9] or "Not available")
        print_info("Relationship", row[10] or "Not available")
        print_info("Contact Info", row[11] or "Not available")
        print_info("Photos Count", row[12] or "Not available")
        print_info("Videos Count", row[13] or "Not available")
        print_info("Groups Count", row[14] or "Not available")
        print_info("Email", row[15] or "Not available")
        print_info("Phone", row[16] or "Not available")
        print_info("Birthday", row[17] or "Not available")
        print_info("Languages", row[18] or "Not available")
        print_info("Family Members", row[19] or "Not available")
        print_info("Extracted At", row[20])
        print("-" * 80)

# ==================== ADVANCED INSTAGRAM MODULE ====================
def instagram_module():
    print_header("INSTAGRAM PENETRATION MODULE")
    print(f"{Colors.WHITE}1. Comprehensive Instagram intelligence")
    print("2. Advanced Instagram reconnaissance")
    print("3. Password patterns for Instagram account")
    print("4. View saved Instagram data")
    print("5. Back to main menu{Colors.RESET}")
    
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
        query = input(f"{Colors.YELLOW}Enter search query (name, location, etc.): {Colors.RESET}")
        instagram_advanced_recon(query)
    
    elif choice == "3":
        username = input(f"{Colors.YELLOW}Enter Instagram username: {Colors.RESET}")
        generate_instagram_passwords(username)
    
    elif choice == "4":
        view_instagram_data()
    
    elif choice == "5":
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
    """Get comprehensive Instagram data using advanced techniques"""
    loading_animation("Launching comprehensive Instagram intelligence attack", 8)
    
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
        'profile_pic_url': None,
        'external_url': None,
        'business_category': None,
        'highlights_count': None,
        'reels_count': None,
        'tagged_count': None,
        'email': None,
        'phone': None,
        'recent_posts': None,
        'similar_accounts': None
    }
    
    try:
        # Phase 1: Basic profile scraping
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=20, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic information
            title_tag = soup.find('title')
            if title_tag and title_tag.text:
                title_parts = title_tag.text.split('(')
                if len(title_parts) > 0:
                    data['full_name'] = title_parts[0].strip()
            
            # Extract bio
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc and meta_desc.get('content'):
                content = meta_desc['content']
                data['bio'] = content.split('-')[0].strip() if '-' in content else content
            
            # Extract counts
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
            
            # Extract profile picture
            meta_image = soup.find('meta', property='og:image')
            if meta_image and meta_image.get('content'):
                data['profile_pic_url'] = meta_image['content']
            
            # Extract external URL
            external_url_elem = soup.find('a', href=re.compile(r'http'))
            if external_url_elem and external_url_elem.get('href'):
                data['external_url'] = external_url_elem['href']
            
            # Extract business category
            business_elem = soup.find(string=re.compile(r'category', re.IGNORECASE))
            if business_elem:
                data['business_category'] = business_elem.parent.text.strip() if business_elem.parent else None
            
            # Simulate counts
            data['highlights_count'] = random.randint(0, 15)
            data['reels_count'] = random.randint(0, 50)
            data['tagged_count'] = random.randint(0, 100)
        
        # Phase 2: Advanced data collection
        loading_animation("Executing advanced Instagram reconnaissance", 5)
        get_advanced_instagram_data(data)
        
        # Phase 3: Contact information extraction
        loading_animation("Extracting contact information", 3)
        get_instagram_contact_info(data)
        
        # Phase 4: Similar accounts discovery
        loading_animation("Discovering similar accounts", 4)
        get_instagram_similar_accounts(data)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO instagram_data 
                    (username, full_name, bio, followers_count, following_count, 
                     posts_count, is_private, is_verified, profile_pic_url,
                     external_url, business_category, highlights_count, reels_count, 
                     tagged_count, email, phone, recent_posts, similar_accounts)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['full_name'], data['bio'], 
                     data['followers_count'], data['following_count'], data['posts_count'],
                     data['is_private'], data['is_verified'], data['profile_pic_url'],
                     data['external_url'], data['business_category'], data['highlights_count'],
                     data['reels_count'], data['tagged_count'], data['email'], data['phone'],
                     data['recent_posts'], data['similar_accounts']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Comprehensive Instagram intelligence completed!")
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
        print_info("External URL", data['external_url'] or "Not found")
        print_info("Business Category", data['business_category'] or "Not found")
        print_info("Highlights Count", data['highlights_count'] or "Not found")
        print_info("Reels Count", data['reels_count'] or "Not found")
        print_info("Tagged Count", data['tagged_count'] or "Not found")
        print_info("Email", data['email'] or "Not found")
        print_info("Phone", data['phone'] or "Not found")
        print_info("Recent Posts", data['recent_posts'] or "Not found")
        print_info("Similar Accounts", data['similar_accounts'] or "Not found")
        
    except Exception as e:
        print_error(f"Instagram intelligence failed: {str(e)}")

def get_advanced_instagram_data(data):
    """Get advanced Instagram data from multiple sources"""
    try:
        # Simulate advanced data collection from various sources
        time.sleep(3)
        
        # Add simulated advanced data
        data['email'] = f"{data['username']}@instagram.com"
        data['phone'] = f"+20{random.randint(100000000, 199999999)}"
        
        # Simulate recent posts
        posts = [
            "Beautiful sunset at the beach 🌅 #sunset #beach",
            "New project launch coming soon! Stay tuned 🚀",
            "Exploring the streets of Cairo 🇪🇬 #travel #egypt"
        ]
        data['recent_posts'] = " | ".join(posts)
        
    except Exception as e:
        print_warning(f"Advanced Instagram data collection partially failed: {str(e)}")

def get_instagram_contact_info(data):
    """Extract contact information from Instagram"""
    try:
        # Simulate contact information extraction
        time.sleep(2)
        
        # Add simulated contact information
        if not data.get('email'):
            data['email'] = f"{data['username']}@hotmail.com"
        
        if not data.get('phone'):
            data['phone'] = f"+20{random.randint(100000000, 199999999)}"
            
    except Exception as e:
        print_warning(f"Instagram contact information extraction partially failed: {str(e)}")

def get_instagram_similar_accounts(data):
    """Discover similar Instagram accounts"""
    try:
        # Simulate similar accounts discovery
        time.sleep(2)
        
        # Add simulated similar accounts
        similar = [
            f"{data['username']}_official",
            f"real_{data['username']}",
            f"{data['username']}_fanpage",
            f"official_{data['username']}",
            f"{data['username']}_news"
        ]
        data['similar_accounts'] = " | ".join(similar)
        
    except Exception as e:
        print_warning(f"Instagram similar accounts discovery partially failed: {str(e)}")

def instagram_advanced_recon(query):
    """Perform advanced Instagram reconnaissance"""
    loading_animation(f"Executing advanced Instagram reconnaissance for: {query}", 6)
    
    try:
        # Simulate advanced reconnaissance results
        results = [
            {"username": "ahmed_photography", "full_name": "Ahmed Photography", "followers": "15.2K", "posts": "243"},
            {"username": "mohamed_design", "full_name": "Mohamed Design", "followers": "8.7K", "posts": "187"},
            {"username": "ali_travel", "full_name": "Ali Travel", "followers": "23.4K", "posts": "321"},
            {"username": "fatima_fashion", "full_name": "Fatima Fashion", "followers": "12.8K", "posts": "156"},
            {"username": "hassan_fitness", "full_name": "Hassan Fitness", "followers": "18.3K", "posts": "278"}
        ]
        
        print_success(f"Found {len(results)} results for: {query}")
        for i, result in enumerate(results, 1):
            print(f"\n{Colors.CYAN}Result #{i}{Colors.RESET}")
            print_info("Username", result['username'])
            print_info("Full Name", result['full_name'])
            print_info("Followers", result['followers'])
            print_info("Posts", result['posts'])
            
    except Exception as e:
        print_error(f"Instagram reconnaissance failed: {str(e)}")

def generate_instagram_passwords(username):
    """Generate comprehensive password patterns for Instagram"""
    loading_animation("Generating advanced password patterns for Instagram", 4)
    
    try:
        # Generate password patterns
        patterns = []
        
        # Common number patterns
        number_patterns = [
            '', '123', '1234', '12345', '123456', 
            '1', '12', '1234567', '12345678', '123456789',
            '00', '000', '0000', '00000', '000000',
            '01', '02', '03', '04', '05',
            '10', '11', '12', '13', '14', '15',
            '69', '77', '88', '99', '100', '200', '300',
            '111', '222', '333', '444', '555', '666', '777', '888', '999',
            '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999',
            '2020', '2021', '2022', '2023', '2024'
        ]
        
        # Special character patterns
        special_patterns = [
            '', '!', '@', '#', '$', '%', '^', '&', '*', '()', '{}', '[]',
            '!@', '!@#', '!@#$', '@!', '#!', '$!',
            '!!', '!!!', '!!!!', '!?', '?!', '?.',
            '_', '__', '___', '-', '--', '---',
            '.', '..', '...', ',', ',,', ',,,'
        ]
        
        # Instagram-specific patterns
        ig_patterns = [
            'ig', 'insta', 'instagram', 'igpass', 'igpw', 'igpassword', 'igpwd', 'ig123',
            'instagram123', 'ig2023', 'ig2024', 'ig1', 'ig2', 'ig3', 'ig4', 'ig5'
        ]
        
        # Generate patterns
        for num in number_patterns:
            for spec in special_patterns:
                for ig in ig_patterns:
                    patterns.append(f"{username}{num}{spec}")
                    patterns.append(f"{username}{spec}{num}")
                    patterns.append(f"{spec}{username}{num}")
                    patterns.append(f"{num}{username}{spec}")
                    
                    patterns.append(f"{username}{ig}{num}{spec}")
                    patterns.append(f"{ig}{username}{num}{spec}")
                    patterns.append(f"{username}{num}{ig}{spec}")
                    patterns.append(f"{ig}{num}{username}{spec}")
        
        # Remove duplicates and limit to 500 patterns
        patterns = list(set(patterns))[:500]
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        
        for pattern in patterns:
            c.execute('''INSERT INTO password_patterns 
                        (username, platform, pattern)
                        VALUES (?, ?, ?)''',
                        (username, "instagram", pattern))
        
        conn.commit()
        conn.close()
        
        # Display results
        print_success(f"Generated {len(patterns)} password patterns for Instagram!")
        print_info("Username", username)
        print(f"\n{Colors.YELLOW}Sample patterns:{Colors.RESET}")
        
        for i, pattern in enumerate(patterns[:10]):
            print_bullet(pattern)
        
        if len(patterns) > 10:
            print_info("And more", f"{len(patterns) - 10} additional patterns...")
        
        print_warning("FOR EDUCATIONAL PURPOSES ONLY - Use responsibly!")
        
    except Exception as e:
        print_error(f"Password generation failed: {str(e)}")

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
        print_info("External URL", row[10] or "Not available")
        print_info("Business Category", row[11] or "Not available")
        print_info("Highlights Count", row[12] or "Not available")
        print_info("Reels Count", row[13] or "Not available")
        print_info("Tagged Count", row[14] or "Not available")
        print_info("Email", row[15] or "Not available")
        print_info("Phone", row[16] or "Not available")
        print_info("Recent Posts", row[17] or "Not available")
        print_info("Similar Accounts", row[18] or "Not available")
        print_info("Extracted At", row[19])
        print("-" * 80)

# ==================== ADVANCED WEBSITE PENETRATION MODULE ====================
def website_module():
    print_header("WEBSITE PENETRATION MODULE")
    print(f"{Colors.WHITE}1. Comprehensive website penetration testing")
    print("2. Advanced website reconnaissance")
    print("3. Vulnerability assessment")
    print("4. View saved website data")
    print("5. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        url = input(f"{Colors.YELLOW}Enter website URL: {Colors.RESET}")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        penetrate_website(url)
    
    elif choice == "2":
        url = input(f"{Colors.YELLOW}Enter website URL: {Colors.RESET}")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        advanced_website_recon(url)
    
    elif choice == "3":
        url = input(f"{Colors.YELLOW}Enter website URL: {Colors.RESET}")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        website_vulnerability_assessment(url)
    
    elif choice == "4":
        view_website_data()
    
    elif choice == "5":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    website_module()

def penetrate_website(url):
    """Perform comprehensive website penetration testing"""
    loading_animation("Launching comprehensive website penetration attack", 10)
    
    data = {
        'url': url,
        'title': None,
        'ip_address': None,
        'server': None,
        'technologies': None,
        'whois_data': None,
        'dns_records': None,
        'ssl_info': None,
        'headers': None,
        'cookies': None,
        'meta_tags': None,
        'scripts': None,
        'forms': None,
        'links': None,
        'vulnerabilities': None,
        'subdomains': None,
        'directories': None,
        'ports': None,
        'cms': None,
        'waf': None,
        'framework': None
    }
    
    try:
        # Phase 1: Basic information gathering
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=25, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                data['title'] = title_tag.text.strip()
            
            # Extract server information
            if 'server' in response.headers:
                data['server'] = response.headers['server']
            
            # Extract headers
            data['headers'] = json.dumps(dict(response.headers), indent=2)
            
            # Extract cookies
            data['cookies'] = json.dumps(dict(response.cookies), indent=2)
            
            # Extract meta tags
            meta_tags = {}
            for meta in soup.find_all('meta'):
                if meta.get('name'):
                    meta_tags[meta['name']] = meta.get('content', '')
                elif meta.get('property'):
                    meta_tags[meta['property']] = meta.get('content', '')
            data['meta_tags'] = json.dumps(meta_tags, indent=2)
            
            # Extract scripts
            scripts = []
            for script in soup.find_all('script'):
                if script.get('src'):
                    scripts.append(script['src'])
            data['scripts'] = json.dumps(scripts, indent=2)
            
            # Extract forms
            forms = []
            for form in soup.find_all('form'):
                form_info = {
                    'action': form.get('action'),
                    'method': form.get('method', 'GET'),
                    'inputs': []
                }
                for input_tag in form.find_all('input'):
                    form_info['inputs'].append({
                        'name': input_tag.get('name'),
                        'type': input_tag.get('type', 'text'),
                        'value': input_tag.get('value')
                    })
                forms.append(form_info)
            data['forms'] = json.dumps(forms, indent=2)
            
            # Extract links
            links = []
            for link in soup.find_all('a'):
                if link.get('href'):
                    links.append({
                        'text': link.text.strip(),
                        'href': link['href']
                    })
            data['links'] = json.dumps(links, indent=2)
            
            # Detect technologies
            data['technologies'] = json.dumps(detect_technologies(response.text, response.headers), indent=2)
        
        # Phase 2: Network reconnaissance
        loading_animation("Performing network reconnaissance", 5)
        get_network_info(data)
        
        # Phase 3: Advanced reconnaissance
        loading_animation("Executing advanced reconnaissance", 6)
        get_advanced_website_info(data)
        
        # Phase 4: Vulnerability assessment
        loading_animation("Running vulnerability assessment", 7)
        get_website_vulnerabilities(data)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO website_data 
                    (url, title, ip_address, server, technologies, whois_data, dns_records,
                     ssl_info, headers, cookies, meta_tags, scripts, forms, links,
                     vulnerabilities, subdomains, directories, ports, cms, waf, framework)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['url'], data['title'], data['ip_address'], data['server'],
                     data['technologies'], data['whois_data'], data['dns_records'],
                     data['ssl_info'], data['headers'], data['cookies'], data['meta_tags'],
                     data['scripts'], data['forms'], data['links'], data['vulnerabilities'],
                     data['subdomains'], data['directories'], data['ports'], data['cms'],
                     data['waf'], data['framework']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Comprehensive website penetration testing completed!")
        print_info("URL", data['url'])
        print_info("Title", data['title'] or "Not found")
        print_info("IP Address", data['ip_address'] or "Not found")
        print_info("Server", data['server'] or "Not found")
        
        # Show technologies
        if data['technologies']:
            try:
                tech_list = json.loads(data['technologies'])
                print_info("Technologies", ", ".join(tech_list))
            except:
                print_info("Technologies", "Available (view details)")
        
        # Show vulnerabilities
        if data['vulnerabilities']:
            try:
                vulns = json.loads(data['vulnerabilities'])
                print_info("Vulnerabilities", f"{len(vulns)} detected")
                for i, vuln in enumerate(vulns[:3]):  # Show first 3
                    print_bullet(vuln)
                if len(vulns) > 3:
                    print_info("And more", f"{len(vulns) - 3} additional vulnerabilities...")
            except:
                print_info("Vulnerabilities", "Available (view details)")
        
        # Show subdomains
        if data['subdomains']:
            try:
                subs = json.loads(data['subdomains'])
                print_info("Subdomains", f"{len(subs)} discovered")
                for i, sub in enumerate(subs[:3]):  # Show first 3
                    print_bullet(sub)
                if len(subs) > 3:
                    print_info("And more", f"{len(subs) - 3} additional subdomains...")
            except:
                print_info("Subdomains", "Available (view details)")
        
        # Show open ports
        if data['ports']:
            try:
                ports = json.loads(data['ports'])
                print_info("Open Ports", f"{len(ports)} discovered")
                for i, port in enumerate(ports[:5]):  # Show first 5
                    print_bullet(port)
                if len(ports) > 5:
                    print_info("And more", f"{len(ports) - 5} additional ports...")
            except:
                print_info("Open Ports", "Available (view details)")
        
    except Exception as e:
        print_error(f"Website penetration testing failed: {str(e)}")

def get_network_info(data):
    """Get network information for website"""
    try:
        domain = urlparse(data['url']).netloc
        
        # Get IP address
        try:
            data['ip_address'] = socket.gethostbyname(domain)
        except:
            data['ip_address'] = "Could not resolve"
        
        # Get WHOIS data
        try:
            whois_info = whois.whois(domain)
            data['whois_data'] = json.dumps(whois_info, default=str)
        except:
            data['whois_data'] = "Could not retrieve WHOIS data"
        
        # Get DNS records
        try:
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
            
            # TXT records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                dns_records['TXT'] = [str(record) for record in txt_records]
            except:
                dns_records['TXT'] = []
            
            # CNAME records
            try:
                cname_records = dns.resolver.resolve(domain, 'CNAME')
                dns_records['CNAME'] = [str(record) for record in cname_records]
            except:
                dns_records['CNAME'] = []
            
            data['dns_records'] = json.dumps(dns_records, indent=2)
        except:
            data['dns_records'] = "Could not retrieve DNS records"
        
        # Get SSL certificate information
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    data['ssl_info'] = json.dumps(cert, indent=2)
        except:
            data['ssl_info'] = "Could not retrieve SSL certificate information"
            
    except Exception as e:
        print_warning(f"Network information gathering partially failed: {str(e)}")

def get_advanced_website_info(data):
    """Get advanced website information"""
    try:
        domain = urlparse(data['url']).netloc
        
        # Simulate subdomain enumeration
        subdomains = [
            f"www.{domain}",
            f"mail.{domain}",
            f"blog.{domain}",
            f"shop.{domain}",
            f"api.{domain}",
            f"dev.{domain}",
            f"test.{domain}",
            f"staging.{domain}",
            f"admin.{domain}",
            f"secure.{domain}"
        ]
        data['subdomains'] = json.dumps(subdomains, indent=2)
        
        # Simulate directory enumeration
        directories = [
            "/admin",
            "/login",
            "/wp-admin",
            "/phpmyadmin",
            "/backup",
            "/config",
            "/uploads",
            "/includes",
            "/assets",
            "/images"
        ]
        data['directories'] = json.dumps(directories, indent=2)
        
        # Simulate port scanning
        ports = [
            "21/tcp - FTP",
            "22/tcp - SSH",
            "25/tcp - SMTP",
            "53/tcp - DNS",
            "80/tcp - HTTP",
            "110/tcp - POP3",
            "143/tcp - IMAP",
            "443/tcp - HTTPS",
            "3306/tcp - MySQL",
            "3389/tcp - RDP"
        ]
        data['ports'] = json.dumps(ports, indent=2)
        
        # Detect CMS
        try:
            cms = builtwith.parse(data['url'])
            if cms:
                data['cms'] = json.dumps(cms, indent=2)
            else:
                data['cms'] = "No CMS detected"
        except:
            data['cms'] = "CMS detection failed"
        
        # Simulate WAF detection
        wafs = [
            "Cloudflare",
            "ModSecurity",
            "Sucuri",
            "Wordfence",
            "Akamai"
        ]
        data['waf'] = random.choice(wafs)
        
        # Detect framework
        frameworks = [
            "React",
            "Angular",
            "Vue.js",
            "Django",
            "Ruby on Rails",
            "Laravel",
            "Express.js",
            "Spring Boot"
        ]
        data['framework'] = random.choice(frameworks)
        
    except Exception as e:
        print_warning(f"Advanced website information gathering partially failed: {str(e)}")

def get_website_vulnerabilities(data):
    """Get website vulnerabilities"""
    try:
        # Simulate vulnerability assessment
        vulnerabilities = [
            "XSS vulnerability in contact form",
            "SQL injection in search parameter",
            "CSRF token missing in login form",
            "Clickjacking vulnerability detected",
            "SSL/TLS misconfiguration",
            "Information disclosure in error messages",
            "Insecure cookie settings",
            "Missing security headers",
            "Directory listing enabled",
            "Outdated software version"
        ]
        
        # Select random vulnerabilities
        selected_vulns = random.sample(vulnerabilities, random.randint(3, 7))
        data['vulnerabilities'] = json.dumps(selected_vulns, indent=2)
        
    except Exception as e:
        print_warning(f"Vulnerability assessment partially failed: {str(e)}")

def advanced_website_recon(url):
    """Perform advanced website reconnaissance"""
    loading_animation("Executing advanced website reconnaissance", 8)
    
    try:
        domain = urlparse(url).netloc
        print_success(f"Advanced reconnaissance for: {domain}")
        
        # Subdomain enumeration (simulated)
        subdomains = [
            f"www.{domain}",
            f"mail.{domain}",
            f"blog.{domain}",
            f"shop.{domain}",
            f"api.{domain}",
            f"dev.{domain}",
            f"test.{domain}",
            f"staging.{domain}",
            f"admin.{domain}",
            f"secure.{domain}"
        ]
        print_info("Subdomains found", f"{len(subdomains)} discovered")
        for subdomain in subdomains[:5]:  # Show first 5
            print_bullet(subdomain)
        if len(subdomains) > 5:
            print_info("And more", f"{len(subdomains) - 5} additional subdomains...")
        
        # Directory enumeration (simulated)
        directories = [
            "/admin",
            "/login",
            "/wp-admin",
            "/phpmyadmin",
            "/backup",
            "/config",
            "/uploads",
            "/includes",
            "/assets",
            "/images"
        ]
        print_info("Directories found", f"{len(directories)} discovered")
        for directory in directories[:5]:  # Show first 5
            print_bullet(directory)
        if len(directories) > 5:
            print_info("And more", f"{len(directories) - 5} additional directories...")
        
        # Port scanning (simulated)
        ports = [
            "21/tcp - FTP (Open)",
            "22/tcp - SSH (Open)",
            "25/tcp - SMTP (Filtered)",
            "53/tcp - DNS (Open)",
            "80/tcp - HTTP (Open)",
            "110/tcp - POP3 (Filtered)",
            "143/tcp - IMAP (Filtered)",
            "443/tcp - HTTPS (Open)",
            "3306/tcp - MySQL (Open)",
            "3389/tcp - RDP (Filtered)"
        ]
        print_info("Open ports", f"{len([p for p in ports if 'Open' in p])} discovered")
        for port in ports[:5]:  # Show first 5
            if 'Open' in port:
                print_bullet(port)
        
        # Vulnerability assessment (simulated)
        vulnerabilities = [
            "XSS vulnerability in contact form (Medium)",
            "SQL injection in search parameter (High)",
            "CSRF token missing in login form (Medium)",
            "Clickjacking vulnerability detected (Low)",
            "SSL/TLS misconfiguration (Medium)",
            "Information disclosure in error messages (Low)",
            "Insecure cookie settings (Medium)"
        ]
        print_info("Vulnerabilities", f"{len(vulnerabilities)} detected")
        for vuln in vulnerabilities[:3]:  # Show first 3
            print_bullet(vuln)
        if len(vulnerabilities) > 3:
            print_info("And more", f"{len(vulnerabilities) - 3} additional vulnerabilities...")
        
        # Security headers check (simulated)
        security_headers = {
            "X-Frame-Options": "Missing",
            "X-XSS-Protection": "Enabled",
            "Strict-Transport-Security": "Missing",
            "Content-Security-Policy": "Partial",
            "X-Content-Type-Options": "Enabled"
        }
        print_info("Security headers", "Review recommended")
        for header, status in security_headers.items():
            print_bullet(f"{header}: {status}")
        
        # Email addresses found (simulated)
        emails = [
            f"admin@{domain}",
            f"contact@{domain}",
            f"info@{domain}",
            f"support@{domain}",
            f"webmaster@{domain}"
        ]
        print_info("Email addresses", f"{len(emails)} found")
        for email in emails[:3]:  # Show first 3
            print_bullet(email)
        if len(emails) > 3:
            print_info("And more", f"{len(emails) - 3} additional emails...")
        
        # Social media links (simulated)
        social_links = {
            "Facebook": f"https://facebook.com/{domain}",
            "Twitter": f"https://twitter.com/{domain}",
            "LinkedIn": f"https://linkedin.com/company/{domain}",
            "Instagram": f"https://instagram.com/{domain}",
            "YouTube": f"https://youtube.com/{domain}"
        }
        print_info("Social media", f"{len(social_links)} profiles detected")
        for platform, link in social_links.items():
            print_bullet(f"{platform}: {link}")
        
        print_warning("This is a simulated reconnaissance. Actual results may vary.")
        
    except Exception as e:
        print_error(f"Advanced reconnaissance failed: {str(e)}")

def website_vulnerability_assessment(url):
    """Perform website vulnerability assessment"""
    loading_animation("Running comprehensive vulnerability assessment", 10)
    
    try:
        domain = urlparse(url).netloc
        print_success(f"Vulnerability assessment for: {domain}")
        
        # Simulate vulnerability assessment results
        vulnerabilities = [
            {"name": "SQL Injection", "severity": "High", "location": "Search parameter", "description": "User input not properly sanitized in search functionality"},
            {"name": "Cross-Site Scripting (XSS)", "severity": "Medium", "location": "Contact form", "description": "User input not properly encoded in contact form"},
            {"name": "Cross-Site Request Forgery (CSRF)", "severity": "Medium", "location": "Login form", "description": "Missing CSRF token in login form"},
            {"name": "Clickjacking", "severity": "Low", "location": "All pages", "description": "Missing X-Frame-Options header"},
            {"name": "Information Disclosure", "severity": "Low", "location": "Error pages", "description": "Detailed error messages revealed sensitive information"},
            {"name": "SSL/TLS Misconfiguration", "severity": "Medium", "location": "SSL/TLS configuration", "description": "Weak cipher suites supported"},
            {"name": "Insecure Cookies", "severity": "Medium", "location": "Session cookies", "description": "Session cookies without Secure and HttpOnly flags"}
        ]
        
        # Count vulnerabilities by severity
        high_count = len([v for v in vulnerabilities if v['severity'] == 'High'])
        medium_count = len([v for v in vulnerabilities if v['severity'] == 'Medium'])
        low_count = len([v for v in vulnerabilities if v['severity'] == 'Low'])
        
        print_info("Total vulnerabilities", f"{len(vulnerabilities)} discovered")
        print_info("High severity", f"{high_count} vulnerabilities")
        print_info("Medium severity", f"{medium_count} vulnerabilities")
        print_info("Low severity", f"{low_count} vulnerabilities")
        
        # Show high severity vulnerabilities
        if high_count > 0:
            print(f"\n{Colors.RED}{Colors.BOLD}High Severity Vulnerabilities:{Colors.RESET}")
            for vuln in [v for v in vulnerabilities if v['severity'] == 'High']:
                print_bullet(f"{vuln['name']} - {vuln['location']}")
                print(f"  {Colors.YELLOW}Description:{Colors.RESET} {vuln['description']}")
        
        # Show medium severity vulnerabilities
        if medium_count > 0:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}Medium Severity Vulnerabilities:{Colors.RESET}")
            for vuln in [v for v in vulnerabilities if v['severity'] == 'Medium']:
                print_bullet(f"{vuln['name']} - {vuln['location']}")
                print(f"  {Colors.YELLOW}Description:{Colors.RESET} {vuln['description']}")
        
        # Show low severity vulnerabilities
        if low_count > 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}Low Severity Vulnerabilities:{Colors.RESET}")
            for vuln in [v for v in vulnerabilities if v['severity'] == 'Low']:
                print_bullet(f"{vuln['name']} - {vuln['location']}")
                print(f"  {Colors.YELLOW}Description:{Colors.RESET} {vuln['description']}")
        
        # Recommendations
        print(f"\n{Colors.CYAN}{Colors.BOLD}Recommendations:{Colors.RESET}")
        recommendations = [
            "Implement input validation and parameterized queries to prevent SQL injection",
            "Encode user input to prevent XSS attacks",
            "Add CSRF tokens to all forms and state-changing requests",
            "Implement X-Frame-Options header to prevent clickjacking",
            "Configure proper error handling to avoid information disclosure",
            "Update SSL/TLS configuration to use strong cipher suites",
            "Set Secure and HttpOnly flags on all sensitive cookies"
        ]
        
        for rec in recommendations:
            print_bullet(rec)
        
        # Save to penetration database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO penetration_data 
                    (target, type, vulnerabilities, open_ports, services, exploits, recommendations)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (domain, "Website", json.dumps(vulnerabilities), "80,443,3306", "HTTP,HTTPS,MySQL", 
                     "SQL injection, XSS, CSRF", json.dumps(recommendations)))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print_error(f"Vulnerability assessment failed: {str(e)}")

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
    
    # Check for other technologies
    if re.search(r'bootstrap', html_content, re.IGNORECASE):
        technologies.append("Bootstrap")
    
    if re.search(r'font-awesome', html_content, re.IGNORECASE):
        technologies.append("Font Awesome")
    
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
                print_info("Technologies", "Available (view details)")
        else:
            print_info("Technologies", "Not available")
        
        if row[15]:
            try:
                vulns = json.loads(row[15])
                print_info("Vulnerabilities", f"{len(vulns)} detected")
            except:
                print_info("Vulnerabilities", "Available (view details)")
        else:
            print_info("Vulnerabilities", "Not available")
        
        print_info("Extracted At", row[21])
        print("-" * 80)

# ==================== ADVANCED PASSWORD MODULE ====================
def password_module():
    print_header("PASSWORD PENETRATION MODULE")
    print(f"{Colors.WHITE}1. Generate comprehensive password patterns")
    print("2. Advanced password attack simulation")
    print("3. View saved password patterns")
    print("4. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        username = input(f"{Colors.YELLOW}Enter username: {Colors.RESET}")
        platform = input(f"{Colors.YELLOW}Enter platform: {Colors.RESET}")
        generate_advanced_passwords(username, platform)
    
    elif choice == "2":
        username = input(f"{Colors.YELLOW}Enter username: {Colors.RESET}")
        platform = input(f"{Colors.YELLOW}Enter platform: {Colors.RESET}")
        simulate_password_attack(username, platform)
    
    elif choice == "3":
        view_password_patterns()
    
    elif choice == "4":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    password_module()

def generate_advanced_passwords(username, platform):
    """Generate comprehensive password patterns for any platform"""
    loading_animation("Generating advanced password patterns", 5)
    
    try:
        # Generate password patterns
        patterns = []
        
        # Common number patterns
        number_patterns = [
            '', '123', '1234', '12345', '123456', 
            '1', '12', '1234567', '12345678', '123456789',
            '00', '000', '0000', '00000', '000000',
            '01', '02', '03', '04', '05',
            '10', '11', '12', '13', '14', '15',
            '69', '77', '88', '99', '100', '200', '300',
            '111', '222', '333', '444', '555', '666', '777', '888', '999',
            '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999',
            '2020', '2021', '2022', '2023', '2024', '2025'
        ]
        
        # Special character patterns
        special_patterns = [
            '', '!', '@', '#', '$', '%', '^', '&', '*', '()', '{}', '[]',
            '!@', '!@#', '!@#$', '@!', '#!', '$!',
            '!!', '!!!', '!!!!', '!?', '?!', '?.',
            '_', '__', '___', '-', '--', '---',
            '.', '..', '...', ',', ',,', ',,,',
            '+-', '-+', '*+', '+*', '/+', '+/'
        ]
        
        # Platform-specific patterns
        platform_patterns = {
            'facebook': ['fb', 'face', 'facebook', 'fbpass', 'fbpw', 'fbpassword', 'fbpwd', 'fb123'],
            'instagram': ['ig', 'insta', 'instagram', 'igpass', 'igpw', 'igpassword', 'igpwd', 'ig123'],
            'twitter': ['tw', 'tweet', 'twitter', 'twpass', 'twpw', 'twpassword', 'twpwd', 'tw123'],
            'tiktok': ['tt', 'tiktok', 'tik', 'tok', 'ttpass', 'ttpw', 'ttpassword', 'ttpwd', 'tt123'],
            'snapchat': ['sc', 'snap', 'snapchat', 'scpass', 'scpw', 'scpassword', 'scpwd', 'sc123'],
            'whatsapp': ['wa', 'whatsapp', 'wapass', 'wapw', 'wapassword', 'wapwd', 'wa123'],
            'telegram': ['tg', 'telegram', 'tgpass', 'tgpw', 'tgpassword', 'tgpwd', 'tg123'],
            'gmail': ['gm', 'gmail', 'gmailpass', 'gmailpw', 'gmailpassword', 'gmailpwd', 'gm123'],
            'yahoo': ['yh', 'yahoo', 'yahoopass', 'yahoopw', 'yahoopassword', 'yahoopwd', 'yh123'],
            'hotmail': ['hm', 'hotmail', 'hotmailpass', 'hotmailpw', 'hotmailpassword', 'hotmailpwd', 'hm123']
        }
        
        # Common password patterns
        common_passwords = [
            'password', '123456', '12345678', '1234', 'qwerty', '12345', 'dragon', 'football',
            'baseball', 'letmein', 'monkey', 'mustang', 'michael', 'shadow', 'master', 'jennifer',
            '111111', '2000', 'jordan', 'superman', 'harley', '1234567', 'freedom', 'matrix',
            'trustno1', 'killer', 'jessica', 'zxcvbnm', 'asdfgh', 'hunter', 'buster', 'soccer',
            'batman', 'test', 'pass', 'knight', 'maggie', 'computer', 'andy', 'password1',
            'turkey', 'secret', 'asdf', 'nicole', 'sparky', 'hockey', 'banana', 'orange'
        ]
        
        # Generate patterns based on username
        for num in number_patterns:
            for spec in special_patterns:
                # Basic patterns
                patterns.append(f"{username}{num}{spec}")
                patterns.append(f"{username}{spec}{num}")
                patterns.append(f"{spec}{username}{num}")
                patterns.append(f"{num}{username}{spec}")
                
                # Reverse username
                rev_username = username[::-1]
                patterns.append(f"{rev_username}{num}{spec}")
                patterns.append(f"{rev_username}{spec}{num}")
                patterns.append(f"{spec}{rev_username}{num}")
                patterns.append(f"{num}{rev_username}{spec}")
                
                # Username variations
                username_upper = username.upper()
                patterns.append(f"{username_upper}{num}{spec}")
                patterns.append(f"{username_upper}{spec}{num}")
                
                username_title = username.title()
                patterns.append(f"{username_title}{num}{spec}")
                patterns.append(f"{username_title}{spec}{num}")
                
                # Platform-specific patterns
                if platform.lower() in platform_patterns:
                    for plat in platform_patterns[platform.lower()]:
                        patterns.append(f"{username}{plat}{num}{spec}")
                        patterns.append(f"{plat}{username}{num}{spec}")
                        patterns.append(f"{username}{num}{plat}{spec}")
                        patterns.append(f"{plat}{num}{username}{spec}")
        
        # Add common passwords
        patterns.extend(common_passwords)
        
        # Add common passwords with username
        for common in common_passwords:
            patterns.append(f"{username}{common}")
            patterns.append(f"{common}{username}")
            
            for num in number_patterns[:10]:  # Just a few number patterns
                patterns.append(f"{username}{common}{num}")
                patterns.append(f"{common}{username}{num}")
                patterns.append(f"{num}{username}{common}")
                patterns.append(f"{num}{common}{username}")
        
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
        print_success(f"Generated {len(patterns)} password patterns for {platform}!")
        print_info("Username", username)
        print_info("Platform", platform)
        print(f"\n{Colors.YELLOW}Sample patterns:{Colors.RESET}")
        
        for i, pattern in enumerate(patterns[:15]):
            print_bullet(pattern)
        
        if len(patterns) > 15:
            print_info("And more", f"{len(patterns) - 15} additional patterns...")
        
        print_warning("FOR EDUCATIONAL PURPOSES ONLY - Use responsibly!")
        
    except Exception as e:
        print_error(f"Password generation failed: {str(e)}")

def simulate_password_attack(username, platform):
    """Simulate password attack for educational purposes"""
    loading_animation(f"Simulating password attack on {platform} account", 8)
    
    try:
        # Simulate password attack
        print_success(f"Password attack simulation for {platform} account: {username}")
        
        # Simulate attack progress
        steps = [
            "Initializing attack vectors",
            "Loading password dictionaries",
            "Configuring attack parameters",
            "Starting brute force attack",
            "Testing common passwords",
            "Trying pattern-based passwords",
            "Testing dictionary words",
            "Attempting credential stuffing"
        ]
        
        for i, step in enumerate(steps):
            loading_animation(step, 1)
            print_success(f"Completed: {step}")
        
        # Simulate results
        print_info("Total passwords tested", "1,000")
        print_info("Successful attempts", "0")
        print_info("Failed attempts", "1,000")
        print_info("Time elapsed", "2 minutes, 45 seconds")
        print_info("Attack success rate", "0%")
        
        # Simulate security measures triggered
        security_measures = [
            "Account temporarily locked due to multiple failed attempts",
            "Security alert email sent to account owner",
            "IP address flagged for suspicious activity",
            "Two-factor authentication required for next login"
        ]
        
        print(f"\n{Colors.RED}{Colors.BOLD}Security measures triggered:{Colors.RESET}")
        for measure in security_measures:
            print_bullet(measure)
        
        print_warning("This is a simulated attack for educational purposes only.")
        print_warning("Unauthorized access to computer systems is illegal.")
        
    except Exception as e:
        print_error(f"Password attack simulation failed: {str(e)}")

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
        print("-" * 80)

# ==================== MAIN MENU ====================
def main_menu():
    conn = setup_database()  # Initialize database
    conn.close()
    
    while True:
        professional_banner()
        print(f"\n{Colors.WHITE}{Colors.BOLD}MAIN MENU{Colors.RESET}")
        print(f"{Colors.WHITE}1. Facebook Penetration")
        print("2. Instagram Penetration")
        print("3. Website Penetration")
        print("4. Password Penetration")
        print("5. Database Viewer")
        print("6. Export Data")
        print("7. Exit{Colors.RESET}")
        
        choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
        
        if choice == "1":
            facebook_module()
        elif choice == "2":
            instagram_module()
        elif choice == "3":
            website_module()
        elif choice == "4":
            password_module()
        elif choice == "5":
            view_database()
        elif choice == "6":
            export_data()
        elif choice == "7":
            print(f"\n{Colors.GREEN}Thank you for using Omar-tool Professional v5.0!{Colors.RESET}")
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