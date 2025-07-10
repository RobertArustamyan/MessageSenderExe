import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Configurations.categories import Categories
from bs4 import BeautifulSoup
from Parser.parse import ParseAndMessage
import time,random
logger = logging.getLogger(__name__)


def load_processed_numbers():
    try:
        with open('../processed_numbers.txt', 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_processed_number(number):
    with open('../processed_numbers.txt', 'a') as f:
        f.write(number + '\n')


class LoadPages:
    def __init__(self, driver, config, category, start_page, end_page, start_price, end_price):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.login_timeout)

        self.category = category
        self.start_page = start_page
        self.end_page = end_page
        self.start_price = start_price
        self.end_price = end_price

        self.url_template = getattr(Categories, category)

        logger.info(
            f"Initialized LoadPages for category: {category}, pages: {start_page}-{end_page}, price range: ${start_price}-${end_price}")

    def _get_page_html(self, page):
        url = self.url_template.format(page_number=page, start_price=self.start_price, end_price=self.end_price)

        logger.info(f"Loading page {page}")

        try:
            self.driver.get(url)
            logger.debug(f"Successfully navigated to page {page}")

            # Wait for the search results to load
            logger.debug(f"Waiting for search results to load on page {page}")
            self.wait.until(EC.presence_of_element_located((By.ID, "search-result")))
            logger.info(f"Search results loaded successfully on page {page}")

        except Exception as e:
            logger.error(f"Error loading page {page}: {str(e)}")
            logger.warning(f"Continuing with page source retrieval despite error on page {page}")

        page_source = self.driver.page_source
        logger.debug(f"Retrieved page source for page {page} (length: {len(page_source)} characters)")

        return page_source

    @property
    def get_all_pages(self):
        results = []
        try:
            logger.debug("Started page loading")

            for i in range(self.start_page, self.end_page+1):
                results.append(self._get_page_html(i))
        except Exception as e:
            logger.error(f"Error in getting all_pages: {str(e)}")

        return results




# Add this class to page_load_handler.py after the existing ParseAndMessage class

