import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


with open('finaloutputdemo.txt', 'r') as file:
    urls = file.read().splitlines()

driver = webdriver.Chrome()


with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Tool Name", "Short Description", "Link", "Price", "Categories"])
    for url in urls:
        print(f"Processing URL: {url}")
        driver.get(url)
        try:
            tool_name = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/h1")
            short_description = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/p[1]")
            link = driver.find_element(By.XPATH, "//a[contains(@class, 'hover:no-underline')]").get_attribute("href")
            price = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div")
            category_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'capitalize')]")
            categories = [tag.text for tag in category_elements]
            data = {
                "Tool Name": tool_name.text,
                "Short Description": short_description.text,
                "Link": link,
                "Price": price.text,
                "Categories": categories
            }
            writer.writerow([data["Tool Name"], data["Short Description"], data["Link"], data["Price"], ", ".join(data["Categories"])])
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")


driver.quit()
print("CSV file created successfully.")