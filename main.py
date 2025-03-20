import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from telegram_bot import send_telegram_message

options = Options()

options.add_argument('--headless')  
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 ...')

driver = webdriver.Firefox(options=options)
driver.get('https://mollygram.com/')

search_input = driver.find_element(By.ID, "link")
search_input.send_keys("2.kasar", Keys.ENTER)

max_retries = 3
retry_count = 0
found = False

while retry_count < max_retries and not found:
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "load"))
        )
        found = True
    except TimeoutException:        
        search_input.send_keys("2.kasar", Keys.ENTER)
        retry_count += 1

stories = driver.find_elements(By.CLASS_NAME, "load")
urls = []

for story in stories:
    try:
        img_src = story.find_element(By.TAG_NAME, "img").get_attribute("src")
        url = f"http://tinyurl.com/api-create.php?url={img_src}"
        urls.append(requests.get(url).text)
    except:
        try:
            video = story.find_element(By.TAG_NAME, "video")
            vid_src = video.find_element(By.TAG_NAME, "source").get_attribute("src")
            url = f"http://tinyurl.com/api-create.php?url={vid_src}"
            urls.append(requests.get(url).text)
        except:
            urls.append(None)

driver.quit()

existing_urls = set()
try:
    with open('urls.txt', 'r', encoding='utf-8') as f:
        existing_urls = set(line.strip() for line in f)
except FileNotFoundError:
    pass

new_urls = [url for url in urls if url not in existing_urls]

print(new_urls)

send_telegram_message(new_urls)

with open('urls.txt', 'a', encoding='utf-8') as f:
    for url in new_urls:
        f.write(f"{url}\n")
