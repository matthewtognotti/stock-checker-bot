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
        ## Find product name
        product_name = product.select_one("a.woocommerce-loop-product__link")["title"]
        ## Find the status using the classes 'outofstock' or 'instock' used on the website
        product_status = "Out of stock"
        if "instock" in product.get("class"):
            product_status = "In stock"
        print(f"{product_name} is {product_status}")
        
if __name__ == "__main__":
    main()