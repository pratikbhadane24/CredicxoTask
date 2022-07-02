from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import json
import csv
import time
import logging
logging.getLogger('WDM').setLevel(logging.NOTSET)
start = time.time()


def get_price():
    try:
        price = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "corePrice_feature_div"))).text
    except:
        try:
            price = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "price"))).text
        except:
            price = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "usedBuySection"))).text
    return price


def get_details(id1, id2):
    try:
        detail = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, id1))).text
    except:
        detail = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, id2))).text
    return detail


def get_product_details(url):
    try:
        title = get_details("productTitle", "title").text
        price = get_price()
        image_link = get_details(
            "landingImage", "imgBlkFront").get_attribute("src")
        product_details = get_details(
            "productDescription", "detailBulletsWrapper_feature_div").text

        return title, price, image_link, product_details
    except:
        print(f"{url} not available")


with open("Amazon Scraping.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    links = [line[2:] for line in csv_reader]


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

all_products = []

for i in range(len(links)):
    country = links[i][1]
    asin = links[i][0]
    url = f"https://www.amazon.{country}/dp/{asin}"
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(url)
    try:
        product = get_product_details(url)
        if len(product) > 0:
            product_dict = {"Product Title": product[0], "Price": product[1],
                            "Image_link": product[2], "Description": product[3]}

            all_products.append(product_dict)
    except:
        pass
    driver.quit()

with open('scrapes.json', 'a') as outfile:
    outfile.write(json.dumps(all_products, indent=2))

# Database Dump Start
load_dotenv(find_dotenv())
password = os.environ.get('MONGO_PWD')
connection_str = f"mongodb+srv://pratiksample24:{password}@cluster0.o0yxliv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_str)
test_db = client.credixcoTask
collection = test_db.scrapes
collection.insert_many(all_products)
# Database Dump Done


end = time.time()

print(f"Runtime of the program is {end - start}")
