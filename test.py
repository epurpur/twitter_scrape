


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


#set up chromedriver
MY_PATH = "./chromedriver"
driver = webdriver.Chrome(executable_path=MY_PATH)
wait = WebDriverWait(driver, 60)    # determines maximum wait time for an element to load




driver.get('https://clippingchains.com/')

print('sleeping')
time.sleep(5)

page_height = driver.execute_script('return document.body.scrollHeight')
print(f'page_height = {page_height}')

print('Scrolling')

scroll_distance = 598 # this is measured in pixels
driver.execute_script(f'window.scrollBy(0, {scroll_distance});')

time.sleep(5)

print('Scrolling')

scroll_distance = 598 # this is measured in pixels
driver.execute_script(f'window.scrollBy(0, {scroll_distance});')

driver.quit()