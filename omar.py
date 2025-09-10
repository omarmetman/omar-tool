#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Omar-tool Professional v4.0 - Ultimate OSINT & Social Media Intelligence Tool
# Author: Omar M. Etman

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
    
    # Background colors
    BG_BLUE = "\033[48;5;17m"
    BG_DARK = "\033[48;5;233m"
    BG_GRAY = "\033[48;5;236m"

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
    
    # Create tables for different social media platforms
    c.execute('''CREATE TABLE IF NOT EXISTS facebook_profiles
                 (id INTEGER PRIMARY KEY, username TEXT, name TEXT, profile_url TEXT, 
                 location TEXT, join_date TEXT, friends_count INTEGER, extracted_data TEXT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS instagram_profiles
                 (id INTEGER PRIMARY KEY, username TEXT, full_name TEXT, profile_url TEXT, 
                 followers INTEGER, following INTEGER, posts_count INTEGER, bio TEXT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tiktok_profiles
                 (id INTEGER PRIMARY KEY, username TEXT, nickname TEXT, profile_url TEXT, 
                 followers INTEGER, following INTEGER, likes_count INTEGER, bio TEXT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS website_data
                 (id INTEGER PRIMARY KEY, url TEXT, title TEXT, ip_address TEXT, 
                 server_info TEXT, technologies TEXT, emails TEXT, phones TEXT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS password_patterns
                 (id INTEGER PRIMARY KEY, platform TEXT, username TEXT, pattern TEXT,
                 generated_password TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    return conn

# ==================== FACEBOOK MODULE ====================
def facebook_module():
    print_header("FACEBOOK INTELLIGENCE MODULE")
    
    url = input(f"{Colors.CYAN}Enter Facebook URL/Username: {Colors.RESET}").strip()
    if not url:
        print_error("No URL provided")
        return
    
    print_section("Gathering Facebook Intelligence")
    loading_animation("Analyzing profile", 3)
    
    # Extract username from URL
    username = extract_facebook_username(url)
    if not username:
        print_error("Could not extract username from URL")
        return
    
    print_info("Username", username)
    
    # Get real Facebook data using various techniques
    profile_data = get_facebook_data(username)
    
    if profile_data:
        print_section("Profile Information")
        for key, value in profile_data.items():
            if value:  # Only print if value exists
                print_info(key.capitalize().replace('_', ' '), value)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO facebook_profiles 
                    (username, name, profile_url, location, join_date, friends_count, extracted_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (username, profile_data.get('name'), url, profile_data.get('location'),
                  profile_data.get('join_date'), profile_data.get('friends_count'),
                  json.dumps(profile_data)))
        conn.commit()
        conn.close()
        
        print_success("Facebook data saved to database")
    else:
        print_error("Could not retrieve Facebook data")
    
    # Password guessing simulation (for educational purposes only)
    print_section("Common Password Patterns (Educational)")
    common_passwords = guess_common_passwords(username, "facebook")
    for pwd in common_passwords[:5]:  # Show only first 5
        print_bullet(f"Possible pattern: {pwd}")
    
    print_success("Facebook intelligence gathering completed")

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
    
    # If no match, assume it's already a username
    return url

def get_facebook_data(username):
    """
    Get real Facebook data using various OSINT techniques
    """
    data = {}
    
    try:
        # Try to get data from Facebook's public information
        headers = get_random_headers()
        response = requests.get(f"https://www.facebook.com/{username}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Extract basic information from HTML
            html_content = response.text
            
            # Name extraction
            name_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE)
            if name_match:
                data['name'] = name_match.group(1).replace('| Facebook', '').strip()
            
            # Location extraction
            location_match = re.search(r'Lives in[^<]*<[^>]*>([^<]+)</', html_content, re.IGNORECASE)
            if location_match:
                data['location'] = location_match.group(1).strip()
            
            # Join date extraction
            join_match = re.search(r'Joined[^<]*<[^>]*>([^<]+)</', html_content, re.IGNORECASE)
            if join_match:
                data['join_date'] = join_match.group(1).strip()
            
            # Friends count extraction
            friends_match = re.search(r'(\d+)[^<]*friends', html_content, re.IGNORECASE)
            if friends_match:
                data['friends_count'] = friends_match.group(1)
        
        return data
        
    except Exception as e:
        print_error(f"Error retrieving Facebook data: {e}")
        return None

# ==================== INSTAGRAM MODULE ====================
def instagram_module():
    print_header("INSTAGRAM INTELLIGENCE MODULE")
    
    url = input(f"{Colors.CYAN}Enter Instagram URL/Username: {Colors.RESET}").strip()
    if not url:
        print_error("No URL provided")
        return
    
    print_section("Gathering Instagram Intelligence")
    loading_animation("Analyzing profile", 3)
    
    username = extract_instagram_username(url)
    if not username:
        print_error("Could not extract username from URL")
        return
    
    print_info("Username", username)
    
    # Get real Instagram data
    profile_data = get_instagram_data(username)
    
    if profile_data:
        print_section("Profile Information")
        for key, value in profile_data.items():
            if value:
                print_info(key.capitalize().replace('_', ' '), value)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO instagram_profiles 
                    (username, full_name, profile_url, followers, following, posts_count, bio)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (username, profile_data.get('full_name'), url, profile_data.get('followers'),
                  profile_data.get('following'), profile_data.get('posts_count'),
                  profile_data.get('bio')))
        conn.commit()
        conn.close()
        
        print_success("Instagram data saved to database")
    else:
        print_error("Could not retrieve Instagram data")
    
    # Password guessing
    print_section("Common Password Patterns (Educational)")
    common_passwords = guess_common_passwords(username, "instagram")
    for pwd in common_passwords[:5]:
        print_bullet(f"Possible pattern: {pwd}")
    
    print_success("Instagram intelligence gathering completed")

def extract_instagram_username(url):
    patterns = [
        r'instagram\.com/([^/?]+)',
        r'instagr\.am/([^/?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return url

def get_instagram_data(username):
    """
    Get real Instagram data using various techniques
    """
    data = {}
    
    try:
        headers = get_random_headers()
        response = requests.get(f"https://www.instagram.com/{username}/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Extract JSON data from script tags
            json_match = re.search(r'window\._sharedData\s*=\s*({.*?});</script>', html_content, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group(1))
                user_data = json_data.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user', {})
                
                if user_data:
                    data['full_name'] = user_data.get('full_name', '')
                    data['followers'] = user_data.get('edge_followed_by', {}).get('count', '')
                    data['following'] = user_data.get('edge_follow', {}).get('count', '')
                    data['posts_count'] = user_data.get('edge_owner_to_timeline_media', {}).get('count', '')
                    data['bio'] = user_data.get('biography', '')
        
        return data
        
    except Exception as e:
        print_error(f"Error retrieving Instagram data: {e}")
        return None

# ==================== TIKTOK MODULE ====================
def tiktok_module():
    print_header("TIKTOK INTELLIGENCE MODULE")
    
    url = input(f"{Colors.CYAN}Enter TikTok URL/Username: {Colors.RESET}").strip()
    if not url:
        print_error("No URL provided")
        return
    
    print_section("Gathering TikTok Intelligence")
    loading_animation("Analyzing profile", 3)
    
    username = extract_tiktok_username(url)
    if not username:
        print_error("Could not extract username from URL")
        return
    
    print_info("Username", username)
    
    # Get real TikTok data
    profile_data = get_tiktok_data(username)
    
    if profile_data:
        print_section("Profile Information")
        for key, value in profile_data.items():
            if value:
                print_info(key.capitalize().replace('_', ' '), value)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO tiktok_profiles 
                    (username, nickname, profile_url, followers, following, likes_count, bio)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (username, profile_data.get('nickname'), url, profile_data.get('followers'),
                  profile_data.get('following'), profile_data.get('likes_count'),
                  profile_data.get('bio')))
        conn.commit()
        conn.close()
        
        print_success("TikTok data saved to database")
    else:
        print_error("Could not retrieve TikTok data")
    
    # Password guessing
    print_section("Common Password Patterns (Educational)")
    common_passwords = guess_common_passwords(username, "tiktok")
    for pwd in common_passwords[:5]:
        print_bullet(f"Possible pattern: {pwd}")
    
    print_success("TikTok intelligence gathering completed")

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
    
    return url

def get_tiktok_data(username):
    """
    Get real TikTok data using various techniques
    """
    data = {}
    
    try:
        headers = get_random_headers()
        response = requests.get(f"https://www.tiktok.com/@{username}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Extract JSON data from script tags
            json_match = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', html_content, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group(1))
                user_data = json_data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail', {}).get('userInfo', {}).get('user', {})
                
                if user_data:
                    data['nickname'] = user_data.get('nickname', '')
                    data['followers'] = user_data.get('followerCount', '')
                    data['following'] = user_data.get('followingCount', '')
                    data['likes_count'] = user_data.get('heartCount', '')
                    data['bio'] = user_data.get('signature', '')
        
        return data
        
    except Exception as e:
        print_error(f"Error retrieving TikTok data: {e}")
        return None

# ==================== WEBSITE MODULE ====================
def website_module():
    print_header("WEBSITE INTELLIGENCE MODULE")
    
    url = input(f"{Colors.CYAN}Enter Website URL: {Colors.RESET}").strip()
    if not url:
        print_error("No URL provided")
        return
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    print_section("Gathering Website Intelligence")
    loading_animation("Analyzing website", 3)
    
    # Get website data
    website_data = get_website_info(url)
    
    if website_data:
        print_section("Website Information")
        for key, value in website_data.items():
            if value:
                print_info(key.capitalize().replace('_', ' '), value)
        
        # Save to database
        conn = setup_database()
        c = conn.cursor()
        c.execute('''INSERT INTO website_data 
                    (url, title, ip_address, server_info, technologies, emails, phones)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (url, website_data.get('title'), website_data.get('ip_address'),
                  website_data.get('server_info'), website_data.get('technologies'),
                  website_data.get('emails'), website_data.get('phones')))
        conn.commit()
        conn.close()
        
        print_success("Website data saved to database")
    else:
        print_error("Could not retrieve website data")
    
    print_success("Website intelligence gathering completed")

