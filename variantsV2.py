from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


driver = webdriver.Chrome()

# Use JavaScript to scroll the element into view
def scroll_into_view(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def login():
    

    # Open the log in page
    driver.get(LOGIN_PAGE)

    # Find the email address input and input the email
    email_input = driver.find_element(By.NAME, "username")
    scroll_into_view(email_input)
    email_input.send_keys(EMAIL)

    # Find the password input and input the password
    password_input = driver.find_element(By.NAME, "password")
    scroll_into_view(password_input)
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
    scroll_into_view(recaptcha_checkbox)
    recaptcha_checkbox.click()

    # Switch back to the main content and click the login button
    driver.switch_to.default_content()
    login_button = driver.find_element(By.NAME, "login")
    scroll_into_view(login_button)
    login_button.click()



# for variant in variant_elements:
#     # Extract the variant name and price
#     name = variant.find_element(By.TAG_NAME, "dd").text
#     price_main = variant.find_element(By.TAG_NAME, "bdi").text
#     price_decimal = variant.find_element(By.CSS_SELECTOR, "woocommerce-Price-decimal").text
#     price = price_main + price_decimal
#     variants.append({name, price})
#     print({name, price})


# Function to extract in-stock product variants
def get_in_stock_variants(url):
    
    # Open the product page
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-form-row")))
 
    # Locate all product variants
    variants = driver.find_elements(By.CLASS_NAME, "product-form-row")

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

    return in_stock_variants



# Example usage
if __name__ == "__main__":
    
    login()
    
    product_url = "https://www.marukyu-koyamaen.co.jp/english/shop/products/1d9d000cc?currency=USD"
    in_stock_variants = get_in_stock_variants(product_url)
        
     # Print the results
    if in_stock_variants:
        for variant in in_stock_variants:
            print(f"Size: {variant[0]}, Price: {variant[1]}")
    else:
        print("No in-stock variants found.")
        
    driver.quit()