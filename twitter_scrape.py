
import requests
import lxml
import pandas as pd
import time
from dotenv import load_dotenv
import os
import re
from datetime import datetime

from bs4 import BeautifulSoup
from bs4.element import Tag

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select




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

print('clicking advanced search box')
advanced_search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1dbjc4n[data-testid="searchFiltersAdvancedSearch"]')))
advanced_search_box.click()

time.sleep(10)


print('clicking language box')
language_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SELECTOR_1"]')))
language_box.click()
print('Choosing English')
select = Select(language_box)
select.select_by_index(11)

print('Clicking hashtags box')
hashtags_box = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@name="theseHashtags"]')))
hashtags_box[0].click()  # presence_of_all_elements_located returns a list, so you need to access the first element
hashtags_box[0].send_keys('#BostonStrong')

# print("Moving on to Dates")
# #########THIS WORKS
# print('dates from month')
# dates_from_month = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SELECTOR_2"]')))
# dates_from_month.click()
# select_from_month = Select(dates_from_month)
# select_from_month.select_by_index(3)   #select March?



print('dates from day')
dates_from_day = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SELECTOR_10"]')))
print('1')
dates_from_day.click()
print('2')
select_from_day = Select(dates_from_day)
print('3')
select_from_day.select_by_index(1)  #select 1st of the month
print('4')

########### doesn't work
# print('dates from year')
# dates_from_year = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#SELECTOR_11')))
# dates_from_year.click()
# select_from_year = Select(dates_from_year)
# try:
#     print('trying by index')
#     select_from_year.select_by_index(1)  #select 2023
# except Exception:
#     print('trying by value')
#     select_from_year.select_by_value('2023')







# #######STEP . GATHER HTML
# print('extracting info from tweets')
# html = driver.page_source

# soup = BeautifulSoup(html, 'lxml')

# all_tweets = soup.find_all('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu')

# #this holds all info gathered from each tweet on the page
# final_results = []

# for tweet in all_tweets:
    
#     twitter_handle = ''
#     username = ''
#     date_of_tweet = []
#     content = ''
#     image_links = []
#     video_links = []
    
#     # gets username, twitter handle, date of tweet
#     first_nested_div = tweet.find('div', class_='css-1dbjc4n r-k4xj1c r-18u37iz r-1wtj0ep')
#     if first_nested_div:
#         # if these div tags are found
#         for div in first_nested_div:
            
#             #extract text content of the div
#             div_text = div.get_text()
            
#             #find and extract twitter handle
#             for match in re.finditer(r'@(\w+)', div_text):
#                 twitter_handle += match.group(0)
                
#             # Find and extract user's name
#             for match in re.finditer(r'(?<!@)\b(?![A-Za-z]{3} \d{1,2}\b)\w+(?: \w+)+\b', div_text):
#                 username += match.group(0)
                
#             # Find and extract date of tweet
#             pattern = r'(?:[A-Z][a-z]{2} \d{1,2}|\d{1,2}h)'
#             for match in re.finditer(pattern, div_text):
#                 date_of_tweet = match.group(0)
                
#             for i, result in enumerate(date_of_tweet):
#                 if re.match(pattern, result):
#                     # Get the current date in the desired format "Nov 3"
#                     current_date = datetime.now().strftime("%b %d")
#                     current_date = current_date.replace(" 0", " ")  # Remove leading zero from the day
#                     date_of_tweet[i] = current_date     

#     else:
#         # if these div tags are not found
#         twitter_handle = 'No twitter handle'
#         username = 'No Name'
#         date_of_tweet = 'No Date'
    
    
#     # gets content of tweet including hashtags
#     second_nested_div = tweet.find('div', class_='css-901oao css-cens5h r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
#     if second_nested_div:
#         # if these div tags are found
#         tweet_contents = []
        
#         for div in second_nested_div:
#             for item in div:
#                 # if contains span
#                 if item.name == 'span':
#                     tweet_contents.append(item.get_text())
#                 # if contains a
#                 elif item.name == 'a':
#                     tweet_contents.append(item.get_text())
#                 # if no other tag
#                 else:
#                     tweet_contents.append(item)
                
#         #flatten tweet_contents into one long string
#         tweet_contents = ''.join(tweet_contents)
#         content = tweet_contents
        
        
#     else:
#         # if these div tags are not found
#         tweet_contents = 'No Tweet Contents'
#         content = tweet_contents
        
        
#     # gets content of other media. Can be 3 different things: an image, a retweet, a video
#     # check for images first
#     nested_imgs = tweet.find_all('img', class_="css-9pa8cd")
#     if nested_imgs:
#         for i in nested_imgs:
#             # need to remove everything to the right of the "?" character
#             src = i.get('src')
#             src = src.split('?')[0]
#             # check if last 4 characters of the string are .jpg aready
#             if src[-4:] == '.jpg':
#                 image_links.append(src)
#             else:
#                 src = src + '.jpg'    # add .jpg to end to complete string
#                 image_links.append(src)
#     else:
#         image_links.append('No Images')
    
    
        
#     # videos    
#     nested_media = tweet.find_all('video')
#     if nested_media:
#         for i in nested_media:
#             poster_img = i.get('poster')
#             video_links.append(poster_img)
#     else:
#         video_links.append('No Video')
        
    
#     # handle missing or empty data such as username, date of tweet, or content
#     if len(username) == 0:
#         username = 'No Name'
        
#     if len(date_of_tweet) == 0:
#         date_of_tweet = 'No Date'
    
#     final_results.append([twitter_handle, username, date_of_tweet, content, image_links, video_links])

#     print()
#     print('~~~~~~~~~~~~~~~~~')
#     print()







    
    










# exit web driver
# driver.quit()



