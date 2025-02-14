# Get the class names of each product

import requests
from bs4 import BeautifulSoup
import project_constants

def get_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def main():
    
    soup = get_html(project_constants.PRODUCT_PAGE)
    
    ## Find all product elements on page
    products = soup.select("li.product") # Select all <li> elements with class 'product'
    
    ## Loop through each product element
    for product in products:
        try:
            ## Find product name
            product_name = product.select_one("a")["title"]
            ## Get classes for the prodct
            classes = product.get("class")
            print(f"{product_name} has classes: {classes} \n\n")
            
            if "outofstock" not in classes and "instock" not in classes:
                raise Exception("The bot is not logged into the site. Cannot retrieve product data.")

        except Exception as e:
            print(f"Error: {str(e)}")
            return
                
if __name__ == "__main__":
    main()