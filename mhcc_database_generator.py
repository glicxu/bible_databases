import os
import json
import sqlite3
import csv
from bs4 import BeautifulSoup
import re

class MHCCDatabaseGenerator:
    def __init__(self, input_dir="mhcc_commentary"):
        self.input_dir = input_dir
        self.book_mapping = {
            'Genesis': 'Genesis', 'Exodus': 'Exodus', 'Leviticus': 'Leviticus', 
            'Numbers': 'Numbers', 'Deuteronomy': 'Deuteronomy', 'Joshua': 'Joshua',
            'Judges': 'Judges', 'Ruth': 'Ruth', '1 Samuel': '1 Samuel', '2 Samuel': '2 Samuel',
            '1 Kings': '1 Kings', '2 Kings': '2 Kings', '1 Chronicles': '1 Chronicles',
            '2 Chronicles': '2 Chronicles', 'Ezra': 'Ezra', 'Nehemiah': 'Nehemiah',
            'Esther': 'Esther', 'Job': 'Job', 'Psalms': 'Psalms', 'Proverbs': 'Proverbs',
            'Ecclesiastes': 'Ecclesiastes', 'Song of Solomon': 'Song of Solomon',
            'Isaiah': 'Isaiah', 'Jeremiah': 'Jeremiah', 'Lamentations': 'Lamentations',
            'Ezekiel': 'Ezekiel', 'Daniel': 'Daniel', 'Hosea': 'Hosea', 'Joel': 'Joel',
            'Amos': 'Amos', 'Obadiah': 'Obadiah', 'Jonah': 'Jonah', 'Micah': 'Micah',
            'Nahum': 'Nahum', 'Habakkuk': 'Habakkuk', 'Zephaniah': 'Zephaniah',
            'Haggai': 'Haggai', 'Zechariah': 'Zechariah', 'Malachi': 'Malachi',
            'Matthew': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke', 'John': 'John',
            'Acts': 'Acts', 'Romans': 'Romans', '1 Corinthians': '1 Corinthians',
            '2 Corinthians': '2 Corinthians', 'Galatians': 'Galatians', 'Ephesians': 'Ephesians',
            'Philippians': 'Philippians', 'Colossians': 'Colossians', '1 Thessalonians': '1 Thessalonians',
            '2 Thessalonians': '2 Thessalonians', '1 Timothy': '1 Timothy', '2 Timothy': '2 Timothy',
            'Titus': 'Titus', 'Philemon': 'Philemon', 'Hebrews': 'Hebrews', 'James': 'James',
            '1 Peter': '1 Peter', '2 Peter': '2 Peter', '1 John': '1 John', '2 John': '2 John',
            '3 John': '3 John', 'Jude': 'Jude', 'Revelation': 'Revelation'
        }

    def extract_commentary_from_file(self, html_file):
        """Extract commentary content from HTML file"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        content_div = soup.find('div', class_='book-content')
        
        if not content_div:
            return None
        
        # Extract book title
        title_elem = content_div.find('h2')
        book_title = title_elem.get_text().strip() if title_elem else "Unknown"
        
        # Clean up book title
        book_title = re.sub(r'\s+', ' ', book_title).strip()
        
        # Extract commentary text
        paragraphs = []
        for p in content_div.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 20:
                # Clean up text
                text = re.sub(r'\s+', ' ', text)
                paragraphs.append(text)
        
        return {
            'book': book_title,
            'filename': os.path.basename(html_file),
            'commentary': '\n\n'.join(paragraphs)
        }

    def generate_sqlite_database(self, output_file="mhcc.db"):
        """Generate SQLite database"""
        conn = sqlite3.connect(output_file)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mhcc_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                filename TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mhcc_commentary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                commentary TEXT,
                FOREIGN KEY (book_id) REFERENCES mhcc_books (id)
            )
        ''')
        
        # Process files
        book_id = 1
        for filename in sorted(os.listdir(self.input_dir)):
            if filename.endswith('.html'):
                filepath = os.path.join(self.input_dir, filename)
                commentary_data = self.extract_commentary_from_file(filepath)
                
                if commentary_data:
                    # Insert book
                    cursor.execute(
                        "INSERT INTO mhcc_books (id, name, filename) VALUES (?, ?, ?)",
                        (book_id, commentary_data['book'], filename)
                    )
                    
                    # Insert commentary
                    cursor.execute(
                        "INSERT INTO mhcc_commentary (book_id, commentary) VALUES (?, ?)",
                        (book_id, commentary_data['commentary'])
                    )
                    
                    book_id += 1
                    print(f"Added to database: {commentary_data['book']}")
        
        conn.commit()
        conn.close()
        print(f"SQLite database created: {output_file}")

    def generate_json_format(self, output_file="mhcc.json"):
        """Generate JSON format"""
        commentaries = []
        
        for filename in sorted(os.listdir(self.input_dir)):
            if filename.endswith('.html'):
                filepath = os.path.join(self.input_dir, filename)
                commentary_data = self.extract_commentary_from_file(filepath)
                
                if commentary_data:
                    commentaries.append({
                        'book': commentary_data['book'],
                        'commentary': commentary_data['commentary']
                    })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(commentaries, f, indent=2, ensure_ascii=False)
        
        print(f"JSON file created: {output_file}")

    def generate_csv_format(self, output_file="mhcc.csv"):
        """Generate CSV format"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['book', 'commentary'])
            
            for filename in sorted(os.listdir(self.input_dir)):
                if filename.endswith('.html'):
                    filepath = os.path.join(self.input_dir, filename)
                    commentary_data = self.extract_commentary_from_file(filepath)
                    
                    if commentary_data:
                        writer.writerow([commentary_data['book'], commentary_data['commentary']])
        
        print(f"CSV file created: {output_file}")

    def generate_all_formats(self):
        """Generate all output formats"""
        if not os.path.exists(self.input_dir):
            print(f"Input directory '{self.input_dir}' not found.")
            return
        
        print("Generating Matthew Henry's Concise Commentary database...")
        
        # Create formats directory
        formats_dir = os.path.join("formats", "commentary")
        os.makedirs(formats_dir, exist_ok=True)
        
        # Generate all formats
        self.generate_sqlite_database(os.path.join(formats_dir, "mhcc.db"))
        self.generate_json_format(os.path.join(formats_dir, "mhcc.json"))
        self.generate_csv_format(os.path.join(formats_dir, "mhcc.csv"))
        
        print(f"\nAll formats generated in '{formats_dir}' directory")

def main():
    generator = MHCCDatabaseGenerator()
    generator.generate_all_formats()

if __name__ == "__main__":
    main()