def get_website_info(url):
    """
    Get comprehensive website information
    """
    data = {}
    
    try:
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE)
            if title_match:
                data['title'] = title_match.group(1).strip()
            
            # Extract IP address
            domain = urlparse(url).netloc
            try:
                ip = socket.gethostbyname(domain)
                data['ip_address'] = ip
            except:
                data['ip_address'] = "Unknown"
            
            # Extract server information
            data['server_info'] = response.headers.get('Server', 'Unknown')
            
            # Extract technologies
            technologies = detect_technologies(html_content, response.headers)
            data['technologies'] = ', '.join(technologies) if technologies else 'Unknown'
            
            # Extract emails
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html_content)
            data['emails'] = ', '.join(set(emails)) if emails else 'None found'
            
            # Extract phone numbers
            phones = re.findall(r'\+?[0-9][\d\s\-\(\)]{7,}[\d]', html_content)
            data['phones'] = ', '.join(set(phones)) if phones else 'None found'
        
        return data
        
    except Exception as e:
        print_error(f"Error retrieving website data: {e}")
        return None

def detect_technologies(html_content, headers):
    """
    Detect web technologies used by the website
    """
    technologies = []
    
    # Check for common frameworks
    if re.search(r'wp-content|wp-includes', html_content, re.IGNORECASE):
        technologies.append('WordPress')
    
    if re.search(r'jquery', html_content, re.IGNORECASE):
        technologies.append('jQuery')
    
    if re.search(r'bootstrap', html_content, re.IGNORECASE):
        technologies.append('Bootstrap')
    
    # Check server headers
    server = headers.get('Server', '').lower()
    if 'apache' in server:
        technologies.append('Apache')
    elif 'nginx' in server:
        technologies.append('Nginx')
    elif 'iis' in server:
        technologies.append('IIS')
    
    return technologies

