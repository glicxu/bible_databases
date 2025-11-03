#!/usr/bin/env python3
"""
Download Matthew Henry's Concise Commentary chapter by chapter
"""

import requests
import os
import json
import sqlite3
from bs4 import BeautifulSoup
import re
import time

def get_book_info():
    """Get book information with chapter counts"""
    books = [
        ('Genesis', 'ii', 50), ('Exodus', 'iii', 40), ('Leviticus', 'iv', 27), 
        ('Numbers', 'v', 36), ('Deuteronomy', 'vi', 34), ('Joshua', 'vii', 24),
        ('Judges', 'viii', 21), ('Ruth', 'ix', 4), ('1 Samuel', 'x', 31),
        ('2 Samuel', 'xi', 24), ('1 Kings', 'xii', 22), ('2 Kings', 'xiii', 25),
        ('1 Chronicles', 'xiv', 29), ('2 Chronicles', 'xv', 36), ('Ezra', 'xvi', 10),
        ('Nehemiah', 'xvii', 13), ('Esther', 'xviii', 10), ('Job', 'xix', 42),
        ('Psalms', 'xx', 150), ('Proverbs', 'xxi', 31), ('Ecclesiastes', 'xxii', 12),
        ('Song of Solomon', 'xxiii', 8), ('Isaiah', 'xxiv', 66), ('Jeremiah', 'xxv', 52),
        ('Lamentations', 'xxvi', 5), ('Ezekiel', 'xxvii', 48), ('Daniel', 'xxviii', 12),
        ('Hosea', 'xxix', 14), ('Joel', 'xxx', 3), ('Amos', 'xxxi', 9),
        ('Obadiah', 'xxxii', 1), ('Jonah', 'xxxiii', 4), ('Micah', 'xxxiv', 7),
        ('Nahum', 'xxxv', 3), ('Habakkuk', 'xxxvi', 3), ('Zephaniah', 'xxxvii', 3),
        ('Haggai', 'xxxviii', 2), ('Zechariah', 'xxxix', 14), ('Malachi', 'xl', 4),
        ('Matthew', 'xli', 28), ('Mark', 'xlii', 16), ('Luke', 'xliii', 24),
        ('John', 'xliv', 21), ('Acts', 'xlv', 28), ('Romans', 'xlvi', 16),
        ('1 Corinthians', 'xlvii', 16), ('2 Corinthians', 'xlviii', 13),
        ('Galatians', 'xlix', 6), ('Ephesians', 'l', 6), ('Philippians', 'li', 4),
        ('Colossians', 'lii', 4), ('1 Thessalonians', 'liii', 5), 
        ('2 Thessalonians', 'liv', 3), ('1 Timothy', 'lv', 6), ('2 Timothy', 'lvi', 4),
        ('Titus', 'lvii', 3), ('Philemon', 'lviii', 1), ('Hebrews', 'lix', 13),
        ('James', 'lx', 5), ('1 Peter', 'lxi', 5), ('2 Peter', 'lxii', 3),
        ('1 John', 'lxiii', 5), ('2 John', 'lxiv', 1), ('3 John', 'lxv', 1),
        ('Jude', 'lxvi', 1), ('Revelation', 'lxvii', 22)
    ]
    return books

def roman_to_int(roman):
    """Convert roman numeral to integer for chapter numbers"""
    values = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10,
              'xi': 11, 'xii': 12, 'xiii': 13, 'xiv': 14, 'xv': 15, 'xvi': 16, 'xvii': 17, 'xviii': 18, 'xix': 19, 'xx': 20,
              'xxi': 21, 'xxii': 22, 'xxiii': 23, 'xxiv': 24, 'xxv': 25, 'xxvi': 26, 'xxvii': 27, 'xxviii': 28, 'xxix': 29, 'xxx': 30}
    return values.get(roman, 0)

def int_to_roman(num):
    """Convert integer to roman numeral"""
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i']
    result = ''
    for i, value in enumerate(values):
        count = num // value
        result += numerals[i] * count
        num -= value * count
    return result

def download_chapter(book_roman, chapter_num):
    """Download a single chapter commentary"""
    chapter_roman = int_to_roman(chapter_num)
    url = f"https://ccel.org/ccel/henry/mhcc/mhcc.{book_roman}.{chapter_roman}.html"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='book-content')
            
            if content_div:
                paragraphs = []
                for p in content_div.find_all('p'):
                    text = p.get_text().strip()
                    if text and len(text) > 20:
                        text = re.sub(r'\s+', ' ', text)
                        paragraphs.append(text)
                
                return '\n\n'.join(paragraphs) if paragraphs else None
        
        return None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def main():
    """Download all chapter commentaries"""
    books = get_book_info()
    all_commentaries = []
    
    print("Downloading Matthew Henry's Concise Commentary by chapters...")
    
    for book_name, book_roman, chapter_count in books[:5]:  # Start with first 5 books
        print(f"\nProcessing {book_name} ({chapter_count} chapters)...")
        
        for chapter in range(1, min(chapter_count + 1, 11)):  # Limit to first 10 chapters per book
            print(f"  Chapter {chapter}...", end='')
            
            commentary = download_chapter(book_roman, chapter)
            if commentary:
                all_commentaries.append({
                    'book': book_name,
                    'chapter': chapter,
                    'commentary': commentary
                })
                print(" OK")
            else:
                print(" FAILED")
            
            time.sleep(0.5)  # Be respectful to the server
    
    # Save results
    if all_commentaries:
        output_dir = "commentary/mhcc_chapters"
        os.makedirs(output_dir, exist_ok=True)
        
        # JSON format
        with open(f"{output_dir}/mhcc_chapters.json", 'w', encoding='utf-8') as f:
            json.dump(all_commentaries, f, indent=2, ensure_ascii=False)
        
        # SQLite database
        conn = sqlite3.connect(f"{output_dir}/mhcc_chapters.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE mhcc_chapters (
                id INTEGER PRIMARY KEY,
                book TEXT NOT NULL,
                chapter INTEGER NOT NULL,
                commentary TEXT
            )
        ''')
        
        for entry in all_commentaries:
            cursor.execute(
                "INSERT INTO mhcc_chapters (book, chapter, commentary) VALUES (?, ?, ?)",
                (entry['book'], entry['chapter'], entry['commentary'])
            )
        
        conn.commit()
        conn.close()
        
        print(f"\nDownloaded {len(all_commentaries)} chapter commentaries")
        print(f"Files saved in {output_dir}/")
    else:
        print("No commentaries downloaded")

if __name__ == "__main__":
    main()