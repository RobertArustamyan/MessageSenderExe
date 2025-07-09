import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from selenium.webdriver.support.ui import WebDriverWait
from config import Categories
from bs4 import BeautifulSoup
import time,random
logger = logging.getLogger(__name__)


def load_processed_numbers():
    try:
        with open('processed_numbers.txt', 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_processed_number(number):
    with open('processed_numbers.txt', 'a') as f:
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

class ParseAndMessage:
    def __init__(self,driver, config, pages):
        self.pages = pages
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.login_timeout)


    def _parse_page(self, page_html):
        soup = BeautifulSoup(page_html, 'lxml')
        search_result_div = soup.find('div', id='search-result')

        if search_result_div:
            offers = search_result_div.find_all('a', href=True)
            return list(set(a['href'] for a in offers if '/offer/' in a['href']))

        return []

    def _get_all_offers(self):
        all_links = []
        for page_html in self.pages:
            all_links.extend(self._parse_page(page_html))

        return list(set(all_links))

    def send_messages(self, messages, send_to_all=True,test_mode=True):
        logger.info(f"Starting message sending process. send_to_all: {send_to_all}")

        # Initialize processed numbers set
        try:
            if send_to_all:
                processed = set()
                logger.info("send_to_all=True, starting with empty processed set")
            else:
                with open('processed_numbers.txt', 'r') as f:
                    processed = set(line.strip() for line in f)
                logger.info(f"Loaded {len(processed)} processed numbers from file")
        except FileNotFoundError:
            logger.warning("processed_numbers.txt not found, starting with empty processed set")
            processed = set()
        except Exception as e:
            logger.error(f"Error loading processed numbers: {e}")
            processed = set()

        # Get all offers
        try:
            all_offers = self._get_all_offers()
            logger.info(f"Found {len(all_offers)} total offers to process")
        except Exception as e:
            logger.error(f"Error getting all offers: {e}")
            return

        successful_messages = 0
        skipped_messages = 0
        failed_messages = 0

        for i, offer in enumerate(all_offers, 1):
            logger.info(f"Processing offer {i}/{len(all_offers)}: {offer}")

            try:
                # Navigate to offer page
                full_link = 'https://auto.am' + offer
                logger.debug(f"Navigating to: {full_link}")
                self.driver.get(full_link)

            except Exception as e:
                logger.error(f"Error navigating to offer {offer}: {e}")
                failed_messages += 1
                continue

            try:
                # Click call button to get phone number
                logger.debug("Looking for call button")
                call_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'a.waves-effect.waves-light.btn.blue.modal-trigger.call-seller')
                    )
                )
                call_button.click()
                logger.debug("Call button clicked successfully")

            except Exception as e:
                logger.error(f"Error clicking call button for offer {offer}: {e}")
                failed_messages += 1
                continue

            try:
                # Get phone number
                logger.debug("Extracting phone number")
                phone_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//a[starts-with(@href, "tel:")]'))
                )
                phone_number = phone_element.get_attribute('href').replace('tel:', '')
                logger.debug(f"Phone number extracted: {phone_number}")

            except Exception as e:
                logger.error(f"Error extracting phone number for offer {offer}: {e}")
                failed_messages += 1
                continue

            # Check if already processed
            if phone_number in processed:
                logger.info(f"Phone number {phone_number} already processed, skipping")
                skipped_messages += 1

                # Still need to close the modal
                try:
                    back_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//button[text()="Փակել"]'))
                    )
                    back_button.click()
                    logger.debug("Modal closed after skipping")
                except Exception as e:
                    logger.warning(f"Error closing modal after skipping: {e}")

                continue

            try:
                # Close phone modal
                logger.debug("Closing phone modal")
                back_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Փակել"]'))
                )
                back_button.click()
                logger.debug("Phone modal closed successfully")

            except Exception as e:
                logger.error(f"Error closing phone modal for offer {offer}: {e}")
                failed_messages += 1
                continue

            try:
                # Open message modal
                logger.debug("Opening message modal")
                message_button = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'a.waves-effect.waves-light.btn.blue.modal-trigger.write-seller'
                )
                self.driver.execute_script("arguments[0].click();", message_button)
                logger.debug("Message modal opened successfully")

            except Exception as e:
                logger.error(f"Error opening message modal for offer {offer}: {e}")
                failed_messages += 1
                continue

            try:
                # Send message
                logger.debug("Entering message text")
                message_textarea = self.wait.until(
                    EC.presence_of_element_located((By.ID, 'message-text'))
                )

                message_text = messages.get_random_message()
                message_textarea.send_keys(message_text)
                logger.debug(f"Message entered: {message_text[:50]}...")

                # Random delay before sending
                delay = random.uniform(0, 2)
                logger.debug(f"Waiting {delay:.2f} seconds before sending")
                time.sleep(delay)

            except Exception as e:
                logger.error(f"Error entering message text for offer {offer}: {e}")
                failed_messages += 1
                continue

            try:
                # Send message
                logger.debug("Looking for send button")
                send_button = self.driver.find_element(
                    By.XPATH, "//button[@type='button' and contains(@class, 'swal2-confirm')]"
                )


                if not test_mode:
                    send_button.click()
                logger.info(f"Message would be sent to {phone_number} (send_button.click() is commented out)")

                # Mark as processed
                processed.add(phone_number)
                successful_messages += 1
                logger.info(f"Successfully processed offer {offer} for phone {phone_number}")

            except Exception as e:
                logger.error(f"Error sending message for offer {offer}: {e}")
                failed_messages += 1
                continue

            try:
                # Random delay between messages
                delay = random.uniform(0, 1)
                logger.debug(f"Waiting {delay:.2f} seconds before next message")
                time.sleep(delay)

            except Exception as e:
                logger.warning(f"Error in delay: {e}")


        try:
            logger.info("Saving processed numbers to file")
            with open('processed_numbers.txt', 'w') as f:
                for number in processed:
                    f.write(number + '\n')
            logger.info(f"Successfully saved {len(processed)} processed numbers to file")

        except Exception as e:
            logger.error(f"Error saving processed numbers: {e}")

        logger.info(f"Message sending process completed!")
        logger.info(f"Total offers processed: {len(all_offers)}")
        logger.info(f"Successful messages: {successful_messages}")
        logger.info(f"Skipped messages (already processed): {skipped_messages}")
        logger.info(f"Failed messages: {failed_messages}")
        logger.info(f"Total processed numbers in memory: {len(processed)}")