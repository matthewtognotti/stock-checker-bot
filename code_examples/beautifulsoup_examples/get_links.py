"""Example of extracting all links from an HTML page"""

# Standard Library Imports
from os import getenv

# Third-Party Imports
from bs4 import BeautifulSoup
import requests
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
MY_SITE = getenv("MY_SITE")

url = MY_SITE
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract all links
for link in soup.find_all("a"):
    url = link.get("href")
    if "https" in url:
        print(url)
