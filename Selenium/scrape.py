import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Product:
    def __init__(self, title, status):
        self.title = title
        self.status = status

class StockChecker:
    def __init__(self):
        self.products = []
        self.base_url = "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/principal/"

    def scrape_products(self):
        # Set up ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            # Open the target page
            driver.get(self.base_url)

            # Wait for the page to load
            time.sleep(3)  # Adjust the sleep time as needed

            # Find all product elements
            product_elements = driver.find_elements(By.CSS_SELECTOR, "li.product")

            for product in product_elements:
                # Extract product title
                title_element = product.find_element(By.CSS_SELECTOR, "a.woocommerce-loop-product__link")
                title = title_element.get_attribute("title")

                # Check stock status
                status = "❌ Out of Stock"
                if "outofstock" not in product.get_attribute("class"):
                    status = "✅ In Stock"

                # Add product to the list
                self.products.append(Product(title, status))

        finally:
            # Close the browser
            driver.quit()

    def format_message(self):
        time = time.strftime("%a, %d %b %I:%M %p", time.localtime())
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