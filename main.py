import os
from insta_crawler import Crawler
from insta_scraper import Scraper
from dotenv import load_dotenv

load_dotenv()
Crawler = Crawler(user_id= os.getenv("user_id"), password= os.getenv("password"))

Crawler.login()
Crawler.scrape_followers()
Crawler.scrape_following()
Crawler.close()
