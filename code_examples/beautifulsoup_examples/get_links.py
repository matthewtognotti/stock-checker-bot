from bs4 import BeautifulSoup
import requests
import project_constants

url = project_constants.MY_SITE
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all links
for link in soup.find_all('a'):
    url = link.get('href')
    if "https" in url:
        print(url)
