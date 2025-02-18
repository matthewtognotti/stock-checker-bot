# Project Notes

## Table of Contents
- [Project Notes](#project-notes)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Libraries](#libraries)


## Project Description
A python bot to notify the user when an out of stock item is back in stock. 

The bot will scrape the website for the item and notify the user via text when the item is back in stock.

## Libraries

The bot will use Beautiful Soup for web scraping and Twilio for sending text messages.

pip install bs4

https://www.crummy.com/software/BeautifulSoup/bs4/doc/


Might actually need to use selenium, becuase the site I am targeting requires the user to be logged in to view product data. 



TODO:
- Use .env for secrets or something else.
- Format message to send product link and organized in a table.
- Clean up code and create new repo possibly? to showcase the project. Good comments and documentation. 

