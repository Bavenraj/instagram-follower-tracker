import os
from insta_crawler import Crawler
from insta_scraper import Scraper
import logging
from dotenv import load_dotenv

logging.basicConfig(filename="insta_scrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def crawl_instagram(user_id = os.getenv("user_id"), password = os.getenv("password")):
    crawler = Crawler(user_id, password)
    crawler.login()
    crawler.crawl_followers()
    crawler.crawl_following()
    crawler.close()
def scrape_instagram():
    scraper = Scraper() 
    scraper.extract_details()


#crawl_instagram()
scrape_instagram()