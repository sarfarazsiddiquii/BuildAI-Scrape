'''expects a json file with links and categories as input.
it gives out product link with features as needed in csv file'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import json
import time

def get_webpage_info(driver, url, category):
    driver.get(url)
    time.sleep(3)  

    try:
    
        short_description = driver.find_element(By.CLASS_NAME, "desc-text").get_attribute("data-title")
        title = driver.find_element(By.TAG_NAME, "h1").text
        link = driver.find_element(By.CSS_SELECTOR, ".visit-divy a#specialButton").get_attribute("href")

        
        info = {
            "title": title,
            "short_description": short_description,
            "link": link,
            "category": category
        }
    except Exception as e:
        info = {
            "title": "Error",
            "short_description": "Error",
            "link": "Error",
            "category": category,
            "error": str(e)
        }

    return info

def save_to_csv(data, filename):
    fieldnames = ["title", "short_description", "link", "category"]
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":

    with open("urls.json", "r") as file:
        data = json.load(file)

 
    driver = webdriver.Chrome()


    all_info = []
    for item in data:
        url = item['link']
        category = item['category']
        info = get_webpage_info(driver, url, category)
        all_info.append(info)


    save_to_csv(all_info, 'output.csv')

    driver.quit()
