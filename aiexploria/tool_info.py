'''expects a json file with links and categories as input.
it gives out product link with features as needed in csv file'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from webdriver_manager.chrome import ChromeDriverManager
import signal
import sys

all_info = []

def get_webpage_info(url, category):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        try:
            short_description = driver.find_element(By.CLASS_NAME, "desc-text").get_attribute("data-title")
        except NoSuchElementException:
            short_description = "NA"

        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
        except NoSuchElementException:
            title = "NA"

        try:
            link = driver.find_element(By.CSS_SELECTOR, ".visit-divy a#specialButton").get_attribute("href")
        except NoSuchElementException:
            link = "NA"

        info = {
            "title": title,
            "short_description": short_description,
            "link": link,
            "category": category
        }
    except TimeoutException:
        info = {
            "title": "NA",
            "short_description": "NA",
            "link": "NA",
            "category": category
        }
    finally:
        driver.quit()

    return info

def save_to_csv(data, filename):
    fieldnames = ["title", "short_description", "link", "category"]
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Exiting gracefully...')
    save_to_csv(all_info, 'output.csv')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    with open("demo-url.json", "r") as file:
        data = json.load(file)


    top_100_data = data[:150]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_webpage_info, item['link'], item['category']) for item in top_100_data]
        for future in as_completed(futures):
            try:
                all_info.append(future.result())
            except Exception as e:
                print(f"Error processing a future: {e}")

    save_to_csv(all_info, 'output.csv')