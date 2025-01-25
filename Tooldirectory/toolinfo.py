import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_tool_info(url):
    print(f"Fetching tool info for URL: {url}")
    # Setup Chrome driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the URL
        driver.get(url)

        # Extract information
        pricing_type = driver.find_element(By.CSS_SELECTOR, 'div.flex.flex-row.justify-between h5').text
        tool_name = driver.find_element(By.CSS_SELECTOR, 'h1').text
        category = driver.find_element(By.CSS_SELECTOR, 'h6').text
        short_description = driver.find_element(By.CSS_SELECTOR, 'p').text
        link = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/a').get_attribute('href')

        return {
            'Tool Name': tool_name,
            'Category': category,
            'Pricing Type': pricing_type,
            'Short Description': short_description,
            'Link': link
        }

    except Exception as e:
        print(f"Error fetching tool info for URL: {url} - {e}")
        return None

    finally:
        # Close the driver
        driver.quit()

if __name__ == "__main__":
    with open('sample-links.txt', 'r') as file:
        urls = [url.strip() for url in file.readlines() if url.strip()]

    with open('Tooldirectory-sample.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Tool Name', 'Category', 'Pricing Type', 'Short Description', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(get_tool_info, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    tool_info = future.result()
                    if tool_info:
                        writer.writerow(tool_info)
                except Exception as e:
                    print(f"Error processing URL: {url} - {e}")
