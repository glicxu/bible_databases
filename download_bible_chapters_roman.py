#!/usr/bin/env python3
"""
Download all Bible chapters with Roman numeral naming for books and chapters.
"""

import json
import os
from pathlib import Path

def int_to_roman(num):
    """Convert integer to Roman numeral."""
    values = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    literals = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // values[i]):
            roman_num += literals[i]
            num -= values[i]
        i += 1
    return roman_num

def download_bible_chapters():
    """Download all Bible chapters using Roman numerals for naming."""
    
    # Path to the KJV JSON file
    kjv_path = Path("formats/json/KJV.json")
    
    if not kjv_path.exists():
        print(f"Error: {kjv_path} not found!")
        return
    
    # Create output directory
    output_dir = Path("bible_chapters_roman")
    output_dir.mkdir(exist_ok=True)
    
    # Load the KJV Bible data
    with open(kjv_path, 'r', encoding='utf-8') as f:
        bible_data = json.load(f)
    
    total_chapters = 0
    
    for book_idx, book in enumerate(bible_data['books'], 1):
        book_name = book['name']
        book_roman = int_to_roman(book_idx)
        
        print(f"Processing Book {book_roman}: {book_name}")
        
        # Create book directory
        book_dir = output_dir / f"Book_{book_roman}_{book_name.replace(' ', '_')}"
        book_dir.mkdir(exist_ok=True)
        
        for chapter in book['chapters']:
            chapter_num = chapter['chapter']
            chapter_roman = int_to_roman(chapter_num)
            
            # Create chapter file
            chapter_filename = f"Chapter_{chapter_roman}.txt"
            chapter_path = book_dir / chapter_filename
            
            # Write chapter content
            with open(chapter_path, 'w', encoding='utf-8') as f:
                f.write(f"Book {book_roman}: {book_name}\n")
                f.write(f"Chapter {chapter_roman}\n")
                f.write("=" * 50 + "\n\n")
                
                for verse in chapter['verses']:
                    verse_num = verse['verse']
                    verse_text = verse['text']
                    f.write(f"{verse_num}. {verse_text}\n\n")
            
            total_chapters += 1
            print(f"  Created Chapter {chapter_roman} ({chapter_num})")
    
    print(f"\nCompleted! Downloaded {total_chapters} chapters total.")
    print(f"Files saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    download_bible_chapters()