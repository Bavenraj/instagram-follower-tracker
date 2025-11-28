import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class Crawler:
    def __init__(self, user_id, password):
        logging.info('--Web Crawling--')
        logging.info("Initializing WebDriver")
        load_dotenv()
        options = Options()
        options.page_load_strategy = 'eager'
        #options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.user_id = user_id
        self.password = password    

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        #SOME INSTAGRAMS CHANGES THE LOGIN METHOD, SO WE CHECK WHICH METHOD IS AVAILABLE
        if WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.NAME, 'username'))):
            #OLD INSTAGRAM LOGIN METHOD
            username_input = self.driver.find_element(by = By.NAME, value = "username")
            username_input.clear()
            username_input.send_keys(self.user_id)#os.getenv("user_id"))
            password_input = self.driver.find_element(by = By.NAME, value = "password")
            password_input.clear()
            password_input.send_keys(self.password)#os.getenv("password"))
            time.sleep(2)
            login_button = self.driver.find_element(by=By.CSS_SELECTOR, value ="[type='submit']")
            login_button.click()
        else:
            #NEW INSTAGRAM LOGIN METHOD
            username_input = self.driver.find_element(by = By.NAME, value = "email")
            username_input.clear()
            username_input.send_keys(self.user_id)#os.getenv("user_id"))
            password_input = self.driver.find_element(by = By.NAME, value = "pass")
            password_input.clear()
            password_input.send_keys(self.password)#os.getenv("password"))
            time.sleep(2)
            login_button = self.driver.find_elements(by=By.CSS_SELECTOR, value ="[role='button']")
            login_button[1].click()

        time.sleep(10)
        self.driver.get(f"https://www.instagram.com/{self.user_id}/")
        time.sleep(10)

    def get_user_details(self, follower_type):
        user_details = self.driver.find_elements(By.CSS_SELECTOR, "[class='x5n08af x1s688f']") # the value showed here may not be correct
        if follower_type not in ['followers', 'following']:
            raise ValueError("follower_type must be either 'followers' or 'following'")
        elif follower_type == 'followers':
            clickable_element = user_details[1].text
        else:
            clickable_element = user_details[2].text
        time.sleep(5)            
        post_count = user_details[0].text
        follower_count = user_details[1].text #incorrect value shown here
        following_count = user_details[2].text #incorrect value shown here
        #print(f'Post Count: {post_count}, Follower Count: {follower_count}, Following Count: {following_count}')
        return clickable_element

    def count_followers(self):
        follower_count_crawled = self.driver.find_elements(by=By.CLASS_NAME, value = "x1qnrgzn")
        return len(follower_count_crawled)

    def count_following(self):
        following_count_crawled = self.driver.find_elements(by=By.CLASS_NAME, value = "x1qnrgzn")
        return len(following_count_crawled)

    def scrape_followers(self):
        self.driver.get(f"https://www.instagram.com/{self.user_id}/")
        time.sleep(10)
        self.get_user_details("followers").click()
        time.sleep(5)   
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
        scrollableElement = self.driver.find_element(By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")
        initial_follower_count = 0
        while True:
            for _ in range(3):
                self.driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
                time.sleep(1)
            print("Number of followers crawled:", self.count_followers())
            if int(initial_follower_count) < self.count_followers():
                initial_follower_count =  self.count_followers()
            else: 
                break
        page_html = self.driver.page_source
        with open(f"follower_page_source.html", "w", encoding="utf-8") as file:
            file.write(page_html)

    def scrape_following(self):
        self.driver.get(f"https://www.instagram.com/{self.user_id}/")
        time.sleep(10)
        self.get_user_details("following").click()
        time.sleep(5)   
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
        scrollableElement = self.driver.find_element(By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")
        initial_following_count = 0
        while True:
            for _ in range(3):
                self.driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
                time.sleep(1)
            print("Number of followings crawled:", self.count_following())
            if int(initial_following_count) < self.count_following():
                initial_following_count =  self.count_following()
            else: 
                break
        page_html = self.driver.page_source
        with open(f"following_page_source.html", "w", encoding="utf-8") as file:
            file.write(page_html)

    def close(self):
        time.sleep(10)
        self.driver.close()
        self.driver.quit()
