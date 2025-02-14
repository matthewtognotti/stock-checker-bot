from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import project_constants

# Initialize the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

# Open the target webpage
driver.get(project_constants.LOGIN_PAGE)

try:
    # Wait until the iframe containing reCAPTCHA is present
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
    )

    # Wait until the reCAPTCHA checkbox is clickable
    recaptcha_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "div.recaptcha-checkbox-border"))
    )

    # Click the reCAPTCHA checkbox
    recaptcha_checkbox.click()

    # Switch back to the default content
    driver.switch_to.default_content()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()