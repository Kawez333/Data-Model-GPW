import csv
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Function for scraping data and saving it to a CSV file
def scrape_and_save_data():
    url = "https://www.wnp.pl/finanse/gpw/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="table-3")

    # Get table headers
    headers = []
    header_row = table.find("thead").find("tr")
    header_cells = header_row.find_all("th")
    for cell in header_cells:
        headers.append(cell.text.strip())

    # Get data from table rows
    data_rows = table.find("tbody").find_all("tr")
    rows_data = []
    for row in data_rows:
        cells = row.find_all("td")
        row_data = []
        for cell in cells:
            row_data.append(cell.text.strip())
        rows_data.append(row_data)

    # Save data to a CSV file
    filename = "results.csv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows_data)

    print(f"Data has been saved to the file {filename}")

# Call the function to scrape and save the data
scrape_and_save_data()

# Storage Blob account connection configuration
account_name = 'gpwblob'
account_key = '*******************************'
container_name = 'gpwcont'
blob_name = 'results.csv'

# Create BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Create container if it doesn't exist
container_client = blob_service_client.get_container_client(container_name)
try:
    container_client.create_container()
    print(f"Container '{container_name}' has been created.")
except Exception as e:
    print(f"Container '{container_name}' already exists.")

# Path to the CSV file
csv_file_path = os.path.join(os.getcwd(), "results.csv")

# Upload the file to Blob Storage container
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
with open(csv_file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("File has been uploaded to the Blob Storage container.")
