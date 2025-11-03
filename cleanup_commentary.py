import os
import json
import sqlite3
import re

def clean_commentary_text(text):
    """Clean commentary text by removing unwanted header and footer content"""
    # Remove the header content up to "Chapter Outline"
    text = re.sub(r'^.*?(?=Chapter Outline)', '', text, flags=re.DOTALL)
    
    # Remove "Chapter X Next »" at the beginning
    text = re.sub(r'^Chapter \d+ Next »\s*', '', text)
    
    # Remove footer content from "« Prev" onwards
    text = re.sub(r'« Prev.*$', '', text, flags=re.DOTALL)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def update_json_files():
    """Update all JSON files with cleaned text"""
    json_dir = "mhc_commentary_formatted/json"
    
    for filename in os.listdir(json_dir):
        if filename.endswith('.json') and filename != 'complete_commentary.json':
            filepath = os.path.join(json_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clean each chapter's text
            for chapter, text in data.items():
                data[chapter] = clean_commentary_text(text)
            
            # Write back cleaned data
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Updated individual book JSON files")

def update_complete_json():
    """Recreate complete commentary JSON with cleaned text"""
    json_dir = "mhc_commentary_formatted/json"
    complete_data = {}
    
    for filename in os.listdir(json_dir):
        if filename.endswith('.json') and filename != 'complete_commentary.json':
            book_name = filename.replace('.json', '')
            filepath = os.path.join(json_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                complete_data[book_name] = json.load(f)
    
    # Write complete commentary file
    with open(os.path.join(json_dir, 'complete_commentary.json'), 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, indent=2, ensure_ascii=False)
    
    print("Updated complete commentary JSON file")

def update_sqlite_database():
    """Update SQLite database with cleaned text"""
    conn = sqlite3.connect("mhc_commentary_formatted/mhc_commentary.db")
    cursor = conn.cursor()
    
    # Get all commentary entries
    cursor.execute("SELECT id, text FROM commentary")
    entries = cursor.fetchall()
    
    # Update each entry with cleaned text
    for entry_id, text in entries:
        cleaned_text = clean_commentary_text(text)
        cursor.execute("UPDATE commentary SET text = ? WHERE id = ?", (cleaned_text, entry_id))
    
    conn.commit()
    conn.close()
    print("Updated SQLite database")

if __name__ == "__main__":
    print("Cleaning up commentary text...")
    update_json_files()
    update_complete_json()
    update_sqlite_database()
    print("Cleanup completed!")