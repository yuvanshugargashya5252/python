import time
import random
import logging
import pandas as pd
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pydantic import BaseModel
import pdb;
from datetime import datetime
import os



USERNAME = 'USER'
PASSWORD = 'PASS123'

proxies = {
    'http': f'http://user-{USERNAME}:{PASSWORD}@dc.oxylabs.io:8000',
    'https': f'https://user-{USERNAME}:{PASSWORD}@dc.oxylabs.io:8000'
}

custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}


class Product(BaseModel):
    title: Optional[str]
    url: str
    asin_code: str
    image_url: Optional[str]
    price: Optional[str]
    rating: Optional[str] = None
    monthly_sales: Optional[str] = None
    # description: Optional[str] = None


class AmazonScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.implicitly_wait(10)
        return driver

    def get_product_details(self, url: str) -> dict:
        try:
            # pdb.set_trace()
            response = requests.get(url, headers=custom_headers, proxies=proxies, timeout=10)
            if response.status_code != 200:
                return {}
            soup = BeautifulSoup(response.text, 'lxml')

            rating_element = soup.select_one('#acrPopover')
            rating_text = rating_element.attrs.get('title') if rating_element else None
            rating = rating_text.replace('out of 5 stars', '').strip() if rating_text else None

            description_element = soup.select_one('#productDescription') or soup.select_one('#feature-bullets')
            description = description_element.text.strip() if description_element else None

            return {
                'rating': rating,
                'description': description
            }
        except Exception as e:
            self.logger.warning(f"Failed to fetch product details from {url}: {e}")
            return {}

    def scrape_amazon_page(self, url: str) -> List[Product]:
        driver = self._initialize_driver()
        self.logger.info(f"Navigating to: {url}")
        driver.get(url)
        time.sleep(3)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = os.path.join("screenshots", f"amazon_page_{timestamp}.png")
        driver.save_screenshot(screenshot_path)

        products = []

        try:
            page = 1
            while True:
                self.logger.info(f"Scraping page {page}")
                product_elements = driver.find_elements(
                    By.CSS_SELECTOR, "div[data-asin][data-component-type='s-search-result']"
                )
                self.logger.info(f"Found {len(product_elements)} products on page {page}")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                os.makedirs("screenshots", exist_ok=True)
                screenshot_path = os.path.join("screenshots", f"amazon_page_{timestamp}.png")
                driver.save_screenshot(screenshot_path)

                for element in product_elements:
                    try:
                        # Title
                        try:
                            title_el = element.find_element(
                                By.CSS_SELECTOR,
                                "h2.a-size-medium.a-color-base.a-text-normal span"
                            )
                            title = title_el.text.strip()
                        except:
                            title = "N/A"

                        # Product URL
                        try:
                            product_url_el = element.find_element(
                                By.CSS_SELECTOR,
                                "h2.a-size-medium.a-color-base.a-text-normal"
                            )
                            product_url = product_url_el.find_element(By.XPATH, "..").get_attribute("href")
                        except:
                            product_url = ""

                        # ASIN
                        asin_code = element.get_attribute("data-asin").strip()

                        # Image URL
                        try:
                            image_url = element.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
                        except:
                            image_url = ""

                        # Price
                        try:
                            price_element = element.find_element(
                                By.CSS_SELECTOR,
                                "div[data-cy='secondary-offer-recipe'] span.a-color-base"
                            )
                            price = price_element.text.strip()
                        except:
                            price = None

                        # Rating
                        try:
                            rating_element = element.find_element(By.CSS_SELECTOR, "i.a-icon-star-small span.a-icon-alt")
                            rating_text = rating_element.get_attribute("textContent").strip()
                            print(f"Rating text: {rating_text}")
                            rating = rating_text.split(" out of")[0]
                        except:
                            rating = None

                        try:
                            sales_element = element.find_element(By.XPATH, ".//span[contains(text(), 'bought in past month')]")
                            sales_text = sales_element.text.strip()
                            print(f"Sales text: {sales_text}")
                            monthly_sales = sales_text.split(' ')[0]  # Get only "10K+"
                        except:
                            monthly_sales = None

                        # Description (from product page — you can replace this with actual scraping if needed)
                        # description = ""

                        product = Product(
                            title=title,
                            url=product_url,
                            asin_code=asin_code,
                            image_url=image_url,
                            price=price,
                            rating=rating,
                            # description=description,
                            monthly_sales=monthly_sales
                        )
                        products.append(product)
                        time.sleep(random.uniform(1.5, 3.0))

                    except Exception as e:
                        self.logger.warning(f"Error extracting product: {e}")

                # Try to click the "Next" button
                try:
                    next_btn = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
                    next_btn_classes = next_btn.get_attribute("class")

                    if "s-pagination-disabled" in next_btn_classes:
                        self.logger.info("Reached last page. Exiting loop.")
                        break
                    else:
                        self.logger.info("Moving to next page...")
                        driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(random.uniform(4, 6))
                        page += 1
                except Exception as e:
                    self.logger.info(f"No next button found or could not navigate: {e}")
                    break

        except Exception as e:
            self.logger.error(f"Error scraping product list: {e}")
        finally:
            driver.quit()

        return products



# Example use
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    url = "https://www.amazon.com/s?k=wireless+headphones"
    scraper = AmazonScraper()
    print(f"Scraping products from: {url}")
    results = scraper.scrape_amazon_page(url)

    df = pd.DataFrame([product.dict() for product in results])
    df.to_csv("amazon_scraped_data.csv", index=False)
    print("Saved data to amazon_scraped_data.csv")
