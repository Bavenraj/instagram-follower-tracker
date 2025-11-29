import os
from insta_crawler import Crawler
from insta_scraper import Scraper
import logging
from dotenv import load_dotenv

logging.basicConfig(filename="insta_scrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

Crawler = Crawler(user_id= os.getenv("user_id"), password= os.getenv("password"))
Crawler.login()
Crawler.crawl_followers()
Crawler.crawl_following()
Crawler.close()
Scraper = Scraper() 
Scraper.extract_details()


