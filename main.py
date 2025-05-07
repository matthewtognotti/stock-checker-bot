import asyncio
import logging
import time
from datetime import datetime
from telegram import Bot
from constants import EXCLUDED_PRODUCTS
from dotenv import load_dotenv
from os import getenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

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

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("stock_checker.log"),
        logging.StreamHandler()                   
    ]
)

class Product:
    """       
    """
    def __init__(self, title, status, url, variants):
        self.title = title
        self.status = status
        self.url = url
        self.variants = variants
        
class StockChecker:
    """       
    """
    def __init__(self):
        # Set up the webdriver
        self.driver = webdriver.Chrome()
        self.products = []
        self.stock_count = 0
        
    def _scroll_into_view(self, element) -> None:
        """Scroll to an element on the page using Javascript"""
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def _handle_recaptcha(self) -> None:
        """ 
        Sometimes the reCAPTCHA iframe is present, sometimes it isn't.
        This bypasses the reCaptcha everytime, so we don't have to solve it.
        """
        try:
            # Wait for the iframe to be present and switch to it
            iframe = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
            self.driver.switch_to.frame(iframe)
            # Wait for the reCAPTCHA checkbox to be clickable and click it
            recaptcha_checkbox = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
            self._scroll_into_view(recaptcha_checkbox)
            recaptcha_checkbox.click()
            logger.info("reCAPTCHA bypassed")
            
        except TimeoutException:
            # reCAPTCHA not present; skipping
            logger.info("reCAPTCHA not found")
        
        self.driver.switch_to.default_content()
        
    def _input_field(self, field_name, value):
        """Helper function to find a field, scroll into view, and input a value"""
        field_input = self.driver.find_element(By.NAME, field_name)
        self._scroll_into_view(field_input)
        field_input.send_keys(value)
           
    def login(self) -> None:
        """
        Logs the bot into the target website
        Confirms successful log in by checking for a log in session cookie.
        """
        logger.info("Starting log in process")
        # Open the log in page
        self.driver.get(LOGIN_PAGE)
        # Input the email
        self._input_field("username", EMAIL)
        # Input Password
        self._input_field("password", PASSWORD)
        
        self._handle_recaptcha()
    
        # Find and click the log in button
        login_button = self.driver.find_element(By.NAME, "login")
        self._scroll_into_view(login_button)
        login_button.click()
        # Wait for the form to be submitted, then get the product page
        time.sleep(2) #TODO: Remove this sleep
        self.driver.get(PRODUCT_PAGE)
        
        # Now, we confirm that the log in was successful by checking for the session cookie
        if self.is_logged_in(): 
            logger.info("Log in successful")
            return
        else:
            logger.error("Log in failed")
    
    def is_logged_in(self) -> bool:
        """
        Checks if the bot is currently logged in by checking 
        for the wordpress_logged_in_* session cookie: 
            - https://cookiedatabase.org/cookie/wordpress/wordpress_logged_in_/
            - https://developer.wordpress.org/advanced-administration/wordpress/cookies/
        Returns True if logged in, False otherwise.
        """
        cookies = self.driver.get_cookies()
        for c in cookies:
            if c['name'].startswith('wordpress_logged_in_'):
                return True
        return False
    
    def get_in_stock_variants(self, url : str) -> list:
        """
        Given the proudct page URL, return the product variants 
        that are in stock in a list of tuples with the prices.
        
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
        """ 
        Scrapes product data from the product page appends the relevent data to product list.
        """
        logger.info("Scraping product data")
        driver = self.driver
        # Keep track of the number of in stock items
        self.stock_count = 0
        
        product_elements = driver.find_elements(By.CSS_SELECTOR, "li.product")
        
        # Clear old data from last update
        self.products.clear()
        
        for product in product_elements:
            # Extract product title and url
            title_element = product.find_element(By.CSS_SELECTOR, "a")
            title = title_element.get_attribute("title")
            url = title_element.get_attribute("href")
            
            if title in EXCLUDED_PRODUCTS:
                continue
            
            # Check stock status
            status = "Out of Stock"
            variants = []
            if "instock" in product.get_attribute("class"):
                variants = self.get_in_stock_variants(url)
                # Product is only in stock if it has at least one variant
                if len(variants) >= 1:
                    status = "In Stock"
                    self.stock_count += 1 
                
            # Add product to the product list
            self.products.append(Product(title, status, url, variants))
            
        logger.info(f"{self.stock_count} products in stock")
            
    def format_message(self) -> str:
        """ 
        Format the Telegram text message to the user based on the stock data.
        Returns string to send as text message using the Telegram API.
        """
        formatted_time = time.strftime("%a, %d %b %I:%M %p", time.localtime())
        message = COMPANY_NAME + " Stock Check\n\n"
        message += f"🕜 Last Checked: {formatted_time}\n\n"
        
        for product in self.products:

            if product.status == "In Stock":   
                message += f"🍵 Name: {product.title}\n✅ Status: {product.status}\n"
                
                for size, price in product.variants:
                    message += f"➡️ {size}: {price}\n"
                
                message += f"🔗 Link: {product.url}\n\n"
        logger.info(f"Formatted Message Created:\n{message}")           
        return message
    
    def quit(self) -> None:
        """ Close the driver/browser """
        logger.info("Bot is shutting down")
        self.driver.quit()
                          
class TelegramBot:
    """       
    """
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)

    async def send_message(self, message) -> None:
        # Await the coroutine to properly send the message
        await self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


async def main():
    """       
    """
    logger.info("The Bot has started")
    checker = StockChecker()
    checker.login()
    bot = TelegramBot()
    try:
        while True:
            try:
                # Ensure the bot is logged in becuase it gets auto logged out by the site after 24 hours
                if checker.is_logged_in() is False:
                    logger.info("Bot was logged out, logging back in")
                    checker.login()
                # Scrape product data
                checker.get_products()
                # Only message the user if at least one item is in stock
                if checker.stock_count > 0:
                    message = checker.format_message()
                    await bot.send_message(message)
            except Exception as e:
                logger.exception("Error in main loop. Restarting to self-heal in 60s")
                checker.quit()
                checker = StockChecker()
                checker.login()
            finally:
                await asyncio.sleep(60)
                # Refresh the page to update the stock data
                checker.driver.refresh()
            
    except KeyboardInterrupt:
        logger.info("Process interrupted by Keyboard. Shutting down")
    except Exception as e:
        logger.exception(f"Unhandled exception in main loop")
    finally:
        checker.quit()
        await bot.send_message("Bot has shut down")
        
    
if __name__ == "__main__":
    asyncio.run(main())