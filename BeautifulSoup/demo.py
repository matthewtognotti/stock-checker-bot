import time
import requests
from bs4 import BeautifulSoup
import project_constants

class Product:
    def __init__(self, title, status):
        self.title = title
        self.status = status

class StockChecker:
    def __init__(self):
        self.products = []
        self.base_url = project_constants.PRODUCT_PAGE

    def scrape_products(self):
        response = requests.get(self.base_url)
        
        # if response.status_code != 200:
        #     raise Exception(f"Failed to fetch products: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        product_elements = soup.select("li.product")

        for product in product_elements:
            title = product.select_one("a")["title"]
            status = "❌ Out of Stock"
            if "outofstock" not in product.get("class", []):
                status = "✅ In Stock"
            self.products.append(Product(title, status))

    def format_message(self):
        # time= time.strftime("%a, %d %b %I:%M %p", time.localtime())
        message = "Marukyu Koyamaen Stock Check:\n\n"
        message += f"🕜 Last Checked: {time}\n\n"

        for product in self.products:
            message += f"🍵 Name: {product.title}\n📦 Status: {product.status}\n\n"

        return message

def handle_request():
    checker = StockChecker()

    try:
        checker.scrape_products()
        message = checker.format_message()
        print(message)
        return "OK"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = handle_request()
    print(result)