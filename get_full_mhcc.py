#!/usr/bin/env python3
"""
Download Matthew Henry's Concise Commentary from CCEL
This version targets the complete commentary structure
"""

import requests
import os
import json
import sqlite3
from bs4 import BeautifulSoup
import re

def get_mhcc_book_urls():
    """Get all book URLs for Matthew Henry's Concise Commentary"""
    # These are the direct URLs to each book's commentary
    book_urls = [
        # Old Testament
        "https://ccel.org/ccel/henry/mhcc/mhcc.Gen.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Exod.html", 
        "https://ccel.org/ccel/henry/mhcc/mhcc.Lev.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Num.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Deut.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Josh.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Judg.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Ruth.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iSam.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiSam.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iKgs.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiKgs.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iChr.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiChr.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Ezra.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Neh.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Esth.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Job.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Ps.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Prov.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Eccl.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Song.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Isa.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Jer.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Lam.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Ezek.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Dan.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Hos.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Joel.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Amos.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Obad.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Jonah.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Mic.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Nah.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Hab.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Zeph.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Hag.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Zech.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Mal.html",
        # New Testament
        "https://ccel.org/ccel/henry/mhcc/mhcc.Matt.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Mark.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Luke.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.John.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Acts.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Rom.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iCor.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiCor.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Gal.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Eph.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Phil.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Col.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iTh.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiTh.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iTim.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiTim.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Titus.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Phlm.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Heb.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Jas.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iPet.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiPet.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iJohn.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiJohn.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.iiiJohn.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Jude.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.Rev.html"
    ]
    return book_urls

def extract_book_name(url):
    """Extract book name from URL"""
    book_mapping = {
        'Gen': 'Genesis', 'Exod': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers', 'Deut': 'Deuteronomy',
        'Josh': 'Joshua', 'Judg': 'Judges', 'Ruth': 'Ruth', 'iSam': '1 Samuel', 'iiSam': '2 Samuel',
        'iKgs': '1 Kings', 'iiKgs': '2 Kings', 'iChr': '1 Chronicles', 'iiChr': '2 Chronicles',
        'Ezra': 'Ezra', 'Neh': 'Nehemiah', 'Esth': 'Esther', 'Job': 'Job', 'Ps': 'Psalms',
        'Prov': 'Proverbs', 'Eccl': 'Ecclesiastes', 'Song': 'Song of Solomon', 'Isa': 'Isaiah',
        'Jer': 'Jeremiah', 'Lam': 'Lamentations', 'Ezek': 'Ezekiel', 'Dan': 'Daniel',
        'Hos': 'Hosea', 'Joel': 'Joel', 'Amos': 'Amos', 'Obad': 'Obadiah', 'Jonah': 'Jonah',
        'Mic': 'Micah', 'Nah': 'Nahum', 'Hab': 'Habakkuk', 'Zeph': 'Zephaniah', 'Hag': 'Haggai',
        'Zech': 'Zechariah', 'Mal': 'Malachi', 'Matt': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke',
        'John': 'John', 'Acts': 'Acts', 'Rom': 'Romans', 'iCor': '1 Corinthians', 'iiCor': '2 Corinthians',
        'Gal': 'Galatians', 'Eph': 'Ephesians', 'Phil': 'Philippians', 'Col': 'Colossians',
        'iTh': '1 Thessalonians', 'iiTh': '2 Thessalonians', 'iTim': '1 Timothy', 'iiTim': '2 Timothy',
        'Titus': 'Titus', 'Phlm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James', 'iPet': '1 Peter',
        'iiPet': '2 Peter', 'iJohn': '1 John', 'iiJohn': '2 John', 'iiiJohn': '3 John',
        'Jude': 'Jude', 'Rev': 'Revelation'
    }
    
    # Extract book abbreviation from URL
    book_abbr = url.split('.')[-2]  # Get part before .html
    return book_mapping.get(book_abbr, book_abbr)

def download_commentary(url):
    """Download and extract commentary from a single URL"""
    try:
        print(f"Downloading: {extract_book_name(url)}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main content
        content_div = soup.find('div', class_='book-content')
        if not content_div:
            # Try alternative selectors
            content_div = soup.find('div', id='theText')
        
        if content_div:
            # Extract all text content
            paragraphs = []
            for p in content_div.find_all(['p', 'div']):
                text = p.get_text().strip()
                if text and len(text) > 30:  # Filter short paragraphs
                    # Clean up text
                    text = re.sub(r'\s+', ' ', text)
                    text = re.sub(r'^\d+\.\s*', '', text)  # Remove leading numbers
                    paragraphs.append(text)
            
            commentary_text = '\n\n'.join(paragraphs)
            
            return {
                'book': extract_book_name(url),
                'commentary': commentary_text
            }
    
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def create_database_files(commentaries):
    """Create output files in multiple formats"""
    # Create output directory
    output_dir = os.path.join("formats", "commentary")
    os.makedirs(output_dir, exist_ok=True)
    
    # JSON format
    json_file = os.path.join(output_dir, "MHCC.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(commentaries, f, indent=2, ensure_ascii=False)
    print(f"Created: {json_file}")
    
    # SQLite database
    db_file = os.path.join(output_dir, "MHCC.db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create tables following the project schema
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
    
    # CSV format
    import csv
    csv_file = os.path.join(output_dir, "MHCC.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['book', 'commentary'])
        for commentary in commentaries:
            writer.writerow([commentary['book'], commentary['commentary']])
    print(f"Created: {csv_file}")

def main():
    print("Matthew Henry's Concise Commentary Downloader")
    print("=" * 55)
    
    book_urls = get_mhcc_book_urls()
    commentaries = []
    
    for url in book_urls:
        commentary = download_commentary(url)
        if commentary and commentary['commentary']:
            commentaries.append(commentary)
    
    print(f"\nSuccessfully downloaded {len(commentaries)} books")
    
    if commentaries:
        create_database_files(commentaries)
        print(f"\nFiles created in 'formats/commentary/' directory")
        print("Available formats: JSON, SQLite, CSV")
    else:
        print("No commentary content was successfully downloaded")

if __name__ == "__main__":
    main()