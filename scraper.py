import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_links(url):
    # Make a request to the site
    response = requests.get(url)

    # Check if the site is accessible
    if response.status_code != 200:
        print(f"Failed to access {url}")
        return []

    # Parse the content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all 'a' tags (which define hyperlinks)
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]

        # Construct a full URL from relative paths
        full_url = urljoin(url, href)

        # Append the full URL to the list of links
        links.append(full_url)

    return links


# Test the script with your URL
base_url = "https://stratus.usask.ca/"
found_links = get_links(base_url)

# Display all found links
for link in found_links:
    print(link)
