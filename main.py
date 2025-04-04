from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pytz
import asyncio
from telegram import Bot
from constants import EXCLUDED_PRODUCTS
from dotenv import load_dotenv
from os import getenv
import logging

# Environment variables and secrets 
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
        self.variants = []
        

class StockChecker:
    def __init__(self):
        # Set up the webdriver
        self.driver = webdriver.Chrome()
        self.products = []
        self.stock_count = 0
        
    # Use JavaScript to scroll the element into view
    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        
    def login(self):
        driver = self.driver
        
        # Open the log in page
        driver.get(LOGIN_PAGE)
        
        # Find the email address input and input the email
        email_input = driver.find_element(By.NAME, "username")
        self.scroll_into_view(email_input)
        email_input.send_keys(EMAIL)
        
        # Find the password input and input the password
        password_input = driver.find_element(By.NAME, "password")
        self.scroll_into_view(password_input)
        password_input.send_keys(PASSWORD)
        
        # Wait for the iframe to be present and switch to it
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
        )
        driver.switch_to.frame(iframe)
        # Wait for the reCAPTCHA checkbox to be clickable and click it
        recaptcha_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
        )
        self.scroll_into_view(recaptcha_checkbox)
        recaptcha_checkbox.click()
        
        # Switch back to the main content and click the login button
        driver.switch_to.default_content()
        login_button = driver.find_element(By.NAME, "login")
        self.scroll_into_view(login_button)
        login_button.click()
    
    # Check if logged in
    def is_logged_in(self) -> bool:
        pass
    

    # Given the proudcts URL, return the product variants 
    # that are in stock in a list of tuples with the prices
    # List of tuples chosen over ordered hash map because we need to iterate
    # over the variants and do not need fast look up, insertions, deletions. 
    def get_in_stock_variants(self, url : str) -> list:
        
        # Open the product page
        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-form-row")))
    
        # Locate all product variants
        variants = self.driver.find_elements(By.CLASS_NAME, "product-form-row")

        in_stock_variants = []

        # Iterate through each variant
        for variant in variants:
            # Check if the variant is in stock
            stock_status = variant.find_element(By.TAG_NAME, "p")  # Locate the stock status element
        
            if "in-stock" in stock_status.get_attribute("class"):  # Check if the text contains "In stock"
                # Extract size
                size = variant.find_element(By.CLASS_NAME, "pa-size").find_element(By.TAG_NAME, "dd").text.strip()
                # Extract price (USD)
                price = variant.find_element(By.CLASS_NAME, "woocs_price_USD").text.strip()
                # Append the variant details as a tuple
                in_stock_variants.append((size, price))

        # RETURN TO THE MAIN PAGE BUG HERE TODO: FIX THIS
        self.driver.get(PRODUCT_PAGE)
        
        return in_stock_variants
    
    
    def get_products(self):
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
            status = "❌ Out of Stock"
            variants = []
            if "instock" in product.get_attribute("class"):
                status = "✅ In Stock"
                variants = self.get_in_stock_variants(url)
                self.stock_count += 1
                
            # Add product to the product list
            self.products.append(Product(title, status, url, variants))
    
    
    def format_message(self):
        formatted_time = time.strftime("%a, %d %b %I:%M %p", time.localtime())
        message = COMPANY_NAME + " Stock Check\n\n"
        message += f"🕜 Last Checked: {formatted_time}\n\n"
        
        for product in self.products:
            
            if product.status == "✅ In Stock":
                message += f"🍵 Name: {product.title}\n📦 Status: {product.status}\n Link: {product.url}\n\n"
                
                for size, price in self.products.variants:
                    message += f"Size: {size} --- Price{price}\n"
                    
        return message
    
    def quit(self):
        # Close the driver/browser
        self.driver.quit()
        
                    
class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)

    async def send_message(self, message):
        # Await the coroutine to properly send the message
        await self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Only send stock updates during 9am to 5:30pm (Japan Time) during weekdays 
def japan_business_hours():
    # Define the Japan timezone
    japan_tz = pytz.timezone('Asia/Tokyo')
    
    # Get the current time in Japan
    now_in_japan = datetime.now(japan_tz)
    
    # Check if it's a weekday (Monday = 0, Sunday = 6)
    if now_in_japan.weekday() >= 5:  # Saturday (5) or Sunday (6)
        return False
    
    # Define business hours (9:00 AM to 5:30 PM)
    start_time = now_in_japan.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = now_in_japan.replace(hour=17, minute=30, second=0, microsecond=0)
    
    # Check if the current time is within business hours
    return start_time <= now_in_japan <= end_time


def main():
    bot = TelegramBot()
    checker = StockChecker()
    checker.login()
    
    # Send message to user via Telegram
    asyncio.run(bot.send_message("The bot has successfully started"))
    logging.info("The Bot is up and running")
    
    try:
        while True:
            if japan_business_hours():
            
                # Refresh the page to update the stock data
                checker.driver.refresh()
                
                # Ensure the bot is logged in becuase it gets auto logged out by the site
                # after 24 hours
                # if checker.is_logged_in() is False:
                #     checker.login()
                
                # Scrape product data
                checker.get_products()
                
                # Only message the user if at least one item is in stock,
                # else don't send a message
                if checker.stock_count > 0:
                    message = checker.format_message()
                    # Send message to user via Telegram
                    asyncio.run(bot.send_message(message))
            
            time.sleep(60) # Sleep for 1 minute
            
    except KeyboardInterrupt:
        checker.quit()
        asyncio.run(bot.send_message("The bot has been shut off..."))
        logging.info("Process interrupted by Keyboard. Closing WebDriver.")
        
    
if __name__ == "__main__":
    main()
    
    
    
    
    