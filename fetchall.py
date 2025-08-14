import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_zips(base_url, catalog_url, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Fetch the catalog page
    response = requests.get(urljoin(base_url, catalog_url))
    if response.status_code != 200:
        print(f"Failed to fetch catalog from {urljoin(base_url, catalog_url)}")
        return

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags with href containing .zip
    zip_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '.zip' in href:
            zip_links.append(href)

    print(f"Found {len(zip_links)} ZIP files in {output_folder}")

    # Download each ZIP
    for zip_file in zip_links:
        full_url = urljoin(base_url, zip_file)
        local_path = os.path.join(output_folder, os.path.basename(zip_file))

        if os.path.exists(local_path):
            print(f"Skipping existing file: {local_path}")
            continue

        print(f"Downloading {full_url} to {local_path}")
        zip_response = requests.get(full_url, stream=True)
        if zip_response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in zip_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded {local_path}")
        else:
            print(f"Failed to download {full_url}")

# Base URL
base_url = "https://www.stairwaytohell.com/bbc/archive/"

# Catalog for disk images
disk_base = "diskimages/"
disk_catalog = "reclist.php?sort=name&filter=.zip"
download_zips(base_url + disk_base, disk_catalog, "diskimages")

# Catalog for tape images
tape_base = "tapeimages/"
tape_catalog = "reclist.php?sort=name&filter=.zip"
download_zips(base_url + tape_base, tape_catalog, "tapeimages")