import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_mhc_index():
    """Download the MHC index page from CCEL"""
    url = "https://ccel.org/ccel/henry/mhcc/mhcc.i.html"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_commentary_links(html_content):
    """Extract all commentary book links from the index"""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    # Find all links that point to commentary sections
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'mhcc' in href and '.html' in href and href != 'mhcc.i.html':
            full_url = urljoin("https://ccel.org/ccel/henry/mhcc/", href)
            links.append(full_url)
    
    return list(set(links))  # Remove duplicates

def download_commentary_file(url, output_dir):
    """Download a single commentary file"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        filename = os.path.basename(url)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    output_dir = "mhcc_commentary"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Downloading MHC Concise Commentary index...")
    index_html = download_mhc_index()
    
    print("Extracting commentary links...")
    links = extract_commentary_links(index_html)
    print(f"Found {len(links)} commentary files to download")
    
    success_count = 0
    for url in links:
        if download_commentary_file(url, output_dir):
            success_count += 1
    
    print(f"\nDownload complete: {success_count}/{len(links)} files downloaded successfully")

if __name__ == "__main__":
    main()