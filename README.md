# Sahib
### Overview:
**Python** bot that scrapes Walmart's clearance page for electronics to find the best deals and post them on Twitter automatically. The bot scrapes data using the **Selenium framework** for Python, and the data is then stored in a **MongoDB** collection to be tweeted later. Using Windows Task Scheduler, the script was made into a **CRON job** to tweet 5 deals daily.

### Data Flow:

#### Scraping from Walmart:
**1.** Using **Geckodriver**, a **Webdriver for Firefox** is created that opens Walmart's clearance page for electronics
<br />
**2.** The products are then scrapped using **Selenium**, and data such as the product's title, new and old price, and when it was scrapped is recorded
<br />
**3.** Calculations are done to determine the discount percentage and price, and then using **DNSPython** products are sent to be stored in a **MongoDB** collection

#### Scraping from Twitter:
**1.** Using **Geckodriver**, a **Webdriver for Firefox** is created that opens Twitter's log-in page
<br />
**2.** The script then checks if **cookies** saved as **JSON** objects for an older log-in exist, and if not logs in normally
<br />
**3.** Afterwards a connection with **MongoDB** is established, and the script finds the first 5 postings that haven't been tweeted
<br />
**4.** Using **Selenium** tweets are sent out over a 3 minute period, each with one of 8 template messages to publish new deals, and the posting date is saved in the database to not allow duplicate postings to occur
<br />
**5.** This script was turned into a **CRON job** using Windows Task Scheduler, and it runs automatically once a day to tweet out 5 deals daily

## Demo:
* To view the bot in action, click [here](https://twitter.com/SahibBot_): 
![Demo](https://user-images.githubusercontent.com/66835262/104045431-8c008080-51ac-11eb-9d31-7537516b84c5.png)


## Libraries and Frameworks Used: 
* **Selenium framework for Python:** https://selenium-python.readthedocs.io/
* **Geckodriver:** https://github.com/mozilla/geckodriver/releases
* **MongoDB for Python:** https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
* **DNSPython:** https://pypi.org/project/dnspython/
