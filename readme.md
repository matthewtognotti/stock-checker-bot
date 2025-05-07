# 🛒 Stock Checker Bot with Telegram Notifications

This script automates the process of checking product stock on a website that requires login and reCAPTCHA to check if a product is in stock. Once a product is in stock, the bot sends a Telegram message to the user with a link and all product variants that are in stock.

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
  - [Today](#today)
  - [Future](#future)
  - [📜 License](#-license)

---

## ✨ Features

- **Login Automation and reCATPCHA Bypass**: Logs into the website using Selenium to access stock data and bypasses the reCAPTCHA.
- **Stock Monitoring**: Scrapes product data and checks stock status every minute. Automatically logs back when bot detects it has been logged out by the site. 
- **Telegram Notifications**: Sends a message to the user via Telegram when products are in stock.

---

## 📋 Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.11 or above**: The script is written in Python.
2. **Telegram Bot**: Create a Telegram bot and obtain the bot token and chat ID.
3. **ChromeDriver**: Download and install ChromeDriver that matches your Chrome browser version.

---

## ⚙️ Set Up

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/matthewtognotti/stock-checker-bot
    cd stock-checker-bot
    ```
2. ** Create your Virtual Environemnt (Recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Up Environment Variables**
    Create a `.env` file in the root directory follwing `example .env` provided.

5. **Run the Script**:
    ```bash
    python3 main.py
    ```

---

## 🧩 Code Structure

- **🛒 StockChecker Class**: Handles the login and product data scraping.
- **🤖 TelegramBot Class**: Manages sending messages via the Telegram API.
- **🔄 main Function**: Orchestrates the stock checking and notification process.

---

## 🎨 Customization

- **Excluded Products**: Add product titles to an `EXCLUDED_PRODUCTS` list to exclude them from stock checks.
  
---

## 🛠 Troubleshooting

- **ChromeDriver Issues**: Ensure that the ChromeDriver version matches your Chrome browser version.
- **Login Failures**: Verify that the login credentials and page elements (e.g., email input, password input) are correctly specified.
- **Telegram Notifications**: Ensure that the Telegram bot token and chat ID are correctly set in the `.env` file.

---

## 🚀 Further Improvements

Robust error handling, auto-recovery, logging, and deployment strategies. Bot is resilient and self-healing.

Today
--
1. Figure out how to use try-except and read the stack trace
2. Add Error Handling: Implement robust error handling for login failures, network issues, and Telegram API errors, Also read time out error from URLlib. Make bot self-healing.

3. Commit first, then put code through windsurf.

4. Merge with Main Branch

5. Proof read all code, comments, and files in repo
6. Finalize the readme, create new repo, move issues to the repo, and publish the code



Future
--
- Remove duplicate messages (how does that affect exlcuded products?)
- Auto buy when in stock -  Only once a day? 
- Unit tests w/ site HTML for purchasing products
- Docker File -> AWS
- Raspberry Pi w/ react front end display. 
  
1.  **Format message to send product link**: Organize the message in a table for better readability. or use Telegram's inline buttons. 
2.  Add hash map or other ds (use array of tuples) to store product variants in product and display to the user. this may need to be done with multiprocessing so that we don't get stuck loading on a single page. Additionally, research more about the selenium API (Selenium vs Selenium Base?). There may be a built in way to do multiprocessing and I need to fully understand the API to make this bot quick and reliable. Or use multiple tabs in seleniunm. Also experiement with going headless. 
3.  **Add Multi-User Support**: Allow multiple Telegram users to receive notifications by managing a list of chat IDs.
4.  Run on AWS Lambda or Google Cloud Functions.

---

**📝 Note**: This script is intended for educational purposes. Ensure you comply with the terms of service of the website you are automating.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.