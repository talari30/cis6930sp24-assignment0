import re
import pypdf
import argparse
from urllib.request import urlretrieve
import sqlite3
import requests
import os
from bs4 import BeautifulSoup

def main(url):
    
    # Extraction of data is taking place
    incidents = parse_incident_reports(url)
	
    # Database initiation
    db, cursor = initialize_Db()
	
    # Insertion of data
    insertindb(db, incidents)
	
    # Printing incident counts
    statusofdb(db)
 
    
def download_pdf_file(url: str):
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """

    # Request URL and get response object
    response = requests.get(url, stream=True)

    # isolate PDF filename from URL
    pdf_file_name = os.path.basename(url)
    if response.status_code == 200:
        # Save in current working directory
        filepath = os.path.join(os.getcwd(), pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            
    else:
        print(f' oh man! Could not download {pdf_file_name},')


#extracting
def parse_incident_reports(pdf_source):
    pattern = r"\s+(?=\d+/\d+/\d+\s)"
    file_index = 0
    parsed_incidents = []
    # Download PDF
    pdf_filename = str(file_index) + '.pdf'
    urlretrieve(pdf_source, pdf_filename)
    with open(pdf_filename, 'rb') as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_filename)
        # Concatenate text from all pages
        combined_text = ""
        for page in pdf_reader.pages:
            combined_text += page.extract_text(extraction_mode="layout") + "\n\n\n"
            combined_text = combined_text.strip(r'\s{2,}')
    # Split text into chunks based on the regex pattern
    incident_data_chunks = re.split(pattern, combined_text)
    
    index = 0
    

    while True:
        chunk = incident_data_chunks[index]
        chunk = re.findall(pattern, chunk)
        details = re.split(r'\s{2,}', incident_data_chunks[index + 1], maxsplit=4)
        if len(details) == 5:
            temp_record = {
                'incident_time': details[0], 'incident_number': details[1],
                'incident_location': details[2], 'nature': details[3] if details[3] != "None" else "",  # Replace "None" with empty string
                'incident_ori': details[4]
            }
        else:
            temp_record = {
                'incident_time': details[0], 'incident_number': details[1],
                'incident_ori': details[2], 'nature': "", 'incident_location': ""  # Set nature to empty string directly
            }
        index += 1
        parsed_incidents.append(temp_record)
        if index >= len(incident_data_chunks) - 2:
            break

    file_index += 1
    return parsed_incidents


#starting the database
import os
import sqlite3

def initialize_Db():
    # Create directory if it doesn't exist
    if not os.path.exists("resources"):
        os.makedirs("resources")
    
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect("resources/normanpd.db")
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Create the 'incidents' table with the specified schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    
    # Commit changes
    # conn.commit()
    
    # Return the database connection
#     conn.close()
    return (conn,cursor)

def insertindb(db, incidents):
#     connection_obj = sqlite3.connect('normanpd.db')
    # deletedb(db=db)
    # cursor object
    cursor_obj = db.cursor()

    for incident in incidents:
        try:
            cursor_obj.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)",
                       (incident['incident_time'], incident['incident_number'],
                        incident['incident_location'], incident['nature'], incident['incident_ori']))
        except:
            print('error in insertion')
    return len(incidents)
def statusofdb(db):
    op=db.execute("""SELECT nature || '|' || COUNT(*) AS row
    FROM incidents
    GROUP BY nature
    ORDER BY COUNT(*) DESC, nature ASC;

    """).fetchall()
    
    natures=""
   
    
    natures_list = [str(o[0]) for o in op]  # Create a list comprehension to prepare all strings
    natures = "\n".join(natures_list)  # Join all strings using newline as separator without adding an extra newline at the end
    print(natures)

    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)