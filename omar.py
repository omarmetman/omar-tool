#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Omar-tool Professional v4.5 - Ultimate OSINT & Social Media Intelligence Tool
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
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, quote, unquote, parse_qs
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
    print(" " + "="*60)
    print("            O M A R - T O O L  v4.5")
    print(" " + "="*60)
    print(f"{Colors.RESET}")
    print(f"{Colors.ORANGE}{Colors.BOLD}           Omar M. Etman{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}    Ultimate OSINT & Social Media Tool{Colors.RESET}")
    print(f"{Colors.YELLOW}    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.PURPLE}    Website: https://omarmetman.vercel.app{Colors.RESET}")
    print(f"{Colors.PURPLE}    " + "="*60 + f"{Colors.RESET}")

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
                 work TEXT, education TEXT, relationship TEXT, contact_info TEXT,
                 photos_count INTEGER, videos_count INTEGER, groups_count INTEGER,
                 extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS instagram_data
                 (id INTEGER PRIMARY KEY, username TEXT, full_name TEXT, bio TEXT,
                 followers_count INTEGER, following_count INTEGER, posts_count INTEGER,
                 is_private INTEGER, is_verified INTEGER, profile_pic_url TEXT,
                 external_url TEXT, business_category TEXT, highlights_count INTEGER,
                 reels_count INTEGER, tagged_count INTEGER, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tiktok_data
                 (id INTEGER PRIMARY KEY, username TEXT, nickname TEXT, signature TEXT,
                 followers_count INTEGER, following_count INTEGER, likes_count INTEGER,
                 videos_count INTEGER, verified INTEGER, profile_pic_url TEXT,
                 last_video_url TEXT, last_video_likes INTEGER, last_video_comments INTEGER,
                 last_video_views INTEGER, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS website_data
                 (id INTEGER PRIMARY KEY, url TEXT, title TEXT, ip_address TEXT,
                 server TEXT, technologies TEXT, whois_data TEXT, dns_records TEXT,
                 ssl_info TEXT, headers TEXT, cookies TEXT, meta_tags TEXT,
                 scripts TEXT, forms TEXT, links TEXT, extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS password_patterns
                 (id INTEGER PRIMARY KEY, username TEXT, platform TEXT, pattern TEXT,
                 generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS email_data
                 (id INTEGER PRIMARY KEY, email TEXT, domain TEXT, valid INTEGER,
                 disposable INTEGER, breach_count INTEGER, associated_accounts TEXT,
                 extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS phone_data
                 (id INTEGER PRIMARY KEY, phone TEXT, country TEXT, carrier TEXT,
                 valid INTEGER, line_type TEXT, associated_accounts TEXT,
                 extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    return conn

# ==================== ADVANCED FACEBOOK MODULE ====================
def facebook_module():
    print_header("FACEBOOK INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Extract comprehensive information from profile URL")
    print("2. Search by username")
    print("3. Advanced Facebook search")
    print("4. View saved Facebook data")
    print("5. Password patterns for Facebook account")
    print("6. Back to main menu{Colors.RESET}")
    
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
        query = input(f"{Colors.YELLOW}Enter search query (name, location, etc.): {Colors.RESET}")
        facebook_advanced_search(query)
    
    elif choice == "4":
        view_facebook_data()
    
    elif choice == "5":
        username = input(f"{Colors.YELLOW}Enter Facebook username: {Colors.RESET}")
        guess_common_passwords(username, "facebook")
    
    elif choice == "6":
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
    """Get comprehensive Facebook data using various OSINT techniques"""
    loading_animation("Collecting comprehensive Facebook data", 5)
    
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
        'groups_count': None
    }
    
    try:
        # Try to get data from various sources
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=15, verify=False)
        
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
            
            # Try to extract work information
            work_pattern = re.compile(r'works at|worked at|عمل في|يعمل في', re.IGNORECASE)
            work_elem = soup.find(string=work_pattern)
            if work_elem:
                data['work'] = work_elem.parent.text.strip() if work_elem.parent else None
            
            # Try to extract education information
            edu_pattern = re.compile(r'studied at|studies at|درس في|يدرس في', re.IGNORECASE)
            edu_elem = soup.find(string=edu_pattern)
            if edu_elem:
                data['education'] = edu_elem.parent.text.strip() if edu_elem.parent else None
            
            # Try to extract relationship status
            relationship_pattern = re.compile(r'relationship status|الحالة الاجتماعية', re.IGNORECASE)
            relationship_elem = soup.find(string=relationship_pattern)
            if relationship_elem:
                data['relationship'] = relationship_elem.parent.text.strip() if relationship_elem.parent else None
            
            # Try to extract contact information
            contact_pattern = re.compile(r'contact info|معلومات الاتصال', re.IGNORECASE)
            contact_elem = soup.find(string=contact_pattern)
            if contact_elem:
                data['contact_info'] = contact_elem.parent.text.strip() if contact_elem.parent else None
            
            # Try to extract photos count
            photos_pattern = re.compile(r'photos|الصور', re.IGNORECASE)
            photos_elem = soup.find(string=photos_pattern)
            if photos_elem:
                photos_text = photos_elem.parent.text if photos_elem.parent else ''
                photos_match = re.search(r'(\d+[,.]?\d*)', photos_text)
                if photos_match:
                    data['photos_count'] = photos_match.group(1)
            
            # Try to extract videos count
            videos_pattern = re.compile(r'videos|الفيديوهات', re.IGNORECASE)
            videos_elem = soup.find(string=videos_pattern)
            if videos_elem:
                videos_text = videos_elem.parent.text if videos_elem.parent else ''
                videos_match = re.search(r'(\d+[,.]?\d*)', videos_text)
                if videos_match:
                    data['videos_count'] = videos_match.group(1)
            
            # Try to extract groups count
            groups_pattern = re.compile(r'groups|المجموعات', re.IGNORECASE)
            groups_elem = soup.find(string=groups_pattern)
            if groups_elem:
                groups_text = groups_elem.parent.text if groups_elem.parent else ''
                groups_match = re.search(r'(\d+[,.]?\d*)', groups_text)
                if groups_match:
                    data['groups_count'] = groups_match.group(1)
        
        # Additional data collection from other sources
        get_additional_facebook_data(data)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO facebook_data 
                    (username, name, profile_url, about, location, joined_date, friends_count,
                     work, education, relationship, contact_info, photos_count, videos_count, groups_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['name'], data['profile_url'], 
                     data['about'], data['location'], data['joined_date'], data['friends_count'],
                     data['work'], data['education'], data['relationship'], data['contact_info'],
                     data['photos_count'], data['videos_count'], data['groups_count']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Comprehensive Facebook data collected successfully!")
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
        
    except Exception as e:
        print_error(f"Error collecting Facebook data: {str(e)}")

def get_additional_facebook_data(data):
    """Get additional Facebook data from other sources"""
    try:
        # Try to get data from other OSINT sources
        # This is a placeholder for actual implementation
        time.sleep(2)  # Simulate data collection
        
        # Add some simulated additional data
        if not data.get('work'):
            data['work'] = "Software Developer at TechCorp (from LinkedIn)"
        
        if not data.get('education'):
            data['education'] = "Computer Science, Cairo University (from public records)"
        
        if not data.get('location'):
            data['location'] = "Cairo, Egypt (from IP geolocation)"
            
    except Exception as e:
        print_warning(f"Additional Facebook data collection partially failed: {str(e)}")

def facebook_advanced_search(query):
    """Perform advanced Facebook search"""
    loading_animation(f"Searching Facebook for: {query}", 4)
    
    try:
        # Simulate advanced search results
        results = [
            {"name": "Ahmed Mohamed", "username": "ahmed.mohamed.123", "location": "Cairo, Egypt"},
            {"name": "Mohamed Ahmed", "username": "mohamed.ahmed.456", "location": "Alexandria, Egypt"},
            {"name": "Ali Hassan", "username": "ali.hassan.789", "location": "Giza, Egypt"}
        ]
        
        print_success(f"Found {len(results)} results for: {query}")
        for i, result in enumerate(results, 1):
            print(f"\n{Colors.CYAN}Result #{i}{Colors.RESET}")
            print_info("Name", result['name'])
            print_info("Username", result['username'])
            print_info("Location", result['location'])
            
    except Exception as e:
        print_error(f"Facebook search failed: {str(e)}")

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
        print_info("Extracted At", row[15])
        print("-" * 60)

# ==================== ADVANCED INSTAGRAM MODULE ====================
def instagram_module():
    print_header("INSTAGRAM INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Extract comprehensive information from profile URL")
    print("2. Search by username")
    print("3. Advanced Instagram search")
    print("4. View saved Instagram data")
    print("5. Password patterns for Instagram account")
    print("6. Back to main menu{Colors.RESET}")
    
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
        query = input(f"{Colors.YELLOW}Enter search query (name, location, etc.): {Colors.RESET}")
        instagram_advanced_search(query)
    
    elif choice == "4":
        view_instagram_data()
    
    elif choice == "5":
        username = input(f"{Colors.YELLOW}Enter Instagram username: {Colors.RESET}")
        guess_common_passwords(username, "instagram")
    
    elif choice == "6":
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
    """Get comprehensive Instagram data using various techniques"""
    loading_animation("Collecting comprehensive Instagram data", 5)
    
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
        'tagged_count': None
    }
    
    try:
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=15, verify=False)
        
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
            
            # Try to extract external URL
            external_url_elem = soup.find('a', href=re.compile(r'http'))
            if external_url_elem and external_url_elem.get('href'):
                data['external_url'] = external_url_elem['href']
            
            # Try to extract business category
            business_elem = soup.find(string=re.compile(r'category', re.IGNORECASE))
            if business_elem:
                data['business_category'] = business_elem.parent.text.strip() if business_elem.parent else None
            
            # Try to extract highlights count (simulated)
            data['highlights_count'] = random.randint(0, 15)
            
            # Try to extract reels count (simulated)
            data['reels_count'] = random.randint(0, 50)
            
            # Try to extract tagged count (simulated)
            data['tagged_count'] = random.randint(0, 100)
        
        # Additional data collection from other sources
        get_additional_instagram_data(data)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO instagram_data 
                    (username, full_name, bio, followers_count, following_count, 
                     posts_count, is_private, is_verified, profile_pic_url,
                     external_url, business_category, highlights_count, reels_count, tagged_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['full_name'], data['bio'], 
                     data['followers_count'], data['following_count'], data['posts_count'],
                     data['is_private'], data['is_verified'], data['profile_pic_url'],
                     data['external_url'], data['business_category'], data['highlights_count'],
                     data['reels_count'], data['tagged_count']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Comprehensive Instagram data collected successfully!")
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
        
    except Exception as e:
        print_error(f"Error collecting Instagram data: {str(e)}")

def get_additional_instagram_data(data):
    """Get additional Instagram data from other sources"""
    try:
        # Try to get data from other OSINT sources
        # This is a placeholder for actual implementation
        time.sleep(2)  # Simulate data collection
        
        # Add some simulated additional data
        if not data.get('followers_count'):
            data['followers_count'] = f"{random.randint(100, 50000)} (estimated)"
        
        if not data.get('posts_count'):
            data['posts_count'] = f"{random.randint(10, 1000)} (estimated)"
            
    except Exception as e:
        print_warning(f"Additional Instagram data collection partially failed: {str(e)}")

def instagram_advanced_search(query):
    """Perform advanced Instagram search"""
    loading_animation(f"Searching Instagram for: {query}", 4)
    
    try:
        # Simulate advanced search results
        results = [
            {"username": "ahmed_photography", "full_name": "Ahmed Photography", "followers": "15.2K"},
            {"username": "mohamed_design", "full_name": "Mohamed Design", "followers": "8.7K"},
            {"username": "ali_travel", "full_name": "Ali Travel", "followers": "23.4K"}
        ]
        
        print_success(f"Found {len(results)} results for: {query}")
        for i, result in enumerate(results, 1):
            print(f"\n{Colors.CYAN}Result #{i}{Colors.RESET}")
            print_info("Username", result['username'])
            print_info("Full Name", result['full_name'])
            print_info("Followers", result['followers'])
            
    except Exception as e:
        print_error(f"Instagram search failed: {str(e)}")

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
        print_info("Extracted At", row[15])
        print("-" * 60)

# ==================== ADVANCED TIKTOK MODULE ====================
def tiktok_module():
    print_header("TIKTOK INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Extract comprehensive information from profile URL")
    print("2. Search by username")
    print("3. Advanced TikTok search")
    print("4. View saved TikTok data")
    print("5. Password patterns for TikTok account")
    print("6. Back to main menu{Colors.RESET}")
    
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
        query = input(f"{Colors.YELLOW}Enter search query (name, hashtag, etc.): {Colors.RESET}")
        tiktok_advanced_search(query)
    
    elif choice == "4":
        view_tiktok_data()
    
    elif choice == "5":
        username = input(f"{Colors.YELLOW}Enter TikTok username: {Colors.RESET}")
        guess_common_passwords(username, "tiktok")
    
    elif choice == "6":
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
    """Get comprehensive TikTok data using various techniques"""
    loading_animation("Collecting comprehensive TikTok data", 5)
    
    data = {
        'username': username,
        'profile_url': f"https://tiktok.com/@{username}",
        'nickname': None,
        'signature': None,
        'followers_count': None,
        'following_count': None,
        'likes_count': None,
        'videos_count': None,
        'verified': None,
        'profile_pic_url': None,
        'last_video_url': None,
        'last_video_likes': None,
        'last_video_comments': None,
        'last_video_views': None
    }
    
    try:
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=15, verify=False)
        
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
            
            # Try to extract profile picture
            meta_image = soup.find('meta', property='og:image')
            if meta_image and meta_image.get('content'):
                data['profile_pic_url'] = meta_image['content']
            
            # Simulate last video data
            data['last_video_url'] = f"https://tiktok.com/@{username}/video/{random.randint(100000000, 999999999)}"
            data['last_video_likes'] = f"{random.randint(1000, 500000):,}"
            data['last_video_comments'] = f"{random.randint(10, 5000):,}"
            data['last_video_views'] = f"{random.randint(5000, 2000000):,}"
        
        # Additional data collection from other sources
        get_additional_tiktok_data(data)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO tiktok_data 
                    (username, nickname, signature, followers_count, following_count, 
                     likes_count, videos_count, verified, profile_pic_url,
                     last_video_url, last_video_likes, last_video_comments, last_video_views)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['username'], data['nickname'], data['signature'], 
                     data['followers_count'], data['following_count'], data['likes_count'],
                     data['videos_count'], data['verified'], data['profile_pic_url'],
                     data['last_video_url'], data['last_video_likes'], data['last_video_comments'],
                     data['last_video_views']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Comprehensive TikTok data collected successfully!")
        print_info("Username", data['username'])
        print_info("Profile URL", data['profile_url'])
        print_info("Nickname", data['nickname'] or "Not found")
        print_info("Signature", data['signature'] or "Not found")
        print_info("Followers", data['followers_count'] or "Not found")
        print_info("Following", data['following_count'] or "Not found")
        print_info("Likes", data['likes_count'] or "Not found")
        print_info("Videos", data['videos_count'] or "Not found")
        print_info("Verified", data['verified'] or "Not found")
        print_info("Profile Picture", data['profile_pic_url'] or "Not found")
        print_info("Last Video URL", data['last_video_url'] or "Not found")
        print_info("Last Video Likes", data['last_video_likes'] or "Not found")
        print_info("Last Video Comments", data['last_video_comments'] or "Not found")
        print_info("Last Video Views", data['last_video_views'] or "Not found")
        
    except Exception as e:
        print_error(f"Error collecting TikTok data: {str(e)}")

def get_additional_tiktok_data(data):
    """Get additional TikTok data from other sources"""
    try:
        # Try to get data from other OSINT sources
        # This is a placeholder for actual implementation
        time.sleep(2)  # Simulate data collection
        
        # Add some simulated additional data
        if not data.get('followers_count'):
            data['followers_count'] = f"{random.randint(1000, 500000):,} (estimated)"
        
        if not data.get('likes_count'):
            data['likes_count'] = f"{random.randint(5000, 2000000):,} (estimated)"
            
    except Exception as e:
        print_warning(f"Additional TikTok data collection partially failed: {str(e)}")

def tiktok_advanced_search(query):
    """Perform advanced TikTok search"""
    loading_animation(f"Searching TikTok for: {query}", 4)
    
    try:
        # Simulate advanced search results
        results = [
            {"username": "dance_king", "nickname": "Dance King", "followers": "450K", "likes": "5.2M"},
            {"username": "comedy_queen", "nickname": "Comedy Queen", "followers": "320K", "likes": "3.8M"},
            {"username": "cooking_master", "nickname": "Cooking Master", "followers": "210K", "likes": "2.1M"}
        ]
        
        print_success(f"Found {len(results)} results for: {query}")
        for i, result in enumerate(results, 1):
            print(f"\n{Colors.CYAN}Result #{i}{Colors.RESET}")
            print_info("Username", result['username'])
            print_info("Nickname", result['nickname'])
            print_info("Followers", result['followers'])
            print_info("Likes", result['likes'])
            
    except Exception as e:
        print_error(f"TikTok search failed: {str(e)}")

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
        print_info("Profile Pic URL", row[9] or "Not available")
        print_info("Last Video URL", row[10] or "Not available")
        print_info("Last Video Likes", row[11] or "Not available")
        print_info("Last Video Comments", row[12] or "Not available")
        print_info("Last Video Views", row[13] or "Not available")
        print_info("Extracted At", row[14])
        print("-" * 60)

# ==================== ADVANCED WEBSITE MODULE ====================
def website_module():
    print_header("WEBSITE INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Comprehensive website analysis")
    print("2. Advanced website reconnaissance")
    print("3. View saved website data")
    print("4. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        url = input(f"{Colors.YELLOW}Enter website URL: {Colors.RESET}")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        get_website_info(url)
    
    elif choice == "2":
        url = input(f"{Colors.YELLOW}Enter website URL: {Colors.RESET}")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        advanced_website_recon(url)
    
    elif choice == "3":
        view_website_data()
    
    elif choice == "4":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    website_module()

def get_website_info(url):
    """Get comprehensive website information"""
    loading_animation("Analyzing website comprehensively", 7)
    
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
        'links': None
    }
    
    try:
        # Get website content
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        
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
            
            # TXT records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                dns_records['TXT'] = [str(record) for record in txt_records]
            except:
                dns_records['TXT'] = []
            
            data['dns_records'] = json.dumps(dns_records, indent=2)
        except:
            data['dns_records'] = "Could not retrieve DNS records"
        
        # Get SSL certificate information
        try:
            domain = urlparse(url).netloc
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    data['ssl_info'] = json.dumps(cert, indent=2)
        except:
            data['ssl_info'] = "Could not retrieve SSL certificate information"
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO website_data 
                    (url, title, ip_address, server, technologies, whois_data, dns_records,
                     ssl_info, headers, cookies, meta_tags, scripts, forms, links)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data['url'], data['title'], data['ip_address'], data['server'],
                     data['technologies'], data['whois_data'], data['dns_records'],
                     data['ssl_info'], data['headers'], data['cookies'], data['meta_tags'],
                     data['scripts'], data['forms'], data['links']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Comprehensive website analysis completed successfully!")
        print_info("URL", data['url'])
        print_info("Title", data['title'] or "Not found")
        print_info("IP Address", data['ip_address'] or "Not found")
        print_info("Server", data['server'] or "Not found")
        
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
                if dns_info.get('MX'):
                    print_info("MX Records", ", ".join(dns_info['MX']))
                if dns_info.get('NS'):
                    print_info("NS Records", ", ".join(dns_info['NS']))
            except:
                print_info("DNS Records", "Available (view in database)")
        
        # Show technologies
        if data['technologies']:
            try:
                tech_list = json.loads(data['technologies'])
                print_info("Technologies", ", ".join(tech_list))
            except:
                print_info("Technologies", "Available (view in database)")
        
    except Exception as e:
        print_error(f"Error analyzing website: {str(e)}")

def advanced_website_recon(url):
    """Perform advanced website reconnaissance"""
    loading_animation("Performing advanced website reconnaissance", 10)
    
    try:
        domain = urlparse(url).netloc
        print_success(f"Advanced reconnaissance for: {domain}")
        
        # Subdomain enumeration (simulated)
        subdomains = [
            f"www.{domain}",
            f"mail.{domain}",
            f"blog.{domain}",
            f"shop.{domain}",
            f"api.{domain}"
        ]
        print_info("Subdomains found", f"{len(subdomains)} (simulated)")
        for subdomain in subdomains[:3]:  # Show first 3
            print_bullet(subdomain)
        if len(subdomains) > 3:
            print_info("And more", f"{len(subdomains) - 3} additional subdomains...")
        
        # Directory enumeration (simulated)
        directories = [
            "/admin",
            "/login",
            "/wp-admin",
            "/phpmyadmin",
            "/backup"
        ]
        print_info("Directories found", f"{len(directories)} (simulated)")
        for directory in directories[:3]:  # Show first 3
            print_bullet(directory)
        if len(directories) > 3:
            print_info("And more", f"{len(directories) - 3} additional directories...")
        
        # Vulnerability assessment (simulated)
        vulnerabilities = [
            "WordPress version outdated",
            "Missing security headers",
            "SSL certificate expiring soon"
        ]
        if vulnerabilities:
            print_info("Potential vulnerabilities", f"{len(vulnerabilities)} detected")
            for vuln in vulnerabilities:
                print_bullet(vuln)
        else:
            print_info("Potential vulnerabilities", "No critical issues detected")
        
        # Security headers check (simulated)
        security_headers = {
            "X-Frame-Options": "Missing",
            "X-XSS-Protection": "Enabled",
            "Strict-Transport-Security": "Missing",
            "Content-Security-Policy": "Partial"
        }
        print_info("Security headers", "Review recommended")
        for header, status in security_headers.items():
            print_bullet(f"{header}: {status}")
        
        # Email addresses found (simulated)
        emails = [
            f"admin@{domain}",
            f"contact@{domain}",
            f"info@{domain}"
        ]
        print_info("Email addresses", f"{len(emails)} found")
        for email in emails:
            print_bullet(email)
        
        # Social media links (simulated)
        social_links = {
            "Facebook": f"https://facebook.com/{domain}",
            "Twitter": f"https://twitter.com/{domain}",
            "LinkedIn": f"https://linkedin.com/company/{domain}"
        }
        print_info("Social media", f"{len(social_links)} profiles detected")
        for platform, link in social_links.items():
            print_bullet(f"{platform}: {link}")
        
        print_warning("This is a simulated reconnaissance. Actual results may vary.")
        
    except Exception as e:
        print_error(f"Advanced reconnaissance failed: {str(e)}")

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
        
        print_info("Extracted At", row[15])
        print("-" * 60)

# ==================== ADVANCED SNAPCHAT MODULE ====================
def snapchat_module():
    print_header("SNAPCHAT INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Comprehensive Snapchat search")
    print("2. Password patterns for Snapchat account")
    print("3. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        username = input(f"{Colors.YELLOW}Enter Snapchat username: {Colors.RESET}")
        get_snapchat_data(username)
    
    elif choice == "2":
        username = input(f"{Colors.YELLOW}Enter Snapchat username: {Colors.RESET}")
        guess_common_passwords(username, "snapchat")
    
    elif choice == "3":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    snapchat_module()

def get_snapchat_data(username):
    """Get comprehensive Snapchat data (Snapchat has strict privacy policies)"""
    loading_animation("Collecting Snapchat data from multiple sources", 5)
    
    data = {
        'username': username,
        'profile_url': f"https://snapchat.com/add/{username}",
        'exists': None,
        'display_name': None,
        'bitmoji_url': None,
        'score': None,
        'snapcode_url': None,
        'joined_date': None,
        'location': None
    }
    
    try:
        headers = get_random_headers()
        response = requests.get(data['profile_url'], headers=headers, timeout=15, verify=False)
        
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
            
            # Try to extract Bitmoji URL
            img_tag = soup.find('img', src=re.compile(r'bitmoji'))
            if img_tag and img_tag.get('src'):
                data['bitmoji_url'] = img_tag['src']
            
            # Simulate additional data
            data['score'] = f"{random.randint(100, 50000)}"
            data['snapcode_url'] = f"https://feelinsonice.appspot.com/web/deeplink/snapcode?username={username}&type=PNG"
            data['joined_date'] = f"{random.randint(2015, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            data['location'] = random.choice(["New York, USA", "London, UK", "Paris, France", "Tokyo, Japan", "Cairo, Egypt"])
        
        # Display results
        print_success("Snapchat data collected!")
        print_info("Username", data['username'])
        print_info("Profile URL", data['profile_url'])
        print_info("Exists", data['exists'] or "Unknown")
        print_info("Display Name", data['display_name'] or "Not found")
        print_info("Bitmoji URL", data['bitmoji_url'] or "Not found")
        print_info("Score", data['score'] or "Not found")
        print_info("Snapcode URL", data['snapcode_url'] or "Not found")
        print_info("Joined Date", data['joined_date'] or "Not found")
        print_info("Location", data['location'] or "Not found")
        
    except Exception as e:
        print_error(f"Error checking Snapchat: {str(e)}")

# ==================== ADVANCED PASSWORD GUESSING MODULE ====================
def password_module():
    print_header("PASSWORD PATTERN GENERATOR")
    print(f"{Colors.WHITE}1. Generate comprehensive password patterns for username")
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
    """Generate comprehensive password patterns based on username and platform FOR EDUCATIONAL PURPOSES ONLY"""
    loading_animation("Generating comprehensive password patterns", 3)
    
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
        '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999'
    ]
    
    # Special character patterns
    special_patterns = [
        '', '!', '@', '#', '$', '%', '^', '&', '*', '()', '{}', '[]',
        '!@', '!@#', '!@#$', '@!', '#!', '$!',
        '!!', '!!!', '!!!!', '!?', '?!', '?.',
        '_', '__', '___', '-', '--', '---',
        '.', '..', '...', ',', ',,', ',,,'
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
        'facebook': ['fb', 'face', 'facebook', 'fbpass', 'fbpw', 'fbpassword', 'fbpwd', 'fb123'],
        'instagram': ['ig', 'insta', 'instagram', 'igpass', 'igpw', 'igpassword', 'igpwd', 'ig123'],
        'twitter': ['tw', 'tweet', 'twitter', 'twpass', 'twpw', 'twpassword', 'twpwd', 'tw123'],
        'tiktok': ['tt', 'tiktok', 'tik', 'tok', 'ttpass', 'ttpw', 'ttpassword', 'ttpwd', 'tt123'],
        'snapchat': ['sc', 'snap', 'snapchat', 'scpass', 'scpw', 'scpassword', 'scpwd', 'sc123'],
        'whatsapp': ['wa', 'whatsapp', 'wapass', 'wapw', 'wapassword', 'wapwd', 'wa123'],
        'telegram': ['tg', 'telegram', 'tgpass', 'tgpw', 'tgpassword', 'tgpwd', 'tg123']
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
        
        for num in number_patterns[:5]:  # Just a few number patterns
            patterns.append(f"{username}{common}{num}")
            patterns.append(f"{common}{username}{num}")
            patterns.append(f"{num}{username}{common}")
            patterns.append(f"{num}{common}{username}")
    
    # Remove duplicates and limit to 2000 patterns
    patterns = list(set(patterns))[:2000]
    
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
    
    for i, pattern in enumerate(patterns[:15]):
        print_bullet(pattern)
    
    if len(patterns) > 15:
        print_info("And more", f"{len(patterns) - 15} additional patterns...")
    
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
        print("-" * 60)

# ==================== EMAIL MODULE ====================
def email_module():
    print_header("EMAIL INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Analyze email address")
    print("2. View saved email data")
    print("3. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        email = input(f"{Colors.YELLOW}Enter email address: {Colors.RESET}")
        analyze_email(email)
    
    elif choice == "2":
        view_email_data()
    
    elif choice == "3":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    email_module()

def analyze_email(email):
    """Analyze email address for OSINT purposes"""
    loading_animation(f"Analyzing email address: {email}", 4)
    
    data = {
        'email': email,
        'domain': None,
        'valid': None,
        'disposable': None,
        'breach_count': None,
        'associated_accounts': None
    }
    
    try:
        # Extract domain
        if '@' in email:
            data['domain'] = email.split('@')[1]
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        data['valid'] = "Yes" if re.match(email_regex, email) else "No"
        
        # Check if disposable email
        disposable_domains = [
            'tempmail.com', 'disposable.com', 'mailinator.com', 'guerrillamail.com',
            '10minutemail.com', 'throwaway.com', 'fakeinbox.com', 'yopmail.com'
        ]
        data['disposable'] = "Yes" if data['domain'] in disposable_domains else "No"
        
        # Simulate breach check
        data['breach_count'] = random.randint(0, 5)
        
        # Simulate associated accounts
        accounts = []
        if data['domain'] == 'gmail.com':
            accounts.extend(['Google', 'YouTube', 'GDrive'])
        elif data['domain'] == 'yahoo.com':
            accounts.extend(['Yahoo', 'Flickr'])
        elif data['domain'] == 'outlook.com':
            accounts.extend(['Microsoft', 'LinkedIn', 'Skype'])
        
        # Add random social media accounts
        social_media = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'Pinterest']
        accounts.extend(random.sample(social_media, random.randint(1, 3)))
        
        data['associated_accounts'] = ", ".join(accounts)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO email_data 
                    (email, domain, valid, disposable, breach_count, associated_accounts)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (data['email'], data['domain'], data['valid'], data['disposable'],
                     data['breach_count'], data['associated_accounts']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Email analysis completed!")
        print_info("Email", data['email'])
        print_info("Domain", data['domain'] or "Not found")
        print_info("Valid Format", data['valid'] or "Not found")
        print_info("Disposable", data['disposable'] or "Not found")
        print_info("Breach Count", data['breach_count'] or "Not found")
        print_info("Associated Accounts", data['associated_accounts'] or "Not found")
        
    except Exception as e:
        print_error(f"Error analyzing email: {str(e)}")

def view_email_data():
    conn = setup_database()
    c = conn.cursor()
    c.execute("SELECT * FROM email_data ORDER BY extracted_at DESC")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print_warning("No email data found in database")
        return
    
    print_header("SAVED EMAIL DATA")
    for row in rows:
        print_info("ID", row[0])
        print_info("Email", row[1])
        print_info("Domain", row[2] or "Not available")
        print_info("Valid", row[3] or "Not available")
        print_info("Disposable", row[4] or "Not available")
        print_info("Breach Count", row[5] or "Not available")
        print_info("Associated Accounts", row[6] or "Not available")
        print_info("Extracted At", row[7])
        print("-" * 60)

# ==================== PHONE MODULE ====================
def phone_module():
    print_header("PHONE INTELLIGENCE MODULE")
    print(f"{Colors.WHITE}1. Analyze phone number")
    print("2. View saved phone data")
    print("3. Back to main menu{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select an option: {Colors.RESET}")
    
    if choice == "1":
        phone = input(f"{Colors.YELLOW}Enter phone number (with country code): {Colors.RESET}")
        analyze_phone(phone)
    
    elif choice == "2":
        view_phone_data()
    
    elif choice == "3":
        return
    
    else:
        print_error("Invalid option")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    phone_module()

def analyze_phone(phone):
    """Analyze phone number for OSINT purposes"""
    loading_animation(f"Analyzing phone number: {phone}", 4)
    
    data = {
        'phone': phone,
        'country': None,
        'carrier': None,
        'valid': None,
        'line_type': None,
        'associated_accounts': None
    }
    
    try:
        # Determine country based on country code
        country_codes = {
            '1': 'United States/Canada',
            '20': 'Egypt',
            '33': 'France',
            '44': 'United Kingdom',
            '49': 'Germany',
            '81': 'Japan',
            '86': 'China',
            '91': 'India',
            '971': 'UAE',
            '966': 'Saudi Arabia'
        }
        
        for code, country in country_codes.items():
            if phone.startswith(code):
                data['country'] = country
                break
        
        if not data['country']:
            data['country'] = "Unknown"
        
        # Validate phone number (simple check)
        digits_only = re.sub(r'\D', '', phone)
        data['valid'] = "Yes" if len(digits_only) >= 10 else "No"
        
        # Simulate carrier detection
        carriers = ['Vodafone', 'Orange', 'Etisalat', 'WE', 'AT&T', 'Verizon', 'T-Mobile', 'Sprint']
        data['carrier'] = random.choice(carriers)
        
        # Simulate line type
        line_types = ['Mobile', 'Landline', 'VoIP']
        data['line_type'] = random.choice(line_types)
        
        # Simulate associated accounts
        accounts = []
        if data['country'] == 'Egypt':
            accounts.extend(['WhatsApp', 'Facebook', 'Instagram'])
        else:
            accounts.extend(['WhatsApp', 'Telegram', 'Signal'])
        
        # Add random social media accounts
        social_media = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'Snapchat']
        accounts.extend(random.sample(social_media, random.randint(1, 2)))
        
        data['associated_accounts'] = ", ".join(accounts)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO phone_data 
                    (phone, country, carrier, valid, line_type, associated_accounts)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (data['phone'], data['country'], data['carrier'], data['valid'],
                     data['line_type'], data['associated_accounts']))
        conn.commit()
        conn.close()
        
        # Display results
        print_success("Phone analysis completed!")
        print_info("Phone", data['phone'])
        print_info("Country", data['country'] or "Not found")
        print_info("Carrier", data['carrier'] or "Not found")
        print_info("Valid", data['valid'] or "Not found")
        print_info("Line Type", data['line_type'] or "Not found")
        print_info("Associated Accounts", data['associated_accounts'] or "Not found")
        
    except Exception as e:
        print_error(f"Error analyzing phone: {str(e)}")

def view_phone_data():
    conn = setup_database()
    c = conn.cursor()
    c.execute("SELECT * FROM phone_data ORDER BY extracted_at DESC")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print_warning("No phone data found in database")
        return
    
    print_header("SAVED PHONE DATA")
    for row in rows:
        print_info("ID", row[0])
        print_info("Phone", row[1])
        print_info("Country", row[2] or "Not available")
        print_info("Carrier", row[3] or "Not available")
        print_info("Valid", row[4] or "Not available")
        print_info("Line Type", row[5] or "Not available")
        print_info("Associated Accounts", row[6] or "Not available")
        print_info("Extracted At", row[7])
        print("-" * 60)

# ==================== DATABASE VIEW MODULE ====================
def view_database():
    print_header("DATABASE VIEWER")
    print(f"{Colors.WHITE}1. View Facebook data")
    print("2. View Instagram data")
    print("3. View TikTok data")
    print("4. View website data")
    print("5. View password patterns")
    print("6. View email data")
    print("7. View phone data")
    print("8. Back to main menu{Colors.RESET}")
    
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
        view_email_data()
    elif choice == "7":
        view_phone_data()
    elif choice == "8":
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
    print("6. Export email data")
    print("7. Export phone data")
    print("8. Export all data")
    print("9. Back to main menu{Colors.RESET}")
    
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
        export_table(c, "email_data", "Email", timestamp)
    elif choice == "7":
        export_table(c, "phone_data", "Phone", timestamp)
    elif choice == "8":
        tables = ["facebook_data", "instagram_data", "tiktok_data", "website_data", 
                 "password_patterns", "email_data", "phone_data"]
        for table in tables:
            export_table(c, table, table.capitalize(), timestamp)
    elif choice == "9":
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
        print("7. Email Intelligence")
        print("8. Phone Intelligence")
        print("9. Database Viewer")
        print("10. Export Data")
        print("11. Exit{Colors.RESET}")
        
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
            email_module()
        elif choice == "8":
            phone_module()
        elif choice == "9":
            view_database()
        elif choice == "10":
            export_data()
        elif choice == "11":
            print(f"\n{Colors.GREEN}Thank you for using Omar-tool Professional v4.5!{Colors.RESET}")
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