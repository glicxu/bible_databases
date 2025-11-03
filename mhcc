import os
from bs4 import BeautifulSoup, NavigableString

def extract_books_from_mhcc(input_file_path: str, output_directory: str):
    """
    Parses the Matthew Henry's Concise Commentary HTML file and splits it
    into separate HTML files for each book of the Bible.

    Args:
        input_file_path (str): The path to the mhcc.doc file.
        output_directory (str): The directory where the individual book HTML files will be saved.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback to 'latin-1' if 'utf-8' fails, as these old files can have mixed encodings.
        with open(input_file_path, 'r', encoding='latin-1') as f:
            content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    print(f"Output directory '{output_directory}' created or already exists.")

    # Extract the head content to use as a template for new files
    head_content = soup.head.prettify() if soup.head else "<head><title>Content</title></head>"

    # Find the main content container
    main_content_div = soup.find('div', class_='Section1')
    if not main_content_div:
        print("Error: Could not find the main content <div class='Section1'>.")
        return

    current_book_name = None
    current_book_html = []
    books_extracted = 0

    for element in main_content_div.children:
        # The start of a new book is identified by a <p class="div1"> tag
        if element.name == 'p' and element.get('class') == ['div1']:
            # If we were already processing a book, save it first.
            if current_book_name and current_book_html:
                # Sanitize filename
                safe_filename = "".join([c for c in current_book_name if c.isalnum() or c in (' ', '_')]).rstrip()
                output_filename = os.path.join(output_directory, f"{safe_filename}.html")
                
                # Create the full HTML for the book
                book_body = "".join(str(tag) for tag in current_book_html)
                final_html = f"<html>\n{head_content}\n<body>\n{book_body}\n</body>\n</html>"
                
                with open(output_filename, 'w', encoding='utf-8') as f_out:
                    f_out.write(final_html)
                print(f"Extracted and saved: {output_filename}")
                books_extracted += 1

            # Start the next book
            current_book_name = element.get_text(strip=True)
            current_book_html = [str(element)] # Start with the title tag
        elif current_book_name:
            # Add content to the current book
            if not (isinstance(element, NavigableString) and element.strip() == ''):
                current_book_html.append(str(element))

    print(f"\nExtraction complete. Total books extracted: {books_extracted}")

if __name__ == "__main__":
    # Define the path to your local mhcc.doc file
    source_file = "c:\\src\\workspaces\\bible_databases\\mhcc.doc"
    
    # Define the directory where you want to save the extracted book files
    output_folder = "mhcc_extracted_books"

    if os.path.exists(source_file):
        extract_books_from_mhcc(source_file, output_folder)
    else:
        print(f"Error: Source file not found at '{source_file}'")