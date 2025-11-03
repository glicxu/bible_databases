#!/usr/bin/env python3
"""
Explore the structure of Matthew Henry's Concise Commentary on CCEL
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def explore_mhcc_index():
    """Explore the MHCC index page to understand the structure"""
    url = "https://ccel.org/ccel/henry/mhcc/mhcc.i.html"
    
    try:
        print(f"Fetching: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("\n=== Page Title ===")
        title = soup.find('title')
        if title:
            print(title.get_text().strip())
        
        print("\n=== All Links Found ===")
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()
            if href and text:
                full_url = urljoin("https://ccel.org/ccel/henry/mhcc/", href)
                links.append((full_url, text))
                print(f"{text}: {full_url}")
        
        print(f"\nTotal links found: {len(links)}")
        
        # Try to find the main content
        print("\n=== Main Content Structure ===")
        content_div = soup.find('div', class_='book-content')
        if content_div:
            print("Found div with class 'book-content'")
            paragraphs = content_div.find_all('p')
            print(f"Found {len(paragraphs)} paragraphs")
            if paragraphs:
                print("First paragraph:", paragraphs[0].get_text()[:200] + "...")
        else:
            print("No div with class 'book-content' found")
            
            # Try alternative selectors
            thetext = soup.find('div', id='theText')
            if thetext:
                print("Found div with id 'theText'")
                paragraphs = thetext.find_all('p')
                print(f"Found {len(paragraphs)} paragraphs")
                if paragraphs:
                    print("First paragraph:", paragraphs[0].get_text()[:200] + "...")
        
        return links
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def test_specific_book_url():
    """Test a specific book URL to see the structure"""
    test_urls = [
        "https://ccel.org/ccel/henry/mhcc/mhcc.Gen.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.ii.html",
        "https://ccel.org/ccel/henry/mhcc/mhcc.toc.html"
    ]
    
    for url in test_urls:
        try:
            print(f"\n=== Testing: {url} ===")
            response = requests.get(url)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title')
                if title:
                    print(f"Title: {title.get_text().strip()}")
                
                # Look for content
                content_div = soup.find('div', class_='book-content')
                if content_div:
                    paragraphs = content_div.find_all('p')
                    print(f"Found {len(paragraphs)} paragraphs in book-content")
                    if paragraphs:
                        print("Sample text:", paragraphs[0].get_text()[:150] + "...")
                else:
                    thetext = soup.find('div', id='theText')
                    if thetext:
                        paragraphs = thetext.find_all('p')
                        print(f"Found {len(paragraphs)} paragraphs in theText")
                        if paragraphs:
                            print("Sample text:", paragraphs[0].get_text()[:150] + "...")
                    else:
                        print("No main content found")
            
        except Exception as e:
            print(f"Error with {url}: {e}")

def main():
    print("Exploring Matthew Henry's Concise Commentary Structure")
    print("=" * 60)
    
    # First explore the index
    links = explore_mhcc_index()
    
    # Then test specific URLs
    test_specific_book_url()

if __name__ == "__main__":
    main()