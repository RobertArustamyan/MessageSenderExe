import logging
from typing import Optional
from config import Config
from driver_manager import DriverManager
import pickle
from messages import Messages
from page_load_handler import LoadPages
from page_load_handler import ParseAndMessage


class Sender:
    def __init__(self, headless: bool = False, additional_options: bool = False, config: Optional[Config] = None):
        self.headless = headless
        self.additional_options = additional_options
        self.config = config or Config()

    def send_message(self, cookies_path, category="passenger", start_page=1, end_page=1, start_price="10000",
                     end_price="150000",
                     messages: Messages = None,send_to_all=True,test_mode=True):
        with DriverManager(self.headless, self.additional_options) as driver:
            driver.get('https://auto.am/')

            with open(cookies_path, "rb") as cookies_file:
                cookies = pickle.load(cookies_file)
                for cookie in cookies:
                    driver.add_cookie(cookie)

            driver.refresh()

            loader = LoadPages(driver, self.config, category, start_page, end_page, start_price, end_price)
            parser = ParseAndMessage(driver, self.config, loader.get_all_pages)
            parser.send_messages(messages, send_to_all=send_to_all, test_mode=test_mode)
