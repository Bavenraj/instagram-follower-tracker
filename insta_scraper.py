from dotenv import load_dotenv
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

def scrape_users():
    user_type_dict = [{"type":"follower", "username":"[]"},{"type":"following", "username":"[]"}]
    for user_type in user_type_dict:
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

def unfollowers():
    user_list = scrape_users()
    follower_list = user_list[0]["username"]
    following_list = user_list[1]["username"]
    not_following_back = []
    for user in following_list:
        if user not in follower_list:
            not_following_back.append(user)
    print(f'Users not following back: {len(not_following_back)}')

def unfollowing():
    user_list = scrape_users()
    follower_list = user_list[0]["username"]
    following_list = user_list[1]["username"]
    not_following_back = []
    for user in follower_list:
        if user not in following_list:
            not_following_back.append(user)
    print(f'Users I am not following back: {not_following_back}')   
