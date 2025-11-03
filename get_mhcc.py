#!/usr/bin/env python3
"""
Simple script to download and process Matthew Henry's Concise Commentary
from CCEL (Christian Classics Ethereal Library)
"""

import requests
import os
import json
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def download_mhcc():
    """Download Matthew Henry's Concise Commentary from CCEL"""
    base_url = "https://ccel.org/ccel/henry/mhcc/"
    index_url = base_url + "mhcc.i.html"
    
    print("Downloading MHCC index...")
    response = requests.get(index_url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all commentary links
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith('.html') and 'mhcc' in href and href != 'mhcc.i.html':
            links.append(urljoin(base_url, href))
    
    # Create output directory
    output_dir = "mhcc_files"
    os.makedirs(output_dir, exist_ok=True)
    
    # Download each file
    commentaries = []
    for i, url in enumerate(sorted(set(links)), 1):
        try:
            print(f"Downloading {i}/{len(set(links))}: {os.path.basename(url)}")
            response = requests.get(url)
            response.raise_for_status()
            
            # Extract content
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='book-content')
            
            if content_div:
                # Get book title
                title_elem = content_div.find('h2')
                book_title = title_elem.get_text().strip() if title_elem else f"Book_{i}"
                
                # Get commentary text
                paragraphs = []
                for p in content_div.find_all('p'):
                    text = p.get_text().strip()
                    if text and len(text) > 20:
                        text = re.sub(r'\s+', ' ', text)
                        paragraphs.append(text)
                
                commentary_text = '\n\n'.join(paragraphs)
                
                if commentary_text:
                    commentaries.append({
                        'book': book_title,
                        'commentary': commentary_text
                    })
                    
        except Exception as e:
            print(f"Error downloading {url}: {e}")
    
    return commentaries

def create_outputs(commentaries):
    """Create output files in multiple formats"""
    # Create formats directory
    formats_dir = os.path.join("formats", "commentary")
    os.makedirs(formats_dir, exist_ok=True)
    
    # JSON output
    json_file = os.path.join(formats_dir, "mhcc.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(commentaries, f, indent=2, ensure_ascii=False)
    print(f"Created: {json_file}")
    
    # SQLite database
    db_file = os.path.join(formats_dir, "mhcc.db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE mhcc_books (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE mhcc_commentary (
            id INTEGER PRIMARY KEY,
            book_id INTEGER,
            commentary TEXT,
            FOREIGN KEY (book_id) REFERENCES mhcc_books (id)
        )
    ''')
    
    for i, commentary in enumerate(commentaries, 1):
        cursor.execute("INSERT INTO mhcc_books (id, name) VALUES (?, ?)", 
                      (i, commentary['book']))
        cursor.execute("INSERT INTO mhcc_commentary (book_id, commentary) VALUES (?, ?)", 
                      (i, commentary['commentary']))
    
    conn.commit()
    conn.close()
    print(f"Created: {db_file}")
    
    # Plain text output
    txt_file = os.path.join(formats_dir, "mhcc.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        for commentary in commentaries:
            f.write(f"=== {commentary['book']} ===\n\n")
            f.write(commentary['commentary'])
            f.write("\n\n" + "="*60 + "\n\n")
    print(f"Created: {txt_file}")

def main():
    print("Matthew Henry's Concise Commentary Downloader")
    print("=" * 50)
    
    try:
        commentaries = download_mhcc()
        print(f"\nSuccessfully processed {len(commentaries)} books")
        
        if commentaries:
            create_outputs(commentaries)
            print(f"\nAll files created in 'formats/commentary/' directory")
        else:
            print("No commentary content found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()