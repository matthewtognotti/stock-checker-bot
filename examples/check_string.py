import requests
from bs4 import BeautifulSoup
import project_constants

def get_html():
    url = project_constants.MY_SITE
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def main():
    soup = get_html()
    if "Robot" in soup.text:
        print("true")
    else:
        print("false")
    
if __name__ == "__main__":
    main()