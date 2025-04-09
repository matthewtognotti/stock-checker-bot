from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import pytz
import asyncio
from telegram import Bot
from constants import EXCLUDED_PRODUCTS
from dotenv import load_dotenv
from os import getenv
import logging


load_dotenv()
LOGIN_PAGE = getenv("LOGIN_PAGE")
EMAIL = getenv("EMAIL")
PASSWORD = getenv("PASSWORD")
PRODUCT_PAGE = getenv("PRODUCT_PAGE")
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID")
COMPANY_NAME = getenv("COMPANY_NAME")


if not all([LOGIN_PAGE, EMAIL, PASSWORD, PRODUCT_PAGE, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, COMPANY_NAME]):
    raise ValueError("Missing environment variables. Check your .env file.")


class Product:
    def __init__(self, title, status, url, variants):
        self.title = title
        self.status = status
        self.url = url
        self.variants = variants
        

class StockChecker:
    def __init__(self):
        # Set up the webdriver
        self.driver = webdriver.Chrome()
        self.products = []
        self.stock_count = 0
        
    # Use JavaScript to scroll the element into view
    def _scroll_into_view(self, element) -> None:
        """ Scroll to an element on the page using Javascript """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def _handle_recaptcha(self) -> None:
        """ 
        Sometimes the reCAPTCHA iframe isn't present, so WebDriverWait throws an exception. 
        
        This bypasses the reCaptcha everytime, so we don't have to solve it
        """
        try:
            # Wait for the iframe to be present and switch to it
            iframe = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
            self.driver.switch_to.frame(iframe)
            # Wait for the reCAPTCHA checkbox to be clickable and click it
            recaptcha_checkbox = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
            self._scroll_into_view(recaptcha_checkbox)
            recaptcha_checkbox.click()
            
        except TimeoutException:
            # reCAPTCHA not present; skipping
            logging.debug("reCAPTCHA not found; continuing without interaction.")
            pass
        
        self.driver.switch_to.default_content()
        
    def _input_field(self, field_name, value):
        """Helper function to find a field, scroll into view, and input a value"""
        field_input = self.driver.find_element(By.NAME, field_name)
        self._scroll_into_view(field_input)
        field_input.send_keys(value)
           
    def login(self) -> None:
        driver = self.driver
        
        # Open the log in page
        driver.get(LOGIN_PAGE)
        
        # Input the email
        self._input_field("username", EMAIL)
        # Input Password
        self._input_field("password", PASSWORD)
        
        self._handle_recaptcha()
    
        # Find and click the log in button to finsh signing in
        login_button = driver.find_element(By.NAME, "login")
        self._scroll_into_view(login_button)
        login_button.click()
    
    def is_logged_in(self) -> bool:
        """ TODO: Implement this """
        pass
    
    def get_in_stock_variants(self, url : str) -> list:

        """
        Given the proudct page URL, return the product variants 
        that are in stock in a list of tuples with the prices
        
        List of tuples chosen over ordered hash map because we need to iterate
        over the variants and do not need fast look up, insertions, deletions. 
        """
        
        # Open the product page in a new tab (window)
        product_window = self.driver.current_window_handle
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        
        # Switch to the new window
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-form-row")))
    
        # Locate all product variants
        variants = self.driver.find_elements(By.CLASS_NAME, "product-form-row")

        in_stock_variants = []

        # Iterate through each variant
        for variant in variants:
            # Check if the variant is in stock
            stock_status = variant.find_element(By.TAG_NAME, "p")  # Locate the stock status element
        
            if "in-stock" in stock_status.get_attribute("class"): 
                # Extract size
                size = variant.find_element(By.CLASS_NAME, "pa-size").find_element(By.TAG_NAME, "dd").text.strip()
                # Extract price (USD)
               # us_price = variant.find_element(By.CLASS_NAME, "woocs_price_USD")
                currency_symbol = variant.find_element(By.CLASS_NAME, "woocommerce-Price-currencySymbol").text
                whole_price = variant.find_element(By.CLASS_NAME, "woocommerce-Price-amount").text
                decimal_price = variant.find_element(By.CLASS_NAME, "woocommerce-Price-decimal").text       
               
                price = whole_price + decimal_price
                                
                # Append the variant details as a tuple
                in_stock_variants.append((size, price))

        # Close the current window and switch back to the product window
        self.driver.close()
        self.driver.switch_to.window(product_window)
        return in_stock_variants
    
    def get_products(self) -> None:
        driver = self.driver
        # Keep track of the number of in stock items
        self.stock_count = 0
        
        # Now go to the product page
        driver.get(PRODUCT_PAGE)
        product_elements = driver.find_elements(By.CSS_SELECTOR, "li.product")
        
        # Clear old data from last update
        self.products.clear()
        
        for product in product_elements:
            # Extract product title and url
            title_element = product.find_element(By.CSS_SELECTOR, "a")
            title = title_element.get_attribute("title")
            url = title_element.get_attribute("href")
            
            # if title in EXCLUDED_PRODUCTS:
            #     continue
            
            # Check stock status
            status = "Out of Stock"
            variants = []
            if "instock" in product.get_attribute("class"):
                status = "In Stock"
                variants = self.get_in_stock_variants(url)
                self.stock_count += 1
                
            # Add product to the product list
            self.products.append(Product(title, status, url, variants))
            
    
    def format_message(self) -> str:
        formatted_time = time.strftime("%a, %d %b %I:%M %p", time.localtime())
        message = COMPANY_NAME + " Stock Check\n\n"
        message += f"🕜 Last Checked: {formatted_time}\n\n"
        
        for product in self.products:

            if product.status == "In Stock":
                message += f"🍵 Name: {product.title}\n✅ Status: {product.status}\n"
                
                for size, price in product.variants:
                    message += f"➡️ {size}: {price}\n"
                
                message += f"🔗 Link: {product.url}\n\n"
                    
        return message
    
    def quit(self) -> None:
        """ Close the driver/browser """
        self.driver.quit()
        
                    
class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)

    async def send_message(self, message) -> None:
        # Await the coroutine to properly send the message
        await self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


def main():
    # bot = TelegramBot()
    checker = StockChecker()
    checker.login()
    
    # Send message to user via Telegram
    # asyncio.run(bot.send_message("The bot has successfully started"))
    logging.info("The Bot is up and running")
    
    try:
        while True:
            
            # Refresh the page to update the stock data
            checker.driver.refresh()
            
            # Ensure the bot is logged in becuase it gets auto logged out by the site
            # after 24 hours
            # if checker.is_logged_in() is False:
            #     checker.login()
            
            # Scrape product data
            checker.get_products()
            
            # Only message the user if at least one item is in stock
            if checker.stock_count > 0:
                message = checker.format_message()
                # Send message to user via Telegram
                bot = TelegramBot()
                asyncio.run(bot.send_message(message))
        
            time.sleep(60) # Sleep for 1 minute
            
    except KeyboardInterrupt:
        checker.quit()
        asyncio.run(bot.send_message("The bot has been shut off..."))
        logging.info("Process interrupted by Keyboard. Closing WebDriver.")
        
    
if __name__ == "__main__":
    main()