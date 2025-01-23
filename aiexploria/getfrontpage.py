'''get all the links from the front page of aixploria.com and save them to a text file'''

from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.aixploria.com/en/ultimate-list-ai/"
driver = webdriver.Chrome()
driver.get(url)
cards = driver.find_elements(By.CLASS_NAME, "grid-item")

with open("aiexploria_category_links.txt", "w") as file:
    for card in cards:
        blog_list_div = card.find_element(By.CLASS_NAME, "blog-list")
        a_tag_blog = blog_list_div.find_element(By.TAG_NAME, "a")
        href_blog = a_tag_blog.get_attribute("href")
        file.write(href_blog + "\n")
        

driver.quit()
