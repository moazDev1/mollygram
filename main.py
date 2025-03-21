import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from telegram_bot import send_telegram_message
import urllib.parse
import json
import os
import time


while True:
    options = Options()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
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

    def get_id(url):
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        media_encoded = query.get("media", [None])[0]
        if media_encoded:
            media_url = urllib.parse.unquote(media_encoded)
            media_parsed = urllib.parse.urlparse(media_url)
            media_query = urllib.parse.parse_qs(media_parsed.query)

            ig_key = media_query.get("ig_cache_key", [None])[0]
            if ig_key:
                return f"img_{ig_key}"

            vs = media_query.get("vs", [None])[0]
            if vs:
                return f"vid_{vs}"

        return None

    urls = []
    links = {}

    for story in stories:
        try:
            img_src = story.find_element(By.TAG_NAME, "img").get_attribute("src")
            id = get_id(img_src)
            url = f"http://tinyurl.com/api-create.php?url={img_src}"
            link = requests.get(url).text
            links[id] = link
        except:
            try:
                video = story.find_element(By.TAG_NAME, "video")
                vid_src = video.find_element(By.TAG_NAME, "source").get_attribute("src")
                id = get_id(vid_src)
                url = f"http://tinyurl.com/api-create.php?url={vid_src}"
                link = requests.get(url).text
                links[id] = link
            except:
                pass

    driver.quit()

    existing_links = {}
    if os.path.exists("links.json"):
        try:
            with open("links.json", "r", encoding="utf-8") as f:
                existing_links = json.load(f)
        except json.JSONDecodeError:
            pass

    new_links = []

    for id, link in links.items():
        if id not in existing_links:
            new_links.append(link)
            existing_links[id] = link

    send_telegram_message(new_links)

    try:
        with open("links.json", "w", encoding="utf-8") as f:
            json.dump(existing_links, f, indent=2)
    except:
        pass

    time.sleep(300)