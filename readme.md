# 🛒 Stock Checker Bot with Telegram Notifications

This script automates the process of checking product stock on a website that requires login to view stock data. If any items are in stock, the bot sends a notification of the products in stock to the user via Telegram. The bot operates during specified business hours (9:00 AM to 5:30 PM Japan Time) on weekdays.

---

## 📑 Table of Contents
- [🛒 Stock Checker Bot with Telegram Notifications](#-stock-checker-bot-with-telegram-notifications)
  - [📑 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [📋 Prerequisites](#-prerequisites)
  - [⚙️ Set Up](#️-set-up)
  - [🧩 Code Structure](#-code-structure)
  - [🎨 Customization](#-customization)
  - [🛠 Troubleshooting](#-troubleshooting)
  - [🚀 Further Improvements](#-further-improvements)
  - [Now](#now)
  - [Future](#future)
  - [📜 License](#-license)

---

## ✨ Features

- **Login Automation**: Logs into the website using Selenium to access stock data.
- **Stock Monitoring**: Scrapes product data and checks stock status every minute.
- **Telegram Notifications**: Sends a message to the user via Telegram if any items are in stock.
- **Business Hours Check**: Only operates during specified business hours (9:00 AM to 5:30 PM Japan Time) on weekdays.

---

## 📋 Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.x**: The script is written in Python.
2. **Telegram Bot**: Create a Telegram bot and obtain the bot token and chat ID.
3. **ChromeDriver**: Download and install ChromeDriver that matches your Chrome browser version.
4. **Environment Variables**: Set up the required environment variables in a `.env` file.

---

## ⚙️ Set Up

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/matthewtognotti/stock-checker-bot
    cd stock-checker-bot
    ```
2. ** Create your Virtual Environemnt (Optional)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add the following variables:
    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```
5. **Run the Script**:
    ```bash
    python3 main.py
    ```

---

## 🧩 Code Structure

- **🛒 StockChecker Class**: Handles the login, product data scraping, and stock checking.
- **🤖 TelegramBot Class**: Manages sending messages via Telegram.
- **🔄 main Function**: Orchestrates the stock checking and notification process.

---

## 🎨 Customization

- **Excluded Products**: Add product titles to the `EXCLUDED_PRODUCTS` list in `constants.py` to exclude them from stock checks.
- **Business Hours**: Modify the `japan_business_hours` function to adjust the operating hours.

---

## 🛠 Troubleshooting

- **ChromeDriver Issues**: Ensure that the ChromeDriver version matches your Chrome browser version.
- **Login Failures**: Verify that the login credentials and page elements (e.g., email input, password input) are correctly specified.
- **Telegram Notifications**: Ensure that the Telegram bot token and chat ID are correctly set in the `.env` file.

---

## 🚀 Further Improvements

Now
--
1. Fix issue with telegram bot instantiation in while loop. errors if it is outside. 
2. Remove Japan Hours?
3. Issue where recaptcha is not required, the bot fails
4. Put code through windsurf to make it production grade. Add try and except blocks for errors. Good comments. Readme.
5. Add Error Handling: Implement robust error handling for login failures, network issues, and Telegram API errors.
6. Create improved list of improvements below (should these be issues in github?)
7. Create new repo



Future
--
8. **Add Logging**: Implement a logging system to track bot activity, errors, and stock updates.
9. Detect if the bot gets logged out and sign back in
10. Also read time out error from URLlib
11. **Format message to send product link**: Organize the message in a table for better readability. or use Telegram's inline buttons. 
12. Add hash map or other ds (use array of tuples) to store product variants in product and display to the user. this may need to be done with multiprocessing so that we don't get stuck loading on a single page. Additionally, research more about the selenium API (Selenium vs Selenium Base?). There may be a built in way to do multiprocessing and I need to fully understand the API to make this bot quick and reliable. Or use multiple tabs in seleniunm. Also experiement with going headless. 
13. **Allow user to request updates**: Enable users to send `/update` and receive a table with all in-stock products or a "no products in stock" message.
14. **Mutliprocessing**: One process for stock updates, another for adding to cart and buying (BuyProduct class).
15. **Add Multi-User Support**: Allow multiple Telegram users to receive notifications by managing a list of chat IDs.
16. Run on AWS Lambda or Google Cloud Functions.

---

**📝 Note**: This script is intended for educational purposes. Ensure you comply with the terms of service of the website you are automating.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.