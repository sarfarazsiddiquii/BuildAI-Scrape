from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


with open("clear-category-links.txt", "r") as file:
    base_urls = [line.strip() for line in file.readlines()]


driver = webdriver.Chrome()


unique_links = set()


with open("output_links.txt", "w") as file:
    for base_url in base_urls:
        page_number = 1
        while True:
            
            url = f"{base_url}?page={page_number}"
            driver.get(url)
            
            
            time.sleep(5)
            
            elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/tool/')]")

            for element in elements:
                href = element.get_attribute("href")
                if href not in unique_links:
                    unique_links.add(href)
                    file.write(f"{href}\n")
            
            try:
                next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
                if not next_button.is_enabled():
                    break
            except NoSuchElementException:
                break
            
            page_number += 1


driver.quit()