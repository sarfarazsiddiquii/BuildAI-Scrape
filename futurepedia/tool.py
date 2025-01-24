import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


with open("output_links.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]


driver = webdriver.Chrome()

all_data = []

for url in urls:
    driver.get(url)

    try:
        tool_name = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/h1")
        short_description = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/p[1]")
        price = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div")
        category_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'capitalize')]")

        categories = [tag.text for tag in category_elements]

        data = {
            "Tool Name": tool_name.text,
            "Short Description": short_description.text,
            "Price": price.text,
            "Categories": ", ".join(categories)  
        }

        all_data.append(data)

    except Exception as e:
        print(f"Error processing {url}: {e}")


fieldnames = ["Tool Name", "Short Description", "Price", "Categories"]
with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)


driver.quit()