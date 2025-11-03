# Matthew Henry's Commentary

This directory contains Matthew Henry's Commentary on the Whole Bible in multiple formats.

## About the Commentary

Matthew Henry's Commentary is one of the most widely used and respected Bible commentaries in the English language. It provides verse-by-verse exposition with practical applications for Christian living.

## Available Formats

- **MHC.json** - JSON format for programmatic access
- **MHC.db** - SQLite database with structured tables  
- **MHC.csv** - CSV format for spreadsheet applications
- **MHC.txt** - Plain text format for reading

## Database Schema (SQLite)

### Table: mhc_books
- `id` (INTEGER PRIMARY KEY) - Unique book identifier
- `name` (TEXT) - Name of the Bible book

### Table: mhc_commentary  
- `id` (INTEGER PRIMARY KEY) - Unique commentary entry identifier
- `book_id` (INTEGER) - Foreign key to mhc_books table
- `commentary` (TEXT) - The commentary text for the book

## Source

Processed from files downloaded from Christian Classics Ethereal Library (CCEL).

## License

This work is in the public domain.
