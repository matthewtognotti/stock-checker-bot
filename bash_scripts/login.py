from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from os import getenv
import time


''' For logging into the site from terminal using a shell script for convenience'''

# Environment variables and secrets 
load_dotenv()
LOGIN_PAGE = getenv("LOGIN_PAGE")
EMAIL = getenv("EMAIL")
PASSWORD = getenv("PASSWORD")
PRODUCT_PAGE = getenv("PRODUCT_PAGE")

if not all([LOGIN_PAGE, EMAIL, PASSWORD, PRODUCT_PAGE]):
    raise ValueError("Missing environment variables. Check your .env file.")

class Login:
    def __init__(self):
        # Set up the webdriver
        self.driver = webdriver.Chrome()
        
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
            iframe = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
            self.driver.switch_to.frame(iframe)
            # Wait for the reCAPTCHA checkbox to be clickable and click it
            recaptcha_checkbox = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
            self._scroll_into_view(recaptcha_checkbox)
            recaptcha_checkbox.click()
            
        except TimeoutException:
            # reCAPTCHA not present; skipping
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
        
        driver.get(PRODUCT_PAGE)

    def quit(self):
        self.driver.quit


def main():

    bot = Login()
    
    try:
        print("\nLogging in...\n")
        bot.login()  
        
    except KeyboardInterrupt:
        print("\nExiting bot...\n")
        bot.quit()
    
    time.sleep(60 * 60 * 24)
        
if __name__ == "__main__":
    main()
    
    
    
    
    