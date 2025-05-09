"""
Example of scraping product classes from an ecommerce Site
which can be used to determine if a product is in stock or not
"""

# Standard Library Imports
from os import getenv

# Third-Party Imports
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
PRODUCT_PAGE = getenv("PRODUCT_PAGE")


def get_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def main():
    soup = get_html(PRODUCT_PAGE)
    ## Find all product elements on page
    # Select all <li> elements with class 'product'
    products = soup.select("li.product")
    ## Loop through each product element
    for product in products:
        try:
            ## Find product name
            product_name = product.select_one("a")["title"]
            ## Get classes for the prodct
            classes = product.get("class")
            print(f"{product_name} has classes: {classes} \n\n")

            if "outofstock" not in classes and "instock" not in classes:
                raise Exception(
                    "The bot is not logged into the site. Cannot retrieve product data."
                )
        except Exception as e:
            print(f"Error: {str(e)}")
            return


if __name__ == "__main__":
    main()
