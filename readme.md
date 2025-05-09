# Stock Checker Bot with Telegram Notifications

This Python script helps you track product stock from a website that requires login and reCAPTCHA. When a product comes back in stock, it’ll ping you on Telegram with the product link and available variants with different sizes and prices.

The bot handles logouts, errors, and interruptions automatically - so once it's running, you can mostly forget about it.

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
  - [License](#license)

---

## Features

- **Auto Login & reCAPTCHA Bypass** – Uses Selenium to log into the site and handle reCAPTCHA challenges.
- **Stock Monitoring** – Checks product availability every minute. If the site logs you out, the bot logs back in automatically.
- **Telegram Alerts** – Instantly sends you a Telegram message when products are in stock, including a direct link and variant info.

---

## Prerequisites

Before you get started, make sure you’ve got:

1. **Python 3.11 or higher**
2. **Telegram Bot** – Create one and grab the bot token and your chat ID.
3. **ChromeDriver** – Download the version that matches your installed version of Chrome.

---

## Set Up

1. **Clone the repo**:
    ```bash
    git clone https://github.com/matthewtognotti/stock-checker-bot
    cd stock-checker-bot
    ```

2. **Set up a virtual environment (recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file**:
    - Copy from `example.env` and fill in your Telegram token, chat ID, and other config details.

5. **Run the script**:
    ```bash
    venv/bin/python main.py
    ```

---

## Code Structure

- **StockChecker class** – Handles login and scraping product data.
- **TelegramBot class** – Sends messages to your Telegram account.
- **main.py** – Coordinates everything: login, checking, and notifying.

---

## Customization

- **Skip Certain Products** – Just add product titles to the `EXCLUDED_PRODUCTS` list in constants.py if you don’t want alerts for them.

---

## Troubleshooting

- **ChromeDriver errors?** – Make sure the version matches your installed Chrome.
- **Login not working?** – Double-check your credentials and the site’s input field IDs or product class names.
- **No Telegram messages?** – Verify your bot token and chat ID are correct in `.env`.

---

Note: This bot is intended for educational purposes. Make sure you're following the rules of the website you're interacting with.

---

## License

MIT License. See the [LICENSE](LICENSE) file for the full terms.
