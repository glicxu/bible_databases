#!/usr/bin/env python3
"""
Summary of Matthew Henry's Commentary extraction and processing
"""

import os
import sqlite3
import json

def show_summary():
    """Display a summary of the Matthew Henry Commentary processing"""
    
    print("Matthew Henry's Commentary Processing Summary")
    print("=" * 60)
    
    # Check what files we have
    commentary_dir = os.path.join("formats", "commentary")
    
    if not os.path.exists(commentary_dir):
        print("No commentary directory found.")
        return
    
    print(f"\nFiles created in '{commentary_dir}':")
    total_size = 0
    
    for filename in sorted(os.listdir(commentary_dir)):
        filepath = os.path.join(commentary_dir, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            total_size += size
            print(f"  {filename}: {size:,} bytes")
    
    print(f"\nTotal size: {total_size:,} bytes")
    
    # Check the database content
    db_file = os.path.join(commentary_dir, "MHC.db")
    if os.path.exists(db_file):
        print(f"\nDatabase content (MHC.db):")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Count books
        cursor.execute("SELECT COUNT(*) FROM mhc_books")
        book_count = cursor.fetchone()[0]
        print(f"  Books: {book_count}")
        
        # Count total characters
        cursor.execute("SELECT SUM(LENGTH(commentary)) FROM mhc_commentary")
        char_count = cursor.fetchone()[0]
        print(f"  Total characters: {char_count:,}")
        
        # Show some sample books
        cursor.execute("SELECT name FROM mhc_books ORDER BY name LIMIT 10")
        sample_books = cursor.fetchall()
        print(f"  Sample books: {', '.join([book[0] for book in sample_books])}")
        
        conn.close()
    
    # Check JSON content
    json_file = os.path.join(commentary_dir, "MHC.json")
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\nJSON content (MHC.json):")
        print(f"  Entries: {len(data)}")
        
        if data:
            sample_entry = data[0]
            print(f"  Sample entry: {sample_entry['book']}")
            print(f"  Sample text: {sample_entry['commentary'][:100]}...")
    
    print(f"\nSource files processed:")
    source_dir = "downloaded_mhc_commentary"
    if os.path.exists(source_dir):
        html_files = [f for f in os.listdir(source_dir) if f.endswith('.html')]
        print(f"  HTML files: {len(html_files)}")
        print(f"  Source directory: {source_dir}")
    
    print(f"\nUsage:")
    print(f"  - Use MHC.db for database applications")
    print(f"  - Use MHC.json for web applications or APIs")
    print(f"  - Use MHC.csv for spreadsheet applications")
    print(f"  - Use MHC.txt for reading or text processing")
    
    print(f"\nIntegration with Bible Database Project:")
    print(f"  - Commentary files are in the standard 'formats' directory")
    print(f"  - Database schema follows the project conventions")
    print(f"  - Files can be used alongside existing Bible translations")
    
    print(f"\nNext steps:")
    print(f"  - Import MHC.db into your Bible application")
    print(f"  - Link commentary to Bible verses by book names")
    print(f"  - Use the commentary for study and reference")

if __name__ == "__main__":
    show_summary()