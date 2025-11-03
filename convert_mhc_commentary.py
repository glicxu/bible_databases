import os
import json
import sqlite3
import re
from bs4 import BeautifulSoup

# Bible books mapping (Roman numeral index to book name and chapter count)
BIBLE_BOOKS = {
    2: ("Genesis", 50), 3: ("Exodus", 40), 4: ("Leviticus", 27), 5: ("Numbers", 36),
    6: ("Deuteronomy", 34), 7: ("Joshua", 24), 8: ("Judges", 21), 9: ("Ruth", 4),
    10: ("1 Samuel", 31), 11: ("2 Samuel", 24), 12: ("1 Kings", 22), 13: ("2 Kings", 25),
    14: ("1 Chronicles", 29), 15: ("2 Chronicles", 36), 16: ("Ezra", 10), 17: ("Nehemiah", 13),
    18: ("Esther", 10), 19: ("Job", 42), 20: ("Psalms", 150), 21: ("Proverbs", 31),
    22: ("Ecclesiastes", 12), 23: ("Song of Solomon", 8), 24: ("Isaiah", 66), 25: ("Jeremiah", 52),
    26: ("Lamentations", 5), 27: ("Ezekiel", 48), 28: ("Daniel", 12), 29: ("Hosea", 14),
    30: ("Joel", 3), 31: ("Amos", 9), 32: ("Obadiah", 1), 33: ("Jonah", 4),
    34: ("Micah", 7), 35: ("Nahum", 3), 36: ("Habakkuk", 3), 37: ("Zephaniah", 3),
    38: ("Haggai", 2), 39: ("Zechariah", 14), 40: ("Malachi", 4), 41: ("Matthew", 28),
    42: ("Mark", 16), 43: ("Luke", 24), 44: ("John", 21), 45: ("Acts", 28),
    46: ("Romans", 16), 47: ("1 Corinthians", 16), 48: ("2 Corinthians", 13), 49: ("Galatians", 6),
    50: ("Ephesians", 6), 51: ("Philippians", 4), 52: ("Colossians", 4), 53: ("1 Thessalonians", 5),
    54: ("2 Thessalonians", 3), 55: ("1 Timothy", 6), 56: ("2 Timothy", 4), 57: ("Titus", 3),
    58: ("Philemon", 1), 59: ("Hebrews", 13), 60: ("James", 5), 61: ("1 Peter", 5),
    62: ("2 Peter", 3), 63: ("1 John", 5), 64: ("2 John", 1), 65: ("3 John", 1),
    66: ("Jude", 1), 67: ("Revelation", 22)
}

def roman_to_int(roman):
    """Convert Roman numeral to integer"""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for char in reversed(roman):
        value = values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total

def extract_commentary_text(html_content):
    """Extract clean commentary text from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main content area
    content_div = soup.find('div', id='content')
    if not content_div:
        return ""
    
    # Remove script and style elements
    for script in content_div(["script", "style"]):
        script.decompose()
    
    # Get text and clean it up
    text = content_div.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def convert_commentary():
    """Convert MHC commentary to proper format"""
    source_dir = "mhc_commentary_roman"
    
    # Create output directories
    os.makedirs("mhc_commentary_formatted/html", exist_ok=True)
    os.makedirs("mhc_commentary_formatted/json", exist_ok=True)
    
    # Initialize data structures
    all_commentary = {}
    
    # Create SQLite database
    conn = sqlite3.connect("mhc_commentary_formatted/mhc_commentary.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commentary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            chapter INTEGER,
            text TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    # Process each book
    for book_num in range(2, 68):  # Books II to LXVII
        if book_num not in BIBLE_BOOKS:
            continue
            
        book_name, chapter_count = BIBLE_BOOKS[book_num]
        book_roman = f"Book_{roman_to_roman(book_num)}"
        
        print(f"Processing {book_name}...")
        
        # Insert book into database
        cursor.execute("INSERT OR IGNORE INTO books (id, name) VALUES (?, ?)", 
                      (book_num, book_name))
        
        book_commentary = {}
        
        # Create book directory for HTML output
        book_dir = f"mhc_commentary_formatted/html/{book_name}"
        os.makedirs(book_dir, exist_ok=True)
        
        # Process each chapter
        for chapter in range(1, chapter_count + 1):
            chapter_roman = roman_to_roman(chapter)
            source_file = f"{source_dir}/{book_roman}/Chapter_{chapter_roman}.html"
            
            if os.path.exists(source_file):
                with open(source_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Extract clean text
                commentary_text = extract_commentary_text(html_content)
                
                # Save HTML file with proper name
                html_file = f"{book_dir}/Chapter_{chapter}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Store in data structures
                book_commentary[chapter] = commentary_text
                
                # Insert into database
                cursor.execute(
                    "INSERT INTO commentary (book_id, chapter, text) VALUES (?, ?, ?)",
                    (book_num, chapter, commentary_text)
                )
        
        # Save book JSON
        if book_commentary:
            all_commentary[book_name] = book_commentary
            with open(f"mhc_commentary_formatted/json/{book_name}.json", 'w', encoding='utf-8') as f:
                json.dump(book_commentary, f, indent=2, ensure_ascii=False)
    
    # Save complete JSON
    with open("mhc_commentary_formatted/json/complete_commentary.json", 'w', encoding='utf-8') as f:
        json.dump(all_commentary, f, indent=2, ensure_ascii=False)
    
    # Commit and close database
    conn.commit()
    conn.close()
    
    print("Conversion completed!")
    print(f"- HTML files: mhc_commentary_formatted/html/")
    print(f"- JSON files: mhc_commentary_formatted/json/")
    print(f"- SQLite database: mhc_commentary_formatted/mhc_commentary.db")

def roman_to_roman(num):
    """Convert integer to Roman numeral"""
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    result = ''
    for i, value in enumerate(values):
        count = num // value
        result += numerals[i] * count
        num -= value * count
    return result

if __name__ == "__main__":
    convert_commentary()