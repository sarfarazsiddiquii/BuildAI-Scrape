from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

sitemap_url = "https://tooldirectory.ai/sitemap.xml"

# Set up headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Fetch the sitemap URL
driver.get(sitemap_url)
sitemap_content = driver.page_source

# Close the driver
driver.quit()

# Parse the sitemap content
soup = BeautifulSoup(sitemap_content, 'lxml')

# Find all <loc> tags
links = soup.find_all('loc')

# Store the total number of links
total_links = len(links)
print(f"Found {total_links} <loc> tags")

# Write each link that contains "https://tooldirectory.ai/tools/" to a text file
with open('links.txt', 'w') as file:
    for link in links:
        url = link.text
        if "https://tooldirectory.ai/tools/" in url:
            file.write(url + '\n')