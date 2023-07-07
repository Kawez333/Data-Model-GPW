import csv
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Funkcja scrapująca dane i zapisująca do pliku CSV
def scrape_and_save_data():
    url = "https://www.wnp.pl/finanse/gpw/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="table-3")

    # Pobranie nagłówków tabeli
    headers = []
    header_row = table.find("thead").find("tr")
    header_cells = header_row.find_all("th")
    for cell in header_cells:
        headers.append(cell.text.strip())

    # Pobranie danych z wierszy tabeli
    data_rows = table.find("tbody").find_all("tr")
    rows_data = []
    for row in data_rows:
        cells = row.find_all("td")
        row_data = []
        for cell in cells:
            row_data.append(cell.text.strip())
        rows_data.append(row_data)

    # Zapis danych do pliku CSV
    filename = "wyniki.csv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows_data)

    print(f"Dane zostały zapisane do pliku {filename}")

# Wywołanie funkcji scrapującej i zapisującej dane
scrape_and_save_data()

# Konfiguracja połączenia z kontem Storage Blob
account_name = 'gpwblob'
account_key = '*******************************'
container_name = 'gpwcont'
blob_name = 'wyniki.csv'

# Utworzenie klienta BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Utworzenie kontenera (jeśli nie istnieje)
container_client = blob_service_client.get_container_client(container_name)
try:
    container_client.create_container()
    print(f"Kontener '{container_name}' został utworzony.")
except Exception as e:
    print(f"Kontener '{container_name}' już istnieje.")

# Ścieżka do pliku CSV
csv_file_path = os.path.join(os.getcwd(), "wyniki.csv")

# Wrzucanie pliku do kontenera Blob Storage
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
with open(csv_file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("Plik został wrzucony do kontenera Blob Storage.")