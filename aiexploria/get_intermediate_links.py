'''
After getting the category links from getfrontpage.py, 
this will get the product links from each category link 
(expects output from getfrontpage.py in a text file)
'''
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open("aiexploria_category_links.txt", "r") as file:
    urls = file.readlines()


options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

all_links = []

for base_url in urls:
    base_url = base_url.strip()
    page_number = 1

    while True:  
        url = f"{base_url}/page/{page_number}/"
        logging.info(f"Processing URL: {url}")
        driver.get(url)

        try:
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "post-title"))
            )

            post_titles = driver.find_elements(By.CLASS_NAME, "post-title")
            if not post_titles:
                break

            try:
                category_element = driver.find_element(By.XPATH, '//span[@class="master-cat-title"]')
                category = category_element.get_attribute("data-title")
            except NoSuchElementException:
                category = "Unknown"

            
            for post_title in post_titles:
                link = post_title.find_element(By.TAG_NAME, "a").get_attribute("href")
                all_links.append({"link": link, "category": category})

            
            try:
                next_button = driver.find_element(By.XPATH, '//a[@class="next page-numbers"]')
                if "disabled" in next_button.get_attribute("class"):
                    break
            except NoSuchElementException:
                break

        except TimeoutException:
            logging.error(f"Timeout waiting for page {page_number} to load")
            break
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")
            break

        page_number += 1

driver.quit()

with open("urls.json", "w", encoding="utf-8") as output_file:
    json.dump(all_links, output_file, ensure_ascii=False, indent=4)