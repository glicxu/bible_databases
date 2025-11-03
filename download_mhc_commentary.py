#!/usr/bin/env python3
"""
Download Matthew Henry Commentary from CCEL using Roman numerals.
URL pattern: https://ccel.org/ccel/henry/mhcc/mhcc.{x}.{y}.html
where x is book (2-77) and y is chapter, both in Roman numerals.
"""

import requests
import os
from pathlib import Path
import time

def int_to_roman(num):
    """Convert integer to Roman numeral."""
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    literals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // values[i]):
            roman_num += literals[i]
            num -= values[i]
        i += 1
    return roman_num

def download_mhc_commentary():
    """Download MHC commentary from CCEL."""
    
    # Create output directory
    output_dir = Path("mhc_commentary_roman")
    output_dir.mkdir(exist_ok=True)
    
    # Bible book chapter counts (standard 66 books)
    chapter_counts = [
        50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31,
        12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21,
        28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22
    ]
    
    total_downloaded = 0
    
    for book_idx in range(66):
        book_num = book_idx + 2  # Books start from 2
        book_roman = int_to_roman(book_num)
        chapter_count = chapter_counts[book_idx]
        
        print(f"Processing Book {book_roman} ({book_num}) - {chapter_count} chapters")
        
        # Create book directory
        book_dir = output_dir / f"Book_{book_roman}"
        book_dir.mkdir(exist_ok=True)
        
        for chapter in range(1, chapter_count + 1):
            chapter_roman = int_to_roman(chapter)
            
            # Construct URL
            url = f"https://ccel.org/ccel/henry/mhcc/mhcc.{book_roman}.{chapter_roman}.html"
            
            # Create filename
            filename = f"Chapter_{chapter_roman}.html"
            filepath = book_dir / filename
            
            try:
                print(f"  Downloading Chapter {chapter_roman} ({chapter})...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                # Save the HTML content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                total_downloaded += 1
                print(f"    Saved: {filename}")
                
                # Small delay to be respectful to the server
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"    Failed to download {url}: {e}")
                continue
    
    print(f"\nCompleted! Downloaded {total_downloaded} commentary chapters.")
    print(f"Files saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    download_mhc_commentary()