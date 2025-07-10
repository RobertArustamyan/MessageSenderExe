from typing import Optional
from Configurations.config import Config
from Messages.messages import Messages
from Parser.parse import ParseAndMessage
from Utils.driver_manager import DriverManager
import pickle
from Parser.customParse import CustomParseAndMessage
from Parser.page_load_handler import LoadPages


class Sender:
    def __init__(self, headless: bool = False, additional_options: bool = False, config: Optional[Config] = None):
        self.headless = headless
        self.additional_options = additional_options
        self.config = config or Config()

    def send_message(self, cookies_path, category="passenger", start_page=1, end_page=1, start_price="10000",
                     end_price="150000",
                     messages: Messages = None, send_to_all=True, test_mode=True):
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


# Custom Sender class that can send progress updates to the GUI
class CustomSender(Sender):
    def __init__(self, headless=False, additional_options=False, config=None, progress_callback=None):
        super().__init__(headless, additional_options, config)
        self.progress_callback = progress_callback

    def send_message(self, cookies_path, category="passenger", start_page=1, end_page=1, start_price="10000",
                     end_price="150000", messages=None, send_to_all=True, test_mode=True):

        if self.progress_callback:
            self.progress_callback("Initializing browser and loading cookies...")

        with DriverManager(self.headless, self.additional_options) as driver:
            driver.get('https://auto.am/')

            with open(cookies_path, "rb") as cookies_file:
                cookies = pickle.load(cookies_file)
                for cookie in cookies:
                    driver.add_cookie(cookie)

            driver.refresh()

            if self.progress_callback:
                self.progress_callback("Loading pages...", "Loading pages...")

            loader = LoadPages(driver, self.config, category, start_page, end_page, start_price, end_price)

            # Use custom parser that can send progress updates
            parser = CustomParseAndMessage(driver, self.config, loader.get_all_pages, self.progress_callback)
            parser.send_messages(messages, send_to_all=send_to_all, test_mode=test_mode)
