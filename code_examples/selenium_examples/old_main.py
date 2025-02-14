from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import project_constants


# products
# login method
# get product data method
# format message method
    

def login():
    # Set up the webdriver
    driver = webdriver.Chrome()
    # Open the log in page
    driver.get(project_constants.LOGIN_PAGE)
    # Find the email address input and input the email
    email_input = driver.find_element(By.NAME, "username")
    email_input.send_keys(project_constants.EMAIL)
    # Find the password input and input the password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(project_constants.PASSWORD)
    time.sleep(1.25) # Crashes without this delay... Fix that. 
    # Wait for the iframe to be present and switch to it
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
    )
    driver.switch_to.frame(iframe)
    # Wait for the reCAPTCHA checkbox to be clickable and click it
    recaptcha_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
    )
    recaptcha_checkbox.click()
    # Switch back to the main content
    driver.switch_to.default_content()
    # Find the log in button and click the log in button
    time.sleep(2)
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    
    
    # Now go to the product page
    driver.get(project_constants.PRODUCT_PAGE)
    # Scrape product data and print it
    product_elements = driver.find_elements(By.CSS_SELECTOR, "li.product")
    products = []
    
    for product in product_elements:
        # Extract product title
        title_element = product.find_element(By.CSS_SELECTOR, "a")
        title = title_element.get_attribute("title")
        # Check stock status
        status = "❌ Out of Stock"
        if "outofstock" not in product.get_attribute("class"):
            status = "✅ In Stock"
        print(f"{title} is {status}")
    
    # Wait to see the results
    time.sleep(60)

    # Close the browser
    driver.quit()


def main():
    login()

if __name__ == "__main__":
    main()