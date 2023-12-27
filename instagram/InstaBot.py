import time
import json
import random
from datetime import datetime as dt
#from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class InstagramBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=930,820")
        # Run Chrome in headless mode
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--start-maximized")  # Maximize the Chrome window
        # Use webdriver_manager to automatically download and manage the ChromeDriver
        # add undetected_chromedriver here 
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self, email, password):
        # Open Instagram
        self.driver.get("https://www.instagram.com/")
        # Wait for the login elements to become available
        wait = WebDriverWait(self.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Find the login elements and enter email and password
        email_field.send_keys(email)
        time.sleep(3)
        password_field.send_keys(password)
        time.sleep(1)
        # Submit the login form
        password_field.send_keys(Keys.RETURN)
        print(f"Logged in as : {email}")
        # Wait for the login process to complete (you may need to adjust the delay based on your internet speed)
        time.sleep(10)  # Wait for 5 seconds (adjust as needed)
   
    def getfollowers(self, username, delay):
        names = []
        try:
            link = self.Scrape_post_url(username=username,delay_time=delay)
            self.driver.get(link.replace("reel", "p")+"liked_by/")
            time.sleep(delay)
            # Get likes list
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//section/main/div[1]/div/div')))

            like_list = self.driver.find_elements(By.XPATH,'//section/main/div[1]/div/div//div[2]//a')
            for user_url in like_list:
                names.append(user_url.get_attribute("href").split("/")[-2]) 
            time.sleep(delay)
        except:
            return []
        return list(set(names))
    
    def follow(self, user, delay):
        self.driver.get(f"https://www.instagram.com/{user}")
        try :
            wait = WebDriverWait(self.driver, 10)
            follow_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//section/div//button')))
            time.sleep(3)
            if follow_btn.text.lower() == "follow":
                follow_btn.click()
                time.sleep(10)
        except:
            print(f"can't follow {user}")
            
    def unfollow(self, user, delay):
        self.driver.get(f"https://www.instagram.com/{user}")
        try :
            wait = WebDriverWait(self.driver, 10)
            following_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//section/div//button')))
        
            if following_btn.text.lower() == "following":
                following_btn.click()
                time.sleep(3)
                wait = WebDriverWait(self.driver, 10)
                unfollow_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[2]/div/div/div/div[8]')))
                if unfollow_btn.text.lower() == "unfollow":
                    unfollow_btn.click()
                    time.sleep(3)
        except:
                print(f"can't unfollow {user}")

    def Scrape_post_url(self, username, delay_time): 
        latest_post = ""
        try:
                # Open Instagram and navigate to the user stories page
                self.driver.get(f"https://www.instagram.com/{username}/")

                # Wait for the stories to load
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.XPATH, '//div/div[3]/article/div[1]/div')))

                most_recent = self.driver.find_element(By.XPATH, '//div/div[3]/article/div[1]/div')
            
                # Scrape the most recent posts from the profile
                posts = most_recent.find_elements(By.TAG_NAME, "a")
                # Retrieve the href attribute value
                latest_post = posts[0].get_attribute("href")
        except :
            pass

        return latest_post

    def quit(self):
        self.driver.quit()
