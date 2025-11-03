#!/usr/bin/env python3
"""
Simple Matthew Henry's Concise Commentary setup
"""

import os
import json
import sqlite3
import csv

def create_mhcc_files():
    """Create MHCC files with sample content"""
    
    # Sample commentary content
    commentary_content = """Matthew Henry's Concise Commentary on the Bible

This is a condensed version of Matthew Henry's famous commentary, providing practical observations and spiritual insights on every book of the Bible.

Genesis is a name taken from the Greek, and signifies "the book of generation or production;" it is properly so called, as containing an account of the origin of all things. There is no other history so old. There is nothing in the most ancient book which exists that contradicts it; while many things recorded by the oldest heathen writers, or to be traced in the customs of different nations, confirm what is related in the book of Genesis.

The book of Genesis contains the history of about 2,300 years, from the creation of the world to the death of Joseph. It may be divided into two parts:

1. The general history of mankind for about 1,600 years, from Adam to Abraham (chapters 1-11)
2. The particular history of Abraham and his seed for 430 years, from Abraham's call to the death of Joseph (chapters 12-50)

This commentary provides verse-by-verse exposition with practical applications for Christian living, making the ancient text relevant for modern readers. Matthew Henry's work has been treasured by believers for centuries as a source of spiritual insight and practical wisdom.

The commentary covers all 66 books of the Bible, from Genesis to Revelation, providing historical context, theological insights, and practical applications for each passage. It remains one of the most widely used and respected Bible commentaries in the English language.

Note: This is a sample entry. The full commentary would contain detailed exposition for each book of the Bible. You can download the complete commentary from CCEL at: https://ccel.org/ccel/henry/mhcc/mhcc.i.html"""

    commentary_data = [{
        'book': 'Matthew Henry\'s Concise Commentary',
        'commentary': commentary_content
    }]
    
    # Create output directory
    output_dir = os.path.join("formats", "commentary")
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean existing files
    files_to_clean = ["MHCC.db", "MHCC.json", "MHCC.csv", "MHCC.txt"]
    for filename in files_to_clean:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    # JSON format
    json_file = os.path.join(output_dir, "MHCC.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(commentary_data, f, indent=2, ensure_ascii=False)
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
    
    for i, commentary in enumerate(commentary_data, 1):
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
        for commentary in commentary_data:
            writer.writerow([commentary['book'], commentary['commentary']])
    print(f"Created: {csv_file}")
    
    # Plain text format
    txt_file = os.path.join(output_dir, "MHCC.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("Matthew Henry's Concise Commentary on the Bible\n")
        f.write("=" * 60 + "\n\n")
        for commentary in commentary_data:
            f.write(f"=== {commentary['book']} ===\n\n")
            f.write(commentary['commentary'])
            f.write("\n\n" + "=" * 60 + "\n\n")
    print(f"Created: {txt_file}")
    
    # README file
    readme_file = os.path.join(output_dir, "README.md")
    readme_content = '''# Matthew Henry's Concise Commentary

This directory contains Matthew Henry's Concise Commentary on the Bible in multiple formats.

## About the Commentary

Matthew Henry's Concise Commentary is a condensed version of his famous six-volume commentary on the Bible. It provides practical observations and spiritual insights on every book of the Bible.

## Available Formats

- **MHCC.json** - JSON format
- **MHCC.db** - SQLite database
- **MHCC.csv** - CSV format
- **MHCC.txt** - Plain text format

## Source

Based on content from Christian Classics Ethereal Library (CCEL):
https://ccel.org/ccel/henry/mhcc/mhcc.i.html

## License

Public domain.
'''
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"Created: {readme_file}")

def main():
    print("Creating Matthew Henry's Concise Commentary files...")
    create_mhcc_files()
    
    print("\nFiles created in 'formats/commentary/' directory:")
    output_dir = os.path.join("formats", "commentary")
    for filename in sorted(os.listdir(output_dir)):
        filepath = os.path.join(output_dir, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            print(f"  {filename}: {size:,} bytes")
    
    print("\nTo get the complete commentary, you can:")
    print("1. Visit: https://ccel.org/ccel/henry/mhcc/mhcc.i.html")
    print("2. Use the existing downloaded files in 'downloaded_mhc_commentary/'")
    print("3. Modify the scripts to extract from your local files")

if __name__ == "__main__":
    main()