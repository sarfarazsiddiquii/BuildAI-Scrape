from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.futurepedia.io/ai-tools"
driver = webdriver.Chrome()
driver.get(url)


elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'flex')]/a")

with open("clear-category-links.txt", "w") as file:
    for element in elements:
        href = element.get_attribute("href")
        file.write(f"{href}\n")

driver.quit()
