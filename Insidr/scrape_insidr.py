import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import logging
from dataclasses import dataclass
from typing import List, Optional
import os

@dataclass
class AITool:
    """Data class to store information about an AI tool."""
    name: str
    description: str
    pricing_type: str
    price: str
    link: str
    categories: str

    @classmethod
    def from_element(cls, element) -> 'AITool':
        """Create an AITool instance from a web element."""
        def safe_get_text(class_name: str) -> str:
            try:
                return element.find_element(By.CLASS_NAME, class_name).text
            except NoSuchElementException:
                return "NA"

        def safe_get_link(class_name: str) -> str:
            try:
                return element.find_element(By.CLASS_NAME, class_name).get_attribute("href")
            except NoSuchElementException:
                return "NA"

        return cls(
            name=safe_get_text("aitools-tool-title"),
            description=safe_get_text("aitools-tool-description"),
            pricing_type=safe_get_text("pricing-type"),
            price=safe_get_text("pricing-price"),
            link=safe_get_link("aitools-visit-link"),
            categories=safe_get_text("aitools-tool-categories")
        )

class AIToolsScraper:
    """Class to handle the scraping of AI tools data."""
    
    def __init__(self, headless: bool = False, timeout: int = 10):
        self.base_url = "https://www.insidr.ai/ai-tools/"
        self.timeout = timeout
        self.setup_logging()
        self.driver = self.setup_driver(headless)
        
    def setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self, headless: bool) -> uc.Chrome:
        """Initialize and configure the Chrome driver."""
        options = uc.ChromeOptions()
        options.headless = headless
        return uc.Chrome(use_subprocess=False, options=options)

    def get_page_url(self, page_num: int) -> str:
        """Generate URL for a specific page number."""
        return f"{self.base_url}" if page_num == 1 else f"{self.base_url}page/{page_num}/"

    def scrape_page(self, page_num: int) -> List[AITool]:
        """Scrape a single page and return list of AITool objects."""
        url = self.get_page_url(page_num)
        self.logger.info(f"Scraping page {page_num}: {url}")
        
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "aitools-item"))
            )
            
            posts = self.driver.find_elements(By.CLASS_NAME, "aitools-item")
            return [AITool.from_element(post) for post in posts]
            
        except TimeoutException:
            self.logger.error(f"Timeout waiting for page {page_num} to load")
            return []
        except Exception as e:
            self.logger.error(f"Error scraping page {page_num}: {str(e)}")
            return []

    def save_to_csv(self, tools: List[AITool], filename: str):
        """Save the scraped data to a CSV file."""
        fieldnames = ["Tool Name", "Tool Description", "Pricing Type", 
                     "Tool Rate", "Tool Link", "Hashtags"]
        
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for tool in tools:
                    writer.writerow({
                        "Tool Name": tool.name,
                        "Tool Description": tool.description,
                        "Pricing Type": tool.pricing_type,
                        "Tool Rate": tool.price,
                        "Tool Link": tool.link,
                        "Hashtags": tool.categories
                    })
            self.logger.info(f"Data successfully saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {str(e)}")

    def run(self, num_pages: int, output_file: str):
        """Run the complete scraping process."""
        try:
            all_tools = []
            for page_num in range(1, num_pages + 1):
                tools = self.scrape_page(page_num)
                all_tools.extend(tools)
                time.sleep(2)  
            
            self.save_to_csv(all_tools, output_file)
            
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {str(e)}")
        finally:
            self.driver.quit()

def main():
    scraper = AIToolsScraper(headless=False)
    scraper.run(num_pages=1, output_file="ai_tools_data.csv")

if __name__ == "__main__":
    main()
    
    
    