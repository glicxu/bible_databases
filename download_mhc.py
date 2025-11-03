import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_mhc_commentary(index_html_content: str, output_directory: str, base_web_url: str = "https://www.ccel.org"):
    """
    Downloads all linked Matthew Henry Commentary files from the given MHC index HTML content.

    Args:
        index_html_content (str): The HTML content of the mhc.doc index file.
        output_directory (str): The directory where downloaded files will be saved.
        base_web_url (str): The base URL for constructing absolute links from relative ones.
                            Based on the DC.Identifier in the index, 'https://www.ccel.org' is inferred.
    """
    os.makedirs(output_directory, exist_ok=True)
    print(f"Output directory created/ensured: '{output_directory}'")

    soup = BeautifulSoup(index_html_content, 'html.parser')

    links_to_download = set()
    # Find all <a> tags with an href attribute.
    for a_tag in soup.find_all('a', href=True):
        relative_path = a_tag['href']
        # Filter for links that are part of the commentary series.
        # These links typically start with '/ccel/henry/mhc' followed by volume and book info.
        if relative_path.startswith('/ccel/henry/mhc'):
            full_url = urljoin(base_web_url, relative_path)
            links_to_download.add(full_url)
    
    print(f"Found {len(links_to_download)} unique commentary links to download.")

    downloaded_count = 0
    for url in sorted(list(links_to_download)): # Sort for consistent processing and output
        try:
            print(f"Downloading: {url}")
            response = requests.get(url, timeout=15) # Set a timeout for network requests
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

            # Extract a safe filename from the URL path.
            # Example: /ccel/henry/mhc1.Gen.i.html -> mhc1.Gen.i.html
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename: # Fallback if the URL path ends with a slash
                filename = "index.html" 
            
            # Basic sanitization for filenames to avoid issues with special characters
            filename = "".join([c for c in filename if c.isalnum() or c in ('.', '_', '-')]).strip()
            if not filename: # If filename becomes empty after sanitization
                filename = f"downloaded_page_{downloaded_count}.html" # Generic fallback

            output_file_path = os.path.join(output_directory, filename)

            with open(output_file_path, 'wb') as f: # 'wb' for binary write, as response.content is bytes
                f.write(response.content)
            print(f"Saved: {output_file_path}")
            downloaded_count += 1

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {url}: {e}")

    print(f"\n--- Download Summary ---")
    print(f"Successfully downloaded {downloaded_count} files to '{output_directory}'")
    print(f"Failed to download {len(links_to_download) - downloaded_count} files.")
    print("These HTML files now contain the Matthew Henry Commentary content, ready for your dali_bible app.")

# --- How to use the script ---
if __name__ == "__main__":
    # 1. Define the path to your local mhc.doc file
    local_index_file_path = "c:\\src\\workspaces\\bible_databases\\mhc.doc"
    
    # 2. Define the directory where you want to save the downloaded commentary files
    output_folder_for_commentary = "downloaded_mhc_commentary"

    # Ensure the local index file exists
    if not os.path.exists(local_index_file_path):
        print(f"Error: The index file '{local_index_file_path}' was not found.")
        print("Please ensure the path is correct and the file exists.")
    else:
        # Read the content of the local mhc.doc file
        try:
            # Using 'latin-1' encoding as 'utf-8' can fail on some characters in this specific file.
            with open(local_index_file_path, 'r', encoding='latin-1') as f:
                mhc_index_html_content = f.read()
            
            # Run the download function
            download_mhc_commentary(mhc_index_html_content, output_folder_for_commentary)
        except Exception as e:
            print(f"An error occurred while reading '{local_index_file_path}': {e}")