# ==================== SNAPCHAT MODULE ====================
def snapchat_module():
    print_header("SNAPCHAT INTELLIGENCE MODULE")
    
    username = input(f"{Colors.CYAN}Enter Snapchat Username: {Colors.RESET}").strip()
    if not username:
        print_error("No username provided")
        return
    
    print_section("Gathering Snapchat Intelligence")
    loading_animation("Analyzing profile", 3)
    
    print_info("Username", username)
    
    # Get Snapchat data (limited due to API restrictions)
    profile_data = get_snapchat_data(username)
    
    if profile_data:
        print_section("Profile Information")
        for key, value in profile_data.items():
            if value:
                print_info(key.capitalize().replace('_', ' '), value)
    else:
        print_warning("Limited public data available for Snapchat profiles")
    
    # Password guessing
    print_section("Common Password Patterns (Educational)")
    common_passwords = guess_common_passwords(username, "snapchat")
    for pwd in common_passwords[:5]:
        print_bullet(f"Possible pattern: {pwd}")
    
    print_success("Snapchat intelligence gathering completed")

def get_snapchat_data(username):
    """
    Get limited Snapchat data (Snapchat has strict privacy policies)
    """
    data = {}
    
    # Very limited public information available for Snapchat
    data['username'] = username
    data['platform'] = 'Snapchat'
    
    return data

# ==================== PASSWORD GUESSING MODULE ====================
def guess_common_passwords(username, platform):
    """
    Generate common password patterns based on username and platform
    FOR EDUCATIONAL PURPOSES ONLY
    """
    patterns = []
    
    # Basic patterns
    patterns.extend([
        username,
        username + "123",
        username + "1234",
        username + "12345",
        username + "!",
        username + "@",
        username + "#",
    ])
    
    # Platform-specific patterns
    if platform == "facebook":
        patterns.extend([
            username + "fb",
            username + "facebook",
            "fb" + username,
        ])
    elif platform == "instagram":
        patterns.extend([
            username + "ig",
            username + "insta",
            "ig" + username,
        ])
    elif platform == "tiktok":
        patterns.extend([
            username + "tt",
            username + "tiktok",
            "tt" + username,
        ])
    
    # Common password patterns
    common = ["password", "123456", "qwerty", "admin", "welcome", "monkey", "sunshine", "password1"]
    patterns.extend(common)
    
    # Save patterns to database for educational purposes
    conn = setup_database()
    c = conn.cursor()
    for pattern in patterns[:10]:  # Save only first 10
        c.execute('''INSERT INTO password_patterns (platform, username, pattern, generated_password)
                     VALUES (?, ?, ?, ?)''', (platform, username, pattern, pattern))
    conn.commit()
    conn.close()
    
    return patterns

# ==================== DATABASE VIEW MODULE ====================
def view_database():
    print_header("DATABASE VIEWER")
    
    conn = setup_database()
    c = conn.cursor()
    
    tables = {
        '1': 'facebook_profiles',
        '2': 'instagram_profiles',
        '3': 'tiktok_profiles',
        '4': 'website_data',
        '5': 'password_patterns'
    }
    
    print_section("Select Table to View")
    for key, table in tables.items():
        print(f"{Colors.CYAN}{key}. {table}{Colors.RESET}")
    
    choice = input(f"{Colors.CYAN}Enter choice: {Colors.RESET}").strip()
    
    if choice in tables:
        table_name = tables[choice]
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = c.fetchone()[0]
        
        print_info("Total Records", count)
        
        if count > 0:
            c.execute(f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT 5")
            rows = c.fetchall()
            
            print_section(f"Recent Records from {table_name}")
            for row in rows:
                print(f"{Colors.GRAY}{row}{Colors.RESET}")
        else:
            print_warning("No records found in this table")
    else:
        print_error("Invalid choice")
    
    conn.close()

# ==================== EXPORT DATA MODULE ====================
def export_data():
    print_header("DATA EXPORT")
    
    conn = setup_database()
    c = conn.cursor()
    
    tables = {
        '1': 'facebook_profiles',
        '2': 'instagram_profiles',
        '3': 'tiktok_profiles',
        '4': 'website_data',
        '5': 'password_patterns',
        '6': 'all'
    }
    
    print_section("Select Data to Export")
    for key, table in tables.items():
        print(f"{Colors.CYAN}{key}. {table}{Colors.RESET}")
    
    choice = input(f"{Colors.CYAN}Enter choice: {Colors.RESET}").strip()
    format_choice = input(f"{Colors.CYAN}Format (csv/json): {Colors.RESET}").strip().lower()
    
    if choice in tables and format_choice in ['csv', 'json']:
        table_name = tables[choice]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if table_name == 'all':
            for t in ['facebook_profiles', 'instagram_profiles', 'tiktok_profiles', 'website_data', 'password_patterns']:
                export_table(c, t, format_choice, timestamp)
        else:
            export_table(c, table_name, format_choice, timestamp)
        
        print_success("Data exported successfully")
    else:
        print_error("Invalid choice")
    
    conn.close()

def export_table(cursor, table_name, format_type, timestamp):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    if format_type == 'csv':
        filename = f"{table_name}_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(rows)
    elif format_type == 'json':
        filename = f"{table_name}_{timestamp}.json"
        data = []
        for row in rows:
            data.append(dict(zip(column_names, row)))
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)

# ==================== MAIN MENU ====================
def main_menu():
    conn = setup_database()  # Initialize database
    conn.close()
    
    while True:
        mobile_banner()
        
        print(f"{Colors.BOLD}Select Intelligence Module:{Colors.RESET}")
        print(f"{Colors.CYAN} 1.{Colors.RESET} Facebook OSINT")
        print(f"{Colors.CYAN} 2.{Colors.RESET} Instagram OSINT")
        print(f"{Colors.CYAN} 3.{Colors.RESET} TikTok OSINT")
        print(f"{Colors.CYAN} 4.{Colors.RESET} Website Intelligence")
        print(f"{Colors.CYAN} 5.{Colors.RESET} Snapchat OSINT")
        print(f"{Colors.CYAN} 6.{Colors.RESET} View Collected Data")
        print(f"{Colors.CYAN} 7.{Colors.RESET} Export Data")
        print(f"{Colors.CYAN} 0.{Colors.RESET} Exit")
        print()
        
        choice = input(f"{Colors.WHITE}Enter your choice: {Colors.RESET}")
        
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
            view_database()
        elif choice == "7":
            export_data()
        elif choice == "0":
            print_success("Thank you for using Omar-tool Professional v4.0!")
            break
        else:
            print_error("Invalid choice. Please try again.")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Tool terminated by user{Colors.RESET}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")