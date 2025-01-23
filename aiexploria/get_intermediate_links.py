'''
After getting the category links from getfrontpage.py, 
this will get the product links from each category link 
(expects output from getfrontpage.py in a text file)
'''
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


with open("aiexploria_category_links.txt", "r") as file:
    urls = file.readlines()


driver = webdriver.Chrome()

all_links = []

for base_url in urls:
    base_url = base_url.strip()
    page_number = 1

    while page_number <= 3:  # Limit to the first 3 pages CHANGE THIS WHILE SCRAPING
        url = f"{base_url}/page/{page_number}/"
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Find all post items
        post_titles = driver.find_elements(By.CLASS_NAME, "post-title")
        if not post_titles:
            break
        
        try:
            category_element = driver.find_element(By.XPATH, '//span[@class="master-cat-title"]')
            category = category_element.get_attribute("data-title")
        except Exception as e:
            category = "Unknown"
            
        # Output only the first 2 links from each page CHANGE THIS WHILE SCRAPING
        for post_title in post_titles[:2]:
            link = post_title.find_element(By.TAG_NAME, "a").get_attribute("href")
            all_links.append({"link": link, "category": category})

        page_number += 1


driver.quit()


with open("urls.json", "w", encoding="utf-8") as output_file:
    json.dump(all_links, output_file, ensure_ascii=False, indent=4)