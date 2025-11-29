from bs4 import BeautifulSoup
import logging
import pandas as pd

class Scraper:
    def __init__(self):
        logging.info('--Web Scraping--')
        pass

    def scrape_users(self):
        logging.info("Scraping user details from saved HTML files")
        user_type_dict = [{"type":"follower", "username":"[]"},{"type":"following", "username":"[]"}]
        for user_type in user_type_dict:
            logging.info(f"Scraping {user_type['type']} data")
            page_source = f"{user_type["type"]}.html"
            username_list = f"{user_type["type"]}_list" 
            username_list = []
            soup = BeautifulSoup(open(page_source, encoding='utf-8').read(), 'html.parser')
            user_list = soup.find_all(name='div', attrs={"class": "x1qnrgzn"})
            for user in user_list:
                username = user.find(name='a').get("href").replace("/", "")
                username_list.append(username)                
            user_type["username"] = username_list
        return user_type_dict

    def unfollowers(self):
        user_list = self.scrape_users()
        follower_list = user_list[0]["username"]
        following_list = user_list[1]["username"]
        not_follower_back = []
        for user in following_list:
            if user not in follower_list:
                not_follower_back.append(user)
        #print(f'Users not following back: {len(not_follower_back)}')
        return not_follower_back

    def unfollowing(self):
        user_list = self.scrape_users()
        follower_list = user_list[0]["username"]
        following_list = user_list[1]["username"]
        not_following_back = []
        for user in follower_list:
            if user not in following_list:
                not_following_back.append(user)
        #print(f'Users I am not following back: {not_following_back}')   
        return not_following_back
    
    def mutual_followers(self):
        user_list = self.scrape_users()
        follower_list = user_list[0]["username"]
        following_list = user_list[1]["username"]
        mutuals = []
        for user in following_list:
            if user in follower_list:
                mutuals.append(user)
        #print(f'Mutual followers: {mutuals}')   
        return mutuals
    
    def extract_details(self):
        df1 = pd.DataFrame({
            "username": self.unfollowers(),
            "follower_type": "Unfollower"
        })
        df2 = pd.DataFrame({
            "username": self.unfollowing(),
            "follower_type": "Unfollowing"
        })
        df3 = pd.DataFrame({
            "username": self.mutual_followers(),
            "follower_type": "Mutual"
        })
        with pd.ExcelWriter('instagram_followers_analysis.xlsx') as writer:
            df1.to_excel(writer, sheet_name='Unfollowers', index=True)
            df2.to_excel(writer, sheet_name='Unfollowing', index=True)
            df3.to_excel(writer, sheet_name='Mutual Followers', index=True)

