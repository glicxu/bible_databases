#!/usr/bin/env python3
"""
Download the complete Matthew Henry's Concise Commentary from CCEL
"""

import requests
import os
import json
import sqlite3
import csv
from bs4 import BeautifulSoup
import re

def download_full_commentary():
    """Download the complete commentary from the main content page"""
    url = "https://ccel.org/ccel/henry/mhcc/mhcc.ii.html"
    
    print("Downloading Matthew Henry's Concise Commentary...")
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the main content
    content_div = soup.find('div', id='theText')
    if not content_div:
        content_div = soup.find('div', class_='book-content')
    
    if not content_div:
        print("Could not find main content div")
        return []
    
    print(f"Found content div with {len(content_div.find_all('p'))} paragraphs")
    
    # Extract commentary by books
    commentaries = []
    current_book = None
    current_content = []
    
    # Bible book names to look for
    bible_books = [
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
        'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', 
        '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
        'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs',
        'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah',
        'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
        'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
        'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans',
        '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
        'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
        'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
        'Jude', 'Revelation'
    ]
    
    # Process all elements in the content
    for element in content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'div']):
        text = element.get_text().strip()
        
        if not text or len(text) < 10:
            continue
        
        # Check if this is a book title
        is_book_title = False
        for book in bible_books:
            if book.lower() in text.lower() and len(text) < 100:
                # This looks like a book title
                if current_book and current_content:
                    # Save previous book
                    commentary_text = '\n\n'.join(current_content)
                    if len(commentary_text) > 100:  # Only save if substantial content
                        commentaries.append({
                            'book': current_book,
                            'commentary': commentary_text
                        })
                        print(f"Extracted: {current_book} ({len(commentary_text)} chars)")
                
                current_book = book
                current_content = []
                is_book_title = True
                break
        
        if not is_book_title and current_book:
            # Add content to current book
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'^\d+\.\s*', '', text)  # Remove leading numbers
            if len(text) > 30:  # Only add substantial paragraphs
                current_content.append(text)
    
    # Don't forget the last book
    if current_book and current_content:
        commentary_text = '\n\n'.join(current_content)
        if len(commentary_text) > 100:
            commentaries.append({
                'book': current_book,
                'commentary': commentary_text
            })
            print(f"Extracted: {current_book} ({len(commentary_text)} chars)")
    
    return commentaries

def download_toc_based():
    """Alternative approach: download from table of contents"""
    url = "https://ccel.org/ccel/henry/mhcc/mhcc.toc.html"
    
    print("Downloading from table of contents...")
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', id='theText')
    
    if not content_div:
        print("Could not find theText div")
        return []
    
    # Extract all text content
    all_text = []
    for p in content_div.find_all('p'):
        text = p.get_text().strip()
        if text and len(text) > 20:
            text = re.sub(r'\s+', ' ', text)
            all_text.append(text)
    
    # Join all text and try to split by books
    full_text = '\n\n'.join(all_text)
    
    # Simple approach: create one large commentary file
    return [{
        'book': 'Complete Commentary',
        'commentary': full_text
    }]

def create_output_files(commentaries):
    """Create output files in multiple formats"""
    if not commentaries:
        print("No commentaries to save")
        return
    
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
    csv_file = os.path.join(output_dir, "MHCC.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['book', 'commentary'])
        for commentary in commentaries:
            writer.writerow([commentary['book'], commentary['commentary']])
    print(f"Created: {csv_file}")
    
    # Plain text format
    txt_file = os.path.join(output_dir, "MHCC.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("Matthew Henry's Concise Commentary on the Bible\n")
        f.write("=" * 60 + "\n\n")
        for commentary in commentaries:
            f.write(f"=== {commentary['book']} ===\n\n")
            f.write(commentary['commentary'])
            f.write("\n\n" + "=" * 60 + "\n\n")
    print(f"Created: {txt_file}")

def main():
    print("Matthew Henry's Concise Commentary Downloader")
    print("=" * 55)
    
    # Try the main content approach first
    commentaries = download_full_commentary()
    
    # If that doesn't work well, try the TOC approach
    if len(commentaries) < 10:  # If we didn't get many books
        print("\nTrying alternative approach...")
        commentaries = download_toc_based()
    
    print(f"\nExtracted {len(commentaries)} commentary sections")
    
    if commentaries:
        create_output_files(commentaries)
        print(f"\nFiles created in 'formats/commentary/' directory")
        
        # Show summary
        total_chars = sum(len(c['commentary']) for c in commentaries)
        print(f"Total commentary text: {total_chars:,} characters")
    else:
        print("No commentary content was extracted")

if __name__ == "__main__":
    main()