#!/usr/bin/env python3
"""
Process the existing downloaded Matthew Henry Commentary files
"""

import os
import json
import sqlite3
import csv
from bs4 import BeautifulSoup
import re

def extract_book_name_from_filename(filename):
    """Extract book name from filename"""
    book_mapping = {
        'Gen': 'Genesis', 'Ex': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers', 'Deu': 'Deuteronomy',
        'Jos': 'Joshua', 'Jud': 'Judges', 'Ru': 'Ruth', 'iSam': '1 Samuel', 'iiSam': '2 Samuel',
        'iKi': '1 Kings', 'iiKi': '2 Kings', 'iCh': '1 Chronicles', 'iiCh': '2 Chronicles',
        'Ez': 'Ezra', 'Neh': 'Nehemiah', 'Esth': 'Esther', 'Job': 'Job', 'Ps': 'Psalms',
        'Prov': 'Proverbs', 'Ec': 'Ecclesiastes', 'Song': 'Song of Solomon', 'Is': 'Isaiah',
        'Jer': 'Jeremiah', 'Lam': 'Lamentations', 'Ez': 'Ezekiel', 'Dan': 'Daniel',
        'Hos': 'Hosea', 'Joel': 'Joel', 'Amos': 'Amos', 'Obad': 'Obadiah', 'Jonah': 'Jonah',
        'Mic': 'Micah', 'Nah': 'Nahum', 'Hab': 'Habakkuk', 'Zeph': 'Zephaniah', 'Hag': 'Haggai',
        'Zech': 'Zechariah', 'Mal': 'Malachi', 'Matt': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke',
        'John': 'John', 'Acts': 'Acts', 'Rom': 'Romans', 'iCor': '1 Corinthians', 'iiCor': '2 Corinthians',
        'Gal': 'Galatians', 'Eph': 'Ephesians', 'Phi': 'Philippians', 'Col': 'Colossians',
        'iTh': '1 Thessalonians', 'iiTh': '2 Thessalonians', 'iTim': '1 Timothy', 'iiTim': '2 Timothy',
        'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews', 'Jam': 'James', 'iPet': '1 Peter',
        'iiPet': '2 Peter', 'iJo': '1 John', 'iiJo': '2 John', 'iiiJo': '3 John',
        'Ju': 'Jude', 'Rev': 'Revelation'
    }
    
    # Extract book abbreviation from filename like "mhc1.Gen.i.html"
    parts = filename.split('.')
    if len(parts) >= 2:
        book_abbr = parts[1]
        return book_mapping.get(book_abbr, book_abbr)
    
    return filename

def extract_commentary_from_html(filepath):
    """Extract commentary content from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the main content
    content_div = soup.find('div', class_='book-content')
    if not content_div:
        content_div = soup.find('div', id='theText')
    
    if not content_div:
        return None
    
    # Extract meaningful paragraphs
    paragraphs = []
    for p in content_div.find_all('p', class_='indent'):
        text = p.get_text().strip()
        if text and len(text) > 50:  # Only substantial paragraphs
            # Clean up text
            text = re.sub(r'\\s+', ' ', text)
            # Remove scripture references in brackets
            text = re.sub(r'\\([^)]*\\)', '', text)
            paragraphs.append(text)
    
    # If no indent paragraphs, try all paragraphs
    if not paragraphs:
        for p in content_div.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 50:
                text = re.sub(r'\\s+', ' ', text)
                text = re.sub(r'\\([^)]*\\)', '', text)
                paragraphs.append(text)
    
    return '\\n\\n'.join(paragraphs) if paragraphs else None

def process_downloaded_files():
    """Process all downloaded MHC files"""
    input_dir = "downloaded_mhc_commentary"
    
    if not os.path.exists(input_dir):
        print(f"Directory '{input_dir}' not found")
        return []
    
    commentaries = []
    
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.html'):
            filepath = os.path.join(input_dir, filename)
            
            book_name = extract_book_name_from_filename(filename)
            commentary_text = extract_commentary_from_html(filepath)
            
            if commentary_text and len(commentary_text) > 100:
                commentaries.append({
                    'book': book_name,
                    'commentary': commentary_text
                })
                print(f"Processed: {book_name} ({len(commentary_text)} chars)")
            else:
                print(f"Skipped: {filename} (no substantial content)")
    
    return commentaries

def create_output_files(commentaries):
    """Create output files in multiple formats"""
    if not commentaries:
        print("No commentaries to save")
        return
    
    # Create output directory
    output_dir = os.path.join("formats", "commentary")
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean existing files
    files_to_clean = ["MHC.db", "MHC.json", "MHC.csv", "MHC.txt"]
    for filename in files_to_clean:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    # JSON format
    json_file = os.path.join(output_dir, "MHC.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(commentaries, f, indent=2, ensure_ascii=False)
    print(f"Created: {json_file}")
    
    # SQLite database
    db_file = os.path.join(output_dir, "MHC.db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE mhc_books (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE mhc_commentary (
            id INTEGER PRIMARY KEY,
            book_id INTEGER,
            commentary TEXT,
            FOREIGN KEY (book_id) REFERENCES mhc_books (id)
        )
    ''')
    
    for i, commentary in enumerate(commentaries, 1):
        cursor.execute("INSERT INTO mhc_books (id, name) VALUES (?, ?)", 
                      (i, commentary['book']))
        cursor.execute("INSERT INTO mhc_commentary (book_id, commentary) VALUES (?, ?)", 
                      (i, commentary['commentary']))
    
    conn.commit()
    conn.close()
    print(f"Created: {db_file}")
    
    # CSV format
    csv_file = os.path.join(output_dir, "MHC.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['book', 'commentary'])
        for commentary in commentaries:
            writer.writerow([commentary['book'], commentary['commentary']])
    print(f"Created: {csv_file}")
    
    # Plain text format
    txt_file = os.path.join(output_dir, "MHC.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("Matthew Henry's Commentary on the Whole Bible\\n")
        f.write("=" * 60 + "\\n\\n")
        for commentary in commentaries:
            f.write(f"=== {commentary['book']} ===\\n\\n")
            f.write(commentary['commentary'])
            f.write("\\n\\n" + "=" * 60 + "\\n\\n")
    print(f"Created: {txt_file}")
    
    # README file
    readme_file = os.path.join(output_dir, "README.md")
    readme_content = '''# Matthew Henry's Commentary

This directory contains Matthew Henry's Commentary on the Whole Bible in multiple formats.

## About the Commentary

Matthew Henry's Commentary is one of the most widely used and respected Bible commentaries in the English language. It provides verse-by-verse exposition with practical applications for Christian living.

## Available Formats

- **MHC.json** - JSON format for programmatic access
- **MHC.db** - SQLite database with structured tables  
- **MHC.csv** - CSV format for spreadsheet applications
- **MHC.txt** - Plain text format for reading

## Database Schema (SQLite)

### Table: mhc_books
- `id` (INTEGER PRIMARY KEY) - Unique book identifier
- `name` (TEXT) - Name of the Bible book

### Table: mhc_commentary  
- `id` (INTEGER PRIMARY KEY) - Unique commentary entry identifier
- `book_id` (INTEGER) - Foreign key to mhc_books table
- `commentary` (TEXT) - The commentary text for the book

## Source

Processed from files downloaded from Christian Classics Ethereal Library (CCEL).

## License

This work is in the public domain.
'''
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"Created: {readme_file}")

def main():
    print("Processing Matthew Henry's Commentary files...")
    print("=" * 55)
    
    commentaries = process_downloaded_files()
    
    print(f"\\nProcessed {len(commentaries)} commentary books")
    
    if commentaries:
        create_output_files(commentaries)
        print(f"\\nFiles created in 'formats/commentary/' directory")
        
        # Show summary
        total_chars = sum(len(c['commentary']) for c in commentaries)
        print(f"Total commentary text: {total_chars:,} characters")
        
        print("\\n=== Books Processed ===")
        for commentary in commentaries:
            print(f"- {commentary['book']}")
    else:
        print("No commentary content was extracted")

if __name__ == "__main__":
    main()