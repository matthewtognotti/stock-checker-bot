import requests
from bs4 import BeautifulSoup

url = "https://www.matthewtognotti.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup)

element = soup.find(id="videos")
print(element)
