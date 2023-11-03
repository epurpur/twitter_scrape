
import requests
import lxml
from bs4 import BeautifulSoup
import pandas as pd
import time
from dotenv import load_dotenv
import os
import re
from datetime import datetime

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


#####STEP 1. LOGIN

driver.get('https://twitter.com/i/flow/login')

print('webpage accessed')
time.sleep(15)


#read .env file environment variables
load_dotenv()
email = os.getenv("email")
password = os.getenv("password")
phoneNumber = os.getenv("phoneNumber")

print('writing email')
login = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
# time.sleep(2)
login.click()
login.send_keys(email)

#click next button
print('finding next')
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()
# next_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[2]/div[2]/div/div[7]/div')
time.sleep(10)

#Might get either just the password box or another box that says 'there has been unusual activity'
try:
    phone_number_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='text'][@type='text']")))
    print('unusual activity box. entering phone number')
    phone_number_box.click()
    phone_number_box.send_keys(phoneNumber)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))).click()


except Exception:
    # if this box doesn't appear
    pass

print('writing password')
password_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password'][@type='password']")))
password_box.click()
password_box.send_keys(password)

#click login button
print('clicking login button')
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))
login_button.click()

print('Login Successful!')
print()
print()


######STEP 2. SEARCH

time.sleep(5)
print('clicking search bar')
search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
search_box.click()
print('sending keys #BostonStrong')
search_box.send_keys('#BostonStrong')
#click enter button
print('press enter key')
search_box.send_keys(Keys.RETURN)


print('Waiting for page to render')
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-901oao')))

print('Extra wait time')
time.sleep(15)
######################################################
print('gathering html')
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

print('extracting tweets')

final_results = []

# gather twitter handles
div_tags = soup.find_all('div', class_='css-1dbjc4n r-k4xj1c r-18u37iz r-1wtj0ep')

for div in div_tags:
    usernames = []
    twitter_handles = []
    date_of_tweet = []
    
    # Extract the text content of the div
    div_text = div.get_text()
    
    # Find and extract Twitter usernames
    for match in re.finditer(r'@(\w+)', div_text):
        twitter_handles.append(match.group(0))
        
    # Find and extract Twitter usernames
    for match in re.finditer(r'(?<!@)\b(?![A-Za-z]{3} \d{1,2}\b)\w+(?: \w+)+\b', div_text):
        usernames.append(match.group(0))
        
    # Find and extract date of tweet
    pattern = r'(?:[A-Z][a-z]{2} \d{1,2}|\d{1,2}h)'
    for match in re.finditer(pattern, div_text):
        date_of_tweet = match.group(0)
        
    for i, result in enumerate(date_of_tweet):
        if re.match(pattern, result):
            # Get the current date in the desired format "Nov 3"
            current_date = datetime.now().strftime("%b %d")
            current_date = current_date.replace(" 0", " ")  # Remove leading zero from the day
            date_of_tweet[i] = current_date
            print(date_of_tweet)
            
    final_results.append([usernames, twitter_handles, date_of_tweet])
    


# get all HTML from current page

#########STOP HERE Temporarily
######################################################


# #click 'advanced search'
# print('click advanced search')
# advanced_search = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Advanced search']")))
# advanced_search.click()

# #click 'these hashtags'
# print('add #BostonStrong hashtag')
# these_hashtags = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='theseHashtags']")))
# these_hashtags.click()
# these_hashtags.send_keys('#BostonStrong')

# #scroll down popup box
# print('scrolling halfway down popup box')
# popup_window_handle = driver.window_handles[-1]
# print('popup window handle', popup_window_handle)
# driver.switch_to.window(popup_window_handle)
# popup_window_handle.scrollTo(0, 500)



#######################THOUGHTS- FIND SOME OTHER MORE EASILY ACCESSIBLE POPUP WINDOW TO SCROLL TO IN TEST CODE.
####################### THIS METHOD IS SLOW AND TIME CONSUMING


# #click 'english language from dropdown box'
# print('choosing English language')
# language_box = wait.until(EC.element_to_be_clickable((By.ID, 'SELECTOR_1')))
# language_box.click()
# try:
#     print('pass 1')
#     language_box.select_by_visible_text("English")
# except Exception:
#     print('Error!')
#     print('pass 2')
#     language_box.selectByIndex(12)
    
    











# #click 'latest' button



# ######Step 3. Gather HTML

# gathering HTML
print('Gathering HTML')
soup = BeautifulSoup(driver.page_source, 'lxml')

# mess1 = []

# for item in soup.find_all('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'):
#     mess1.append(item.text)
    
    
# # scroll down page
# print()
# print('Scrolling Page to bottom')
# print()
    

# full_page_height = driver.execute_script('return document.body.scrollHeight')
# print(f'Page height: {full_page_height}')
# #height of window is 598 pixels. need to divide full page height by 598
# scroll_distance = 598
# numberOfScrolls = int(full_page_height / scroll_distance)
# print(f"Number of Scrolls: {numberOfScrolls}")


# for i in range(numberOfScrolls):
#     driver.execute_script(f'window.scrollBy(0, {scroll_distance});')
#     time.sleep(2)
    
# time.sleep(10)

   

# print('Gathering HTML of full page')
# soup = BeautifulSoup(driver.page_source, 'lxml')

# full_mess = []

# for item in soup.find_all('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'):
#     full_mess.append(item.text)


driver.quit()



