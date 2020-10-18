# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import keys
import csv
import time
import json

class Book:
    def __init__(self, title, url):
        self.title = title
        self.url = url
    def __iter__(self):
        return iter([self.title, self.url])

url = 'https://www.goodreads.com/'

def create_csv_file():
    header = ['Title', 'URL']
    with open('/GoodReadsBooks.csv', 'w') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(header)

def read_from_txt_file():
    lines = [line.rstrip('\n') for line in open('/Book_List.txt')]
    return lines

def init_selenium():
    options = Options()
    options.add_argument('--headless')
    global driver
    driver = webdriver.Chrome("/chromedriver")
    driver.get(url)
    time.sleep(20)
    driver.get('https://www.goodreads.com/search?q=')

def search_for_title(title):
    search_field = driver.find_element_by_xpath('//*[@id="search_query_main"]')
    search_field.clear()
    search_field.send_keys(title)
    search_button = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/form/div[1]/input[3]')
    search_button.click()

def scrape_url():
    try:
        url = driver.find_element_by_css_selector('a.bookTitle').get_attribute('href')
    except:
        url = "N/A"

    return url

def write_into_csv_file(vendor):
    with open('/Users/rodrigopeniche/Documents/workspace/WebScraping/GoodReadsBooks.csv', 'a') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(list(vendor))

create_csv_file()
titles = read_from_txt_file()    
init_selenium()

for title in titles:
    search_for_title(title)
    url = scrape_url()
    book = Book(title, url)
    write_into_csv_file(book)
    

