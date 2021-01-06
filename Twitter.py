from config import *
from db import *
from utilities import *

from time import sleep
import json
from pathlib import Path
import random
from datetime import datetime

import pymongo 

client = pymongo.MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_url}")
db = client.walmart

try:
    current_path = os.path.dirname(os.path.abspath(__file__))
except:
    current_path = '.'

driver = init_driver(gecko_driver, user_agent = user_agent, is_headless = False)

is_login = load_cookies(driver)

if is_login == False:
    twitter_login(driver)

driver.get(twitter_url)

if len(driver.find_elements_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div')) > 0:
    products = list(db.products.find({'published_at': False}).limit(5))
    
    for product in products:
        _ = publish_product(driver, product)
        sleep(30)

driver.close()
