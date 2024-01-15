import requests
from bs4 import BeautifulSoup
import os

# URL of the page
url = 'https://mega.nz/desktop'

# Send a GET request
response = requests.get(url)

# If the GET request is successful, the status code will be 200
if response.status_code == 200:
    # Get the content of the response
    page_content = response.content

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find all links on the page
    links = soup.find_all('a')

    # Filter the links for those that are for Linux distributions
    linux_links = [link.get('href') for link in links if link.get('href') is not None and 'linux' in link.get('href')]

    # Check each link
    for link in linux_links:
        response = requests.get(link, stream=True)

        # If the GET request is successful, the status code will be 200
        if response.status_code == 200:
            print(f'The URL {link} is reachable.')

            # Download the file
            local_filename = link.split('/')[-1]
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f'The file {local_filename} has been downloaded.')
        else:
            print(f'The URL {link} is not reachable.')
else:
    print(f'The URL {url} is not reachable.')
