import os
import json
import csv
from bs4 import BeautifulSoup
import re

def extract_commentary_content(html_file):
    """Extract commentary content from a single HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the main content div
    content_div = soup.find('div', class_='book-content')
    if not content_div:
        return None
    
    # Extract book title
    title_elem = content_div.find('h2')
    book_title = title_elem.get_text().strip() if title_elem else "Unknown"
    
    # Extract all paragraphs of commentary
    paragraphs = []
    for p in content_div.find_all('p'):
        text = p.get_text().strip()
        if text and len(text) > 10:  # Filter out very short paragraphs
            paragraphs.append(text)
    
    return {
        'book': book_title,
        'filename': os.path.basename(html_file),
        'content': '\n\n'.join(paragraphs)
    }

def process_all_files(input_dir, output_formats=['json', 'csv', 'txt']):
    """Process all HTML files and create output in multiple formats"""
    commentaries = []
    
    # Process each HTML file
    for filename in os.listdir(input_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(input_dir, filename)
            commentary = extract_commentary_content(filepath)
            if commentary:
                commentaries.append(commentary)
                print(f"Processed: {filename}")
    
    # Sort by book name
    commentaries.sort(key=lambda x: x['book'])
    
    # Create outputs
    if 'json' in output_formats:
        create_json_output(commentaries)
    
    if 'csv' in output_formats:
        create_csv_output(commentaries)
    
    if 'txt' in output_formats:
        create_txt_output(commentaries)
    
    print(f"\nProcessed {len(commentaries)} commentary files")

def create_json_output(commentaries):
    """Create JSON output"""
    output_file = "mhcc_commentary.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(commentaries, f, indent=2, ensure_ascii=False)
    print(f"Created: {output_file}")

def create_csv_output(commentaries):
    """Create CSV output"""
    output_file = "mhcc_commentary.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['book', 'filename', 'content'])
        for commentary in commentaries:
            writer.writerow([commentary['book'], commentary['filename'], commentary['content']])
    print(f"Created: {output_file}")

def create_txt_output(commentaries):
    """Create plain text output"""
    output_file = "mhcc_commentary.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for commentary in commentaries:
            f.write(f"=== {commentary['book']} ===\n")
            f.write(f"Source: {commentary['filename']}\n\n")
            f.write(commentary['content'])
            f.write("\n\n" + "="*50 + "\n\n")
    print(f"Created: {output_file}")

def main():
    input_dir = "mhcc_commentary"
    
    if not os.path.exists(input_dir):
        print(f"Directory '{input_dir}' not found. Please run download_mhc_from_ccel.py first.")
        return
    
    print("Extracting commentary content...")
    process_all_files(input_dir)

if __name__ == "__main__":
    main()