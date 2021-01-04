from config import *
from db import *
import json
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import pymongo
import os

from datetime import datetime 
from time import sleep

client = pymongo.MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_url}")
db = client.walmart

try:
    current_path = os.path.dirname(os.path.abspath(__file__))
except:
    current_path = '.'

def init_driver(gecko_driver, load_images = True, user_agent = '', is_headless = False):
    firefox_profile = webdriver.FirefoxProfile()
    
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    firefox_profile.set_preference('media.volume_scale', "0.0")
    firefox_profile.set_preference("dom.webnotifications.enabled", False)
    
    if not load_images:
        firefox_profile.set_preference('permissions.default.image', 2)
    if user_agent != '':
        firefox_profile.set_preference("general.useragent.override", user_agent)
    
    options = Options()
    options.headless = is_headless
    
    driver = webdriver.Firefox(executable_path = f"{current_path}/{gecko_driver}",
                              firefox_profile = firefox_profile,
                              options = options)
    
    return driver

def get_url(page_url, driver):
    driver.get(page_url)
    
    sleep(page_load)
    close_popup = driver.find_elements_by_css_selector('.acsFocusFirst')
    if len(close_popup) > 0:
        close_popup[0].click()

def get_products(driver):
    products = driver.find_elements_by_css_selector('div.shelf-thumbs .standard-thumb')

    products_info = []

    for product in products:
        # Get product title
        product_title = ''
        if len(product.find_elements_by_css_selector('div.product-details-container .details .title .thumb-header')) > 0:
            product_title = product.find_elements_by_css_selector('div.product-details-container .details .title .thumb-header')[0].text

        # Get product url
        product_url = ''
        if len(product.find_elements_by_css_selector('a.product-link')) > 0:
            product_url = product.find_elements_by_css_selector('a.product-link')[0].get_attribute('href')

        # Get product current price
        current_price = 0
        if len(product.find_elements_by_css_selector('div.product-details-container .all-price-sections .price-current')) > 0:
            current_price = product.find_elements_by_css_selector('div.product-details-container .all-price-sections .price-current')[0].text
            current_price = current_price.replace('\n', '')
            current_price = current_price.replace('$', '')
            current_price = current_price.replace(',', '')
            if "to" in current_price:
                current_price = current_price.split('.')
                current_price = float(current_price[0])
            current_price = float(current_price)

        # Get product old price
        old_price = 0
        if len(product.find_elements_by_css_selector('div.product-details-container .all-price-sections .pricing-spacer .price-was')) > 0:
            old_price = product.find_elements_by_css_selector('div.product-details-container .all-price-sections .pricing-spacer .price-was')[0].text
            old_price = old_price.replace('$', '')
            old_price = old_price.replace("Was ", "")
            if len(old_price) > 0:
                old_price = float(old_price)
            else: 
                old_price = 0

        discount_number = 0
        discount_percent = 0

        if current_price != 0 and old_price != 0 and old_price > current_price:
            discount_number = round(old_price - current_price)
            discount_percent = round(100 - (current_price/old_price) * 100)

        if current_price !=0 and len(product_url) > 0 and len(product_title) > 0:
            product_info = {
                'product_title': product_title,
                'product_url': product_url,
                'current_price': current_price,
                'old_price': old_price,
                'discount_number': discount_number,
                'discount_percent': discount_percent,
                'inserted_at': datetime.now(),
                'updated_at': datetime.now(),
                'published_at': False
            }
            
            if db.products.count_documents({'$or': [ {'product_title': product_title}, {'product_url': product_url}]}) == 0:
                _ = db.products.insert_one(product_info)
            else:
                pd = db.products.find_one({'$or': [ {'product_title': product_title}, {'product_url': product_url}]})
                if pd['current_price'] != current_price or pd['old_price'] != old_price:
                    db.products.update_one({'_id':  pd['_id']}, {'$set': {
                                                                'current_price': current_price,
                                                                'old_price': old_price,
                                                                'discount_number': discount_number,
                                                                'discount_percent': discount_percent,
                                                                'updated_at': datetime.now()
                                                            }} )
                    
            products_info.append(product_info)
        
    return products_info

def load_cookies(driver):
    driver.get(twitter_url)
    cookies = ''
    
    cookie_file = f"{current_path}/{twitter_cookies_path}"
    if Path(cookie_file).is_file():
        with open(cookie_file, 'r', encoding = 'utf8') as ck_file:
            cookies = ck_file.read()
    
    if cookies != '':
        cookies = json.loads(cookies)
        
        if len(cookies) > 0:
            for cookie in cookies:
                driver.add_cookie(cookie)
                
        sleep(5)
    
        driver.get(f"{twitter_url}/settings/account")
        if len(driver.find_elements_by_name("session[username_or_email]")) >  0:
            _ = open(cookie_file, 'w').truncate()
            return False
        else: 
            return True
    
    return False

def twitter_login(driver):    
    driver.get(twitter_login_page)
    
    if driver.find_elements_by_name("session[username_or_email]") and driver.find_elements_by_name("session[password]"):
        email = driver.find_element_by_name("session[username_or_email]")
        email.clear()
        password = driver.find_element_by_name("session[password]")
        password.clear()

        email.send_keys(twitter_email)
        password.send_keys(twitter_password)

        sleep(3)
        password.submit()

        sleep(5)
        cookies_list = driver.get_cookies()

        ck_file = open(f"{current_path}/{twitter_cookies_path}", 'w', encoding = 'utf8')
        ck_file.write(json.dumps(cookies_list))
        ck_file.close()
        
    return True
