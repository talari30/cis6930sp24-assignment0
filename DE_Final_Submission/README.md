cis6930sp24 Rahul Talari
This Python script is designed to download, parse, and store incident report data from PDF files available through specified URLs. It leverages various Python libraries to handle PDF files, web requests, and database operations.

Features:-

PDF Download: Downloads PDF files from specified URLs.
Data Parsing: Extracts incident report data from downloaded PDF files.
Database Storage: Stores extracted data in a SQLite database for further analysis.
Reporting: Outputs a summary of incident counts by nature.
Dependencies
re: For regex operations to parse text data.
pypdf: To read PDF files.
argparse: For command-line option parsing.
urllib.request: To download files from the internet.
sqlite3: For SQLite database operations.
requests: To make HTTP requests.
os: To interact with the operating system, e.g., file paths.
bs4 (BeautifulSoup): For parsing HTML, if needed for web scraping.
Installation
Before running the script, ensure you have Python installed on your system. This project is best managed with Pipenv, which handles virtual environments and package installations.

Installing Pipenv:-

If you don't have Pipenv installed, install it globally with pip: pip install pipenv
Setting Up the Project
Clone the repository or download the project files to your local machine.

Navigate to the project directory and run the following command to create a virtual environment and install the required packages:
pipenv install re pypdf2 argparse requests beautifulsoup4

Note: Replace pypdf with pypdf2 or the correct package name for PDF handling as needed.

Activate the virtual environment: pipenv shell

Usage:-

Run the script from the command line, specifying the URL of the incident summary PDF as an argument:python your_script_name.py --incidents "URL_OF_THE_PDF"

Replace your_script_name.py with the name of your Python script.

Functions Overview:-

main(url): Orchestrates the download, parsing, and database storage process.
download_pdf_file(url): Downloads a PDF file from a specified URL.
parse_incident_reports(pdf_source): Parses the incident reports from the downloaded PDF file.
initialize_Db(): Initializes the SQLite database and creates the necessary tables if they do not exist.
insertindb(db, incidents): Inserts parsed incident data into the database.
statusofdb(db): Prints a summary of incidents grouped by nature.

Additional Notes:-

Ensure the SQLite database path in createdb() matches your desired location.
Modify the parsing logic in parse_incident_reports as necessary to accommodate the structure of your specific PDF files.
