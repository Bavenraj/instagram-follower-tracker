from insta_crawler import Crawler
from insta_scraper import Scraper



load_dotenv()
#print(os.getenv("user_id"))

options = Options()
options.page_load_strategy = 'eager'
#options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)
#SOME INSTAGRAMS CHANGES THE LOGIN METHOD, SO WE CHECK WHICH METHOD IS AVAILABLE
if WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, 'username'))):
    #OLD INSTAGRAM LOGIN METHOD
    username_input = driver.find_element(by = By.NAME, value = "username")
    username_input.clear()
    username_input.send_keys(os.getenv("user_id"))
    password_input = driver.find_element(by = By.NAME, value = "password")
    password_input.clear()
    password_input.send_keys(os.getenv("password"))
    time.sleep(2)
    login_button = driver.find_element(by=By.CSS_SELECTOR, value ="[type='submit']")
    login_button.click()
else:
    #NEW INSTAGRAM LOGIN METHOD
    username_input = driver.find_element(by = By.NAME, value = "email")
    username_input.clear()
    username_input.send_keys(os.getenv("user_id"))
    password_input = driver.find_element(by = By.NAME, value = "pass")
    password_input.clear()
    password_input.send_keys(os.getenv("password"))
    time.sleep(2)
    login_button = driver.find_elements(by=By.CSS_SELECTOR, value ="[role='button']")
    login_button[1].click()

time.sleep(10)
driver.get(f"https://www.instagram.com/{os.getenv("user_id")}/")
time.sleep(10)

user_details = driver.find_elements(By.CSS_SELECTOR, "[class='x5n08af x1s688f']") # the value showed here may not be correct
post_count = user_details[0].text
follower_count = user_details[1].text #incorrect value shown here
following_count = user_details[2].text #incorrect value shown here
print(f'Post Count: {post_count}, Follower Count: {follower_count}, Following Count: {following_count}')

def count_followers():
    follower_count_crawled = driver.find_elements(by=By.CLASS_NAME, value = "x1qnrgzn")
    return len(follower_count_crawled)

def count_following():
    following_count_crawled = driver.find_elements(by=By.CLASS_NAME, value = "x1qnrgzn")
    return len(following_count_crawled)

def scrape_followers():
    driver.get(f"https://www.instagram.com/{os.getenv("user_id")}/")
    time.sleep(10)
    user_details[1].click()
    time.sleep(5)   
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    scrollableElement = driver.find_element(By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")
    initial_follower_count = 0
    while True:
        for _ in range(3):
            driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
            time.sleep(1)
        print("Number of followers crawled:", count_followers())
        if int(initial_follower_count) < count_followers():
            initial_follower_count =  count_followers()
        else: 
            break
    page_html = driver.page_source
    with open(f"follower_page_source.html", "w", encoding="utf-8") as file:
        file.write(page_html)

def scrape_following():
    driver.get(f"https://www.instagram.com/{os.getenv("user_id")}/")
    time.sleep(10)
    user_details[2].click()
    time.sleep(5)   
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    scrollableElement = driver.find_element(By.CSS_SELECTOR, "[class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")
    initial_following_count = 0
    while True:
        for _ in range(3):
            driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
            time.sleep(1)
        print("Number of followings crawled:", count_following())
        if int(initial_following_count) < count_following():
            initial_following_count =  count_following()
        else: 
            break
    page_html = driver.page_source
    with open(f"following_page_source.html", "w", encoding="utf-8") as file:
        file.write(page_html)

time.sleep(10)
driver.close()
driver.quit()

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

#unfollowers()