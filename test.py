
import requests
import lxml
from bs4 import BeautifulSoup
import pandas as pd
import time
from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re


#set up chromedriver
MY_PATH = "./chromedriver"
driver = webdriver.Chrome(executable_path=MY_PATH)
wait = WebDriverWait(driver, 60)    # determines maximum wait time for an element to load


print('going to clipping chains')
driver.get('https://clippingchains.com/')

print('clicking on getting started')
#click on 'getting started'
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-item-7360"]'))).click()

print('waiting')
time.sleep(10)

print('gathering html')
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')


print('extracting links')
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    print(href)
