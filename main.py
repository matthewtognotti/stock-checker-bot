# Standard Library Imports
import asyncio
import logging
import time
import sys
from os import getenv

# Third-Party Imports
from telegram import Bot
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

# Local Imports
from constants import EXCLUDED_PRODUCTS


# Load environment variables from the .env file
load_dotenv()
LOGIN_PAGE = getenv("LOGIN_PAGE")
EMAIL = getenv("EMAIL")
PASSWORD = getenv("PASSWORD")
PRODUCT_PAGE = getenv("PRODUCT_PAGE")
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID")
COMPANY_NAME = getenv("COMPANY_NAME")

# Check if all required environment variables are set
if not all(
    [
        LOGIN_PAGE,
        EMAIL,
        PASSWORD,
        PRODUCT_PAGE,
        TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID,
        COMPANY_NAME,
    ]
):
    raise ValueError("Missing environment variables. Check your .env file.")


# Set up logging for the bot
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("stock_checker.log"), logging.StreamHandler()],
)


class Product:
    """Represents a product with a title, status, URL, and its product variants."""

    def __init__(self, title: str, status: str, url: str, variants: list):
        self.title = title
        self.status = status
        self.url = url
        self.variants = variants


class StockChecker:
    """
    A class to handle the login and scraping process. It interacts with the website
    using Selenium, logs in with provided credentials, and scrapes product stock data.
    """

    def __init__(self):
        # Set up the webdriver
        self.driver = webdriver.Chrome()
        self.products = []
        self.stock_count = 0

    def _scroll_into_view(self, element: WebElement) -> None:
        """
        Scrolls the browser window to bring the specified element into view.

        Args:
            element (WebElement): The element to scroll to.

        Returns:
            None
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def _handle_recaptcha(self) -> None:
        """
        Handles the reCAPTCHA challenge if it appears on the login page.

        If the reCAPTCHA is present, the function bypasses it by interacting with the
        reCAPTCHA checkbox. If it's not present, the function logs that reCAPTCHA
        was not found.

        Args:
            None

        Returns:
            None
        """
        try:
            # Wait for the iframe to be present and switch to it
            iframe = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
                )
            )
            self.driver.switch_to.frame(iframe)
            # Wait for the reCAPTCHA checkbox to be clickable and click it
            recaptcha_checkbox = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
            )
            self._scroll_into_view(recaptcha_checkbox)
            recaptcha_checkbox.click()
            logger.info("reCAPTCHA bypassed")

        except TimeoutException:
            # reCAPTCHA not present; skipping
            logger.info("reCAPTCHA not found")

        self.driver.switch_to.default_content()

    def _fill_input_field(self, field_name: str, value: str) -> None:
        """
        Helper function to find a field, scroll into view, and input
        the given value

        Args:
            field_name (str): The name of the input field to find.
            value (str): The value to input into the field.

        Returns:
            None
        """
        field_input = self.driver.find_element(By.NAME, field_name)
        self._scroll_into_view(field_input)
        field_input.send_keys(value)

    def login(self) -> bool:
        """
        Logs into the target website by submitting the login form with the
        provided credentials.

        It waits until the session cookie is set to confirm successful login.

        Args:
            None

        Returns:
            bool: True if login is successful, False otherwise.
        """
        logger.info("Starting login process")
        # Open the login page
        self.driver.get(LOGIN_PAGE)
        # Input the email
        self._fill_input_field("username", EMAIL)
        # Input Password
        self._fill_input_field("password", PASSWORD)

        self._handle_recaptcha()

        # Find and click the login button
        login_button = self.driver.find_element(By.NAME, "login")
        self._scroll_into_view(login_button)
        login_button.click()

        # After submitting the login form, we wait for the POST request to complete
        # and ensure that the the login session cookie is set before navigating
        # to the product page.
        try:
            # Wait until the session cookie is present
            WebDriverWait(self.driver, 10).until(lambda driver: self.is_logged_in())
            logger.info("Login successful. Session cookie found.")
            self.driver.get(
                PRODUCT_PAGE
            )  # Once logged in, navigate to the product page
            return True
        except TimeoutException:
            logger.error("Login failed: Session cookie not found.")
            return False

    def is_logged_in(self) -> bool:
        """
        Checks if the bot is logged in by looking for the WordPress session cookie.

        Args:
            None

        Returns:
            bool: True if logged in (session cookie found), False otherwise.
        """
        # Reference: https://developer.wordpress.org/advanced-administration/wordpress/cookies/
        cookies = self.driver.get_cookies()
        for c in cookies:
            if c["name"].startswith("wordpress_logged_in_"):
                return True
        return False

    def get_in_stock_variants(self, url: str) -> list:
        """
        Scrapes the product page for in-stock variants of a product.

        Given a product page URL, this function looks for variants that are in stock and
        returns a list of tuples containing the size and price.

        Args:
            url (str): The URL of the product page.

        Returns:
            list: A list of tuples containing the size and price of in-stock variants.
        """
        # Store the current window so we can return to it later
        product_window = self.driver.current_window_handle
        # Open the product page in a new tab
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        # Switch to the new window
        self.driver.switch_to.window(self.driver.window_handles[1])
        # Wait until the product varaints are loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-form-row"))
        )
        # Locate all product variants
        variants = self.driver.find_elements(By.CLASS_NAME, "product-form-row")
        in_stock_variants = []

        # Iterate through each variant
        for variant in variants:
            # Check if the variant is in stock
            stock_status = variant.find_element(
                By.TAG_NAME, "p"
            )  # Locate the stock status element

            if "in-stock" in stock_status.get_attribute("class"):
                # Extract size
                size = (
                    variant.find_element(By.CLASS_NAME, "pa-size")
                    .find_element(By.TAG_NAME, "dd")
                    .text.strip()
                )
                # Extract price (USD)
                # us_price = variant.find_element(By.CLASS_NAME, "woocs_price_USD")
                currency_symbol = variant.find_element(
                    By.CLASS_NAME, "woocommerce-Price-currencySymbol"
                ).text
                whole_price = variant.find_element(
                    By.CLASS_NAME, "woocommerce-Price-amount"
                ).text
                decimal_price = variant.find_element(
                    By.CLASS_NAME, "woocommerce-Price-decimal"
                ).text

                price = whole_price + decimal_price

                # Append the variant details as a tuple
                in_stock_variants.append((size, price))

        # Close the current window and switch back to the product window
        self.driver.close()
        self.driver.switch_to.window(product_window)
        return in_stock_variants

    def get_products(self) -> None:
        """
        Scrapes the product data from the product page and updates the list of products.

        It goes through all product elements, checks stock status, and appends the
        relevant product data to the `self.products` list.

        Args:
            None

        Returns:
            None
        """
        logger.info("Scraping product data")
        # Keep track of the number of in stock items
        self.stock_count = 0
        # Clear old data from last update
        self.products.clear()

        product_elements = self.driver.find_elements(By.CSS_SELECTOR, "li.product")

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
        Formats the stock data into a message to be sent via Telegram.

        It creates a human-readable message that includes information about
        products that are in stock, including their sizes, prices, and URLs.

        Args:
            None

        Returns:
            str: The formatted message to be sent.
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
        logger.info(f"Formatted Message Created")
        return message

    def quit(self) -> None:
        """
        Closes the WebDriver and shuts down the bot.

        It terminates the browser session to clean up resources after
        the bot has finished.

        Args:
            None

        Returns:
            None
        """
        logger.info("Closing Webdriver")
        self.driver.quit()


class TelegramBot:
    """A simple wrapper for interacting with the Telegram Bot API to send messages."""

    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)

    async def send_message(self, message: str) -> None:
        """
        Sends a message to the specified Telegram chat.

        Args:
            message (str): The message content to send.

        Returns:
            None
        """
        await self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


async def handle_login_failure(bot: TelegramBot, checker: StockChecker) -> None:
    """
    Sends a failure alert and shuts down the bot gracefully after login failure.

    Args:
        bot (TelegramBot): The Telegram bot used to send messages.
        checker (StockChecker): The stock checker instance to quit.

    Returns:
        None
    """
    await bot.send_message("⚠️ Login failed. Manual intervention required.")
    logger.info("The Bot was not able to log in. Shutting down.")
    checker.quit()
    # Exit early, since login failed we don't want to try continuously
    # and get rate limited.
    sys.exit(1)


async def main():
    """Main loop that runs the stock checker bot.

    Logs into the website, checks stock periodically, and sends
    Telegram alerts for in-stock products. Handles re-login if
    logged out. Runs until manually stopped.
    """
    logger.info("The Bot has started")
    checker = StockChecker()
    bot = TelegramBot()

    if not checker.login():
        await handle_login_failure(bot, checker)

    try:
        while True:
            try:
                # Confirm the bot is logged in because it gets auto logged out
                # by the site after 24 hours
                if checker.is_logged_in() is False:
                    logger.info("Bot was logged out, logging in")
                    # Try to re-login. If it fails, then exit and don't try again
                    if not checker.login():
                        await handle_login_failure(bot, checker)
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
                await asyncio.sleep(60)  # Delay between scrapes
                checker.driver.refresh()  # Refresh the page to update the stock data

    except KeyboardInterrupt:
        logger.info("Process interrupted by Keyboard. Shutting down")
    except Exception as e:
        logger.exception(f"Unhandled exception in main loop: {e}")
    finally:
        checker.quit()
        logger.info("Shutting down")
        await bot.send_message("Bot has shut down")


if __name__ == "__main__":
    asyncio.run(main())
