from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import project_constants


def login():
    # Set up the webdriver
    driver = webdriver.Chrome()

    # Open Google
    driver.get(project_constants.LOGIN_PAGE)

    # Find the email address input and input the email
    email_input = driver.find_element(By.NAME, "username")
    email_input.send_keys(project_constants.EMAIL)

    # Find the password input and input the password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(project_constants.PASSWORD)

    # Find the captcha and Click the captcha box

    # Find the log in button and click the log in button
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    # Wait to see the results
    time.sleep(100)

    # Close the browser
    driver.quit()


def main():
    login()

if __name__ == "__main__":
    main()