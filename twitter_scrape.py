
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
from selenium.common.exceptions import TimeoutException


MY_PATH = "./chromedriver"
driver = webdriver.Chrome(executable_path=MY_PATH)
wait = WebDriverWait(driver, 60)    # determines maximum wait time for an element to load


#####STEP 1. LOGIN
driver.get('https://twitter.com/i/flow/login')

print('webpage accessed')
time.sleep(30)


#read .env file environment variables
load_dotenv()
email = os.getenv("email")
password = os.getenv("password")
phoneNumber = os.getenv("phoneNumber")

print(email, password, phoneNumber)

print('writing email')

login = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')# login = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
time.sleep(2)
login.click()
login.send_keys(email)

#click next button
print('finding next')
wait = WebDriverWait(driver, 10)  # You can adjust the timeout duration if needed
next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')))
next_button.click()
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

# click on "x" for security box if needed
try:
    print("clicking security X")
    wait = WebDriverWait(driver, 10)
    x_button = wait.until(EC.element_to_be_clickable(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/button/div/svg'))
    x_button.click()
except Exception:
    pass


time.sleep(100)
print('clicking search bar')
search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
search_box.click()
print('Sending search terms keys')

##CHANGE THE DATES AND YEAR HERE
search_box.send_keys('(#BostonStrong) lang:en until:2022-03-01 since:2022-01-01')
print('press enter key')
search_box.send_keys(Keys.RETURN)

print('click latest button')
latest_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Latest"]')))
# Scroll into view
print('scrolling into view')
driver.execute_script("arguments[0].scrollIntoView(true);", latest_button)
# Click on the element
latest_button.click()

#scrolling down page
print('scrolling to bottom of page. This might take a while...')



scrolls = 5000  # an attempt to get all tweets from this year between March 1 and June 1

#this holds all info gathered from each tweet on the page
final_results = []

for scroll in range(scrolls):
    print()
    print(f'Scroll number {scroll + 1}')
    current_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    print("Current height of page: ", current_height)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    
    #######STEP 3. GATHER HTML
    print('extracting info from tweets')
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')

    all_tweets = soup.find_all('div', class_='css-175oi2r r-16y2uox r-1wbh5a2 r-1ny4l3l')

    # #this holds all info gathered from each tweet on the page
    # final_results = []

    for tweet in all_tweets:
        
        twitter_handle = ''
        username = ''
        date_of_tweet = []
        content = ''
        image_links = []
        video_links = []
        
        # gets username, twitter handle, date of tweet
        first_nested_div = tweet.find('div', class_='css-175oi2r r-k4xj1c r-18u37iz r-1wtj0ep')
        if first_nested_div:
            # if these div tags are found
            for div in first_nested_div:
                
                #extract text content of the div
                div_text = div.get_text()
                
                #find and extract twitter handle
                for match in re.finditer(r'@(\w+)', div_text):
                    twitter_handle += match.group(0)
                    
                # Find and extract user's name
                for match in re.finditer(r'(?<!@)\b(?![A-Za-z]{3} \d{1,2}\b)\w+(?: \w+)+\b', div_text):
                    username += match.group(0)
                    
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

        else:
            # if these div tags are not found
            twitter_handle = 'No twitter handle'
            username = 'No Name'
            date_of_tweet = 'No Date'
        
        
        # gets content of tweet including hashtags
        second_nested_div = tweet.find('div', class_='css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim')
        # second_nested_div = tweet.find('div', class_='css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim')
        if second_nested_div:
            # if these div tags are found
            tweet_contents = []
            
            for div in second_nested_div:
                for item in div:
                    # if contains span
                    if item.name == 'span':
                        tweet_contents.append(item.get_text())
                    # if contains a
                    elif item.name == 'a':
                        tweet_contents.append(item.get_text())
                    # if no other tag
                    else:
                        tweet_contents.append(item)
                    
            #flatten tweet_contents into one long string
            tweet_contents = ''.join(tweet_contents)
            content = tweet_contents
            
            
        else:
            # if these div tags are not found
            tweet_contents = 'No Tweet Contents'
            content = tweet_contents
            
            
        # gets content of other media. Can be 3 different things: an image, a retweet, a video
        # check for images first
        nested_imgs = tweet.find_all('img', class_="css-9pa8cd")
        if nested_imgs:
            for i in nested_imgs:
                # need to remove everything to the right of the "?" character
                src = i.get('src')
                src = src.split('?')[0]
                # check if last 4 characters of the string are .jpg aready
                if src[-4:] == '.jpg':
                    image_links.append(src)
                elif src[-5:] == '.jpeg':
                    image_links.append(src)
                else:
                    src = src + '.jpg'    # add .jpg to end to complete string
                    image_links.append(src)
        else:
            image_links.append('No Images')
        
        
            
        # videos    
        nested_media = tweet.find_all('video')
        if nested_media:
            for i in nested_media:
                poster_img = i.get('poster')
                video_links.append(poster_img)
        else:
            video_links.append('No Video')
            
        
        # handle missing or empty data such as username, date of tweet, or content
        if len(username) == 0:
            username = 'No Name'
            
        if len(date_of_tweet) == 0:
            date_of_tweet = 'No Date'
            
        print(f'Total number of tweets gathered: {len(final_results)}')
        
        print(content)
        
        final_results.append([twitter_handle, username, date_of_tweet, content, image_links, video_links])

    
    
    # Check if the "Reply" button is present
    retry_button = driver.find_elements_by_xpath("//span[contains(text(), 'Retry')]")
    
    if retry_button:
        print("Found 'Reply' button, clicking...")
        retry_button[0].click()
    


print('waiting for page to load')
time.sleep(30)





#######STEP 4. Assemble Results into Dataframe
print(f'Collected data from {len(final_results)} tweets')
print('Creating final DataFrame with results')
# Define column names
columns = ['TwitterHandle', 'Name', 'Date', 'TweetContent', 'ImageUrls', 'VideoUrls']

# Create a DataFrame
df = pd.DataFrame(final_results, columns=columns)
    
# Save Dataframe
df.to_csv('/Users/ep9k/Desktop/twitter_scrape/Data/2022_early.csv')









# exit web driver
# driver.quit()



