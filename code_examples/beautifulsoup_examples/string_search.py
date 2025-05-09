"""Search for a string on an HTML page using Beautiful Soup"""

# Standard Library Imports
from os import getenv

# Third-Party Imports
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
MY_SITE = getenv("MY_SITE")


def get_html():
    url = MY_SITE
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def main():
    soup = get_html()
    if "Robot" in soup.text:
        print("true")
    else:
        print("false")


if __name__ == "__main__":
    main()
