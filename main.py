from config import MEDIUM_EMAIL, MEDIUM_PASSWORD
from deepseek.client import generate_article
from medium.uploader import MediumUploader
from automation.browser import get_driver
from utils import get_logger
import time

logger = get_logger(__name__)

def run():
    logger.info("Generating article content")
    article = generate_article()
    print(article)
    logger.info("Article content generated")

    logger.info("Starting Chrome WebDriver")
    driver = get_driver(headless=False) # Set to False for debugging
    logger.info("Chrome WebDriver started")


    logger.info("Logging into Medium")
    uploader = MediumUploader(driver)
    uploader.login(MEDIUM_EMAIL, MEDIUM_PASSWORD)
    logger.info("Logged into Medium")

    logger.info("Publishing article")
    uploader.publish(article)
    logger.info("Article published")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    run()
