import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
from urllib.parse import urlparse, parse_qs, urljoin

# Path to memory zip
memory_zip_path = "memory.zip"

# Ensure memory.zip exists
if not os.path.exists(memory_zip_path):
    with ZipFile(memory_zip_path, 'w') as zipf:
        pass

def extract_actual_url(duckduckgo_url):
    parsed_url = urlparse(duckduckgo_url)
    if parsed_url.netloc == "duckduckgo.com" and "uddg" in parse_qs(parsed_url.query):
        actual_url = parse_qs(parsed_url.query)["uddg"][0]
        if not actual_url.startswith("http://") and not actual_url.startswith("https://"):
            actual_url = "https://" + actual_url
        return actual_url
    if not duckduckgo_url.startswith("http://") and not duckduckgo_url.startswith("https://"):
        duckduckgo_url = "https://" + duckduckgo_url
    return duckduckgo_url


def search_engine(query):
    print(f"Searching for '{query}' on DuckDuckGo...")
    response = requests.get(f"https://duckduckgo.com/html/?q={query}")
    if response.status_code != 200:
        print("Failed to connect to DuckDuckGo.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for result in soup.find_all('a', class_='result__a'):
        title = result.get_text()
        link = result['href']
        if link.startswith('//'):
            link = 'https:' + link
        link = extract_actual_url(link)
        results.append((title, link))
    return results

def fetch_site_details(url):
    print(f"Fetching details for {url}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else soup.get_text().strip().split('\n')[0]
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else "No Description"

        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        files = []
        # Find all image URLs in the page
        for img_tag in soup.find_all('img', src=True):
            img_url = img_tag['src']
            # Ensure it is a full URL
            if img_url.startswith('/'):
                img_url = base_url + img_url
            files.append(img_url)

        return title, description, files, base_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching site: {e}")
        return "Error", "Error", [], ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error", "Error", [], ""


def download_file(url, filename, base_url):
    print(f"Downloading {filename}...")

    try:
        # If the URL starts with double slashes (//), prepend with https
        if url.startswith('//'):
            url = 'https:' + url

        # If the URL is relative, join it with the base URL
        elif not url.startswith('http'):
            url = urljoin(base_url, url)

        # Send the request and follow redirects
        response = requests.get(url, stream=True, allow_redirects=True)

        # Check if the response is an image
        if 'image' not in response.headers['Content-Type']:
            print(f"Skipping {filename} (not an image).")
            return

        # Download the image
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"File {filename} downloaded successfully.")

            # Add the file to memory.zip
            with ZipFile(memory_zip_path, 'a') as zipf:
                zipf.write(filename, os.path.basename(filename))  # Ensure only the filename is saved
            print(f"File {filename} added to memory.zip.")

            # Optionally remove the local file after adding it to the zip
            os.remove(filename)
            print(f"File {filename} removed from local disk after zipping.")
        else:
            print(f"Failed to download the file: {url}")
    except Exception as e:
        print(f"Error downloading file: {e}")



def main():
    while True:
        print("\nSussy Browser")
        print("1. Search")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            query = input("Enter search query: ")
            results = search_engine(query)
            if not results:
                print("No results found.")
                continue

            for i, (title, link) in enumerate(results):
                print(f"{i+1}. {title} - {link}")

            try:
                selection = int(input("Select a result (number): ")) - 1
                if selection < 0 or selection >= len(results):
                    print("Invalid selection.")
                    continue

                title, link = results[selection]
                site_title, site_description, files, base_url = fetch_site_details(link)
                print(f"Title: {site_title}")
                print(f"Description: {site_description}")

                if files:
                    print("Files available for download:")
                    for i, file_url in enumerate(files):
                        print(f"{i+1}. {file_url}")

                    try:
                        file_selection = int(input("Select a file to download (number): ")) - 1
                        if file_selection < 0 or file_selection >= len(files):
                            print("Invalid selection.")
                            continue

                        file_url = files[file_selection]
                        filename = file_url.split('/')[-1]
                        download_file(file_url, filename, base_url)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                else:
                    print("No downloadable files found on this site.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '2':
            print("Exiting Mini OS Browser.")
            break

        else:
            print("Invalid choice.")
