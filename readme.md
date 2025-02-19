# Stock Checker Bot with Telegram Notifications 

This script automates the process of checking product stock on a website that requires login to view stock data. If any items are in stock, the bot sends a notification of the products in stock to the user via Telegram. The bot operates during specified business hours (9:00 AM to 5:30 PM Japan Time) on weekdays.

---

## Table of Contents
- [Stock Checker Bot with Telegram Notifications](#stock-checker-bot-with-telegram-notifications)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Set Up](#set-up)
  - [Code Structure](#code-structure)
  - [Customization](#customization)
  - [Troubleshooting](#troubleshooting)
  - [Further Improvements](#further-improvements)
  - [License](#license)

---

## Features

- **Login Automation**: Logs into the website using Selenium to access stock data.
- **Stock Monitoring**: Scrapes product data and checks stock status every minute.
- **Telegram Notifications**: Sends a message to the user via Telegram if any items are in stock.
- **Business Hours Check**: Only operates during specified business hours (9:00 AM to 5:30 PM Japan Time) on weekdays.

---

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.x**: The script is written in Python.
2. **Selenium**: Install Selenium using pip:
    ```bash
    pip install selenium 
    ```
3. Telegram Bot: Create a Telegram bot and obtain the bot token and chat ID.
4. ChromeDriver: Download and install ChromeDriver that matches your Chrome browser version.
5. Environment Variables: Set up the required environment variables in a .env file.

---

## Set Up

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/stock-checker-bot.git
    cd stock-checker-bot
    ```
2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add the following variables:
    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```
4. **Run the Script**:
    ```bash
    python stock_checker_bot.py
    ```

---

## Code Structure

- StockChecker Class: Handles the login, product data scraping, and stock checking.
- TelegramBot Class: Manages sending messages via Telegram.
- main Function: Orchestrates the stock checking and notification process.

---

## Customization
- Excluded Products: Add product titles to the EXCLUDED_PRODUCTS list in constants.py to exclude them from stock checks.
- Business Hours: Modify the japan_business_hours function to adjust the operating hours.

---

## Troubleshooting
- ChromeDriver Issues: Ensure that the ChromeDriver version matches your Chrome browser version.

- Login Failures: Verify that the login credentials and page elements (e.g., email input, password input) are correctly specified.

- Telegram Notifications: Ensure that the Telegram bot token and chat ID are correctly set in the .env file.


---

## Further Improvements
- [ ] Clean up code and create new repo possibly? to showcase the project. Good comments and documentation. 
- [ ] Format message to send product link and organized in a table.
- [ ] Allow the user to send /update and give a table with all the products that are in stock or respond no products are in stock.
- [ ] **Add Error Handling**: Implement robust error handling for login failures, network issues, and Telegram API errors.
- [ ] **Add Logging**: Implement a logging system to track bot activity, errors, and stock updates.
- [ ] **Add Multi-User Support**: Allow multiple Telegram users to receive notifications by managing a list of chat IDs.
- [ ] Enable a user to prompt the bot to send a full list of products in stock. 


---

Note: This script is intended for educational purposes. Ensure you comply with the terms of service of the website you are automating.


## License
This project is licensed under the MIT License. See the LICENSE file for details.



