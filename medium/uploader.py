import os
import pickle
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MediumUploader:
    COOKIE_FILE = "medium_cookies.pkl"
    LOGIN_URL = "https://medium.com/m/signin"
    HOME_URL = "https://medium.com/"

    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def human_type(self, element, text: str, min_delay: float = 0.05, max_delay: float = 0.15):
        """
        Types text into the element character by character with random delays
        to simulate human typing and avoid captchas.
        """
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(min_delay, max_delay))
    
    def save_cookies(self):
        with open(self.COOKIE_FILE, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)

    def load_cookies(self):
        with open(self.COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            if isinstance(cookie.get("expiry", None), float):
                cookie["expiry"] = int(cookie["expiry"])
            self.driver.add_cookie(cookie)

    def login(self, email: str, password: str):
        self.driver.get(self.LOGIN_URL)

        if os.path.exists(self.COOKIE_FILE):
            self.load_cookies()
            self.driver.refresh()
            return

        facebook_button = self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class,'by') and contains(@class,'bz') and starts-with(@href, '//medium.com/m/connect/facebook')]"
        )))

        facebook_button.click()
        email_input = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "input[name='email']"
        )))

        email_input.click()
        self.human_type(email_input, email)

        password_input = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "input[name='pass']"
        )))

        password_input.click()
        self.human_type(password_input, password)
        time.sleep(5)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

        continue_button = self.wait.until(EC.presence_of_element_located((
            By.CLASS_NAME,
            'div.x1e0frkt'
        )))

        continue_button.click()
        time.sleep(10)
        if self.driver.current_url == self.HOME_URL:
            self.save_cookies()

    def publish(self, article: object):
        self.driver.get("https://medium.com/new-story")
        article_input = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "div.postArticle-content.js-postField.js-notesSource.editable"
        )))

        article_input.click()
        article_input.send_keys(article["title"])
        article_input.send_keys(Keys.ENTER)

        article_input.send_keys(Keys.CONTROL, Keys.ALT, "2")
        article_input.send_keys(article["subtitle"])
        article_input.send_keys(Keys.ENTER)
        time.sleep(0.5)

        add_media_button = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[title*='Add an image, video, embed']"
        ))) 

        add_media_button.click()
        unsplash_button = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[title*='Unsplash']"
        )))
        
        unsplash_button.click()
        search_input = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "div.js-unsplashImageInput.unsplashInput.editable"
        )))

        search_input.send_keys(article["image"])
        search_input.send_keys(Keys.ENTER)
        time.sleep(0.5)

        image_button = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "div.unsplashImage"
        )))

        image_button.click()
        time.sleep(0.1)
        article_input.click()

        paragraphs = article["body"].split("/n")
        for paragraph in paragraphs:
            if paragraph.strip() == "":
                continue
            if "##" in paragraph:
                paragraph = paragraph.replace("##", "")
                article_input.send_keys(Keys.CONTROL, Keys.ALT, "5")
            
            paragraph = paragraph.replace("/", "")
            words = paragraph.split(" ")

            for word in words:
                if word.strip() == "":
                    continue
                if "*" in word:
                    word = word.replace("*", "")
                    article_input.send_keys(Keys.CONTROL, "i")
                    time.sleep(0.1)
                    article_input.send_keys(word.strip())
                    time.sleep(0.1)
                    article_input.send_keys(Keys.CONTROL, "i")
                else:
                    article_input.send_keys(word.strip())
                
                article_input.send_keys(Keys.SPACE)

            article_input.send_keys(Keys.ENTER)

        time.sleep(0.5)
        publish_button = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[data-action='show-prepublish']"
        )))

        publish_button.click()
        time.sleep(0.5)
        tags_input = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "div.js-tagInput.tags-input.editable"
        )))

        tags_input.click()
        tags = article["tags"].split(",")
        for tag in tags:
            tag = tag.strip()
            if tag == "":
                continue
            tags_input.send_keys(tag)
            tags_input.send_keys(Keys.ENTER)
            time.sleep(0.1)

        #publish_button = self.wait.until(EC.element_to_be_clickable((
        #    By.CSS_SELECTOR,
        #    "button[data-action='publish']"
        #)))

        #publish_button.click()
