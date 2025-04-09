from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    
    
    
    
    