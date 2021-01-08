# Sahib
## Overview:
Twitter bot that scrapes Wal-mart's clearance page using **Python** to find best deals and post them on twitter automatically. The bot scrapes data using the **Selenium framework** for Python, and the data is then stored in a **MongoDB** cluster to be tweeted later. Using Windows Task Manager, a **CRON job** was created to tweet 5 deals daily.

## Data Flow:

### Scraping from Walmart:
**1.** Using **Selenium**, a **Webdriver for Firefox** is created that opens  
<br />
**2.** Using the **TradingView webhook API**, a POST request containing the **JSON** message is sent to a REST API (**AWS Lambda** function) 
<br />
**3.** This executes a **Python** script running through the **AWS Chalice Serverless Framework** 
<br />
**4.** The **Python** script then executes a bracket order using the **Alpaca API Paper Trading API** (tested requests live and offline using **Insomnia REST API Client**)

### Scraping from Twitter:


## Demo:
* To view the bot in action:https://twitter.com/SahibBot_
![Demo](https://user-images.githubusercontent.com/66835262/104045431-8c008080-51ac-11eb-9d31-7537516b84c5.png)


## Libraries and Frameworks Used: 
* **Selenium framework for Python:** https://selenium-python.readthedocs.io/
* **Geckodriver:** https://github.com/mozilla/geckodriver/releases
* **MongoDB for Python:** https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
* **DNSPython:** https://pypi.org/project/dnspython/
