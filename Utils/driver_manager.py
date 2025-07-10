from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
import logging
from typing import Optional
from Utils.exceptions import DriverInitializationError

logger = logging.getLogger(__name__)


class DriverManager:
    """Manages Chrome WebDriver initialization and cleanup."""

    def __init__(self, headless: bool = False, additional_options: bool = False):
        self.headless = headless
        self.additional_options = additional_options
        self._driver: Optional[webdriver.Chrome] = None

    def __enter__(self):
        """Context manager entry."""
        self._driver = self._initialize_driver()
        return self._driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.quit_driver()

    def _initialize_driver(self) -> webdriver.Chrome:
        """Initialize Chrome driver with options."""
        load_dotenv()

        options = self._get_chrome_options()

        try:
            driver = webdriver.Chrome(options=options)
            logger.info("Chrome driver initialized successfully")
            return driver
        except WebDriverException as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise DriverInitializationError(f"Driver initialization failed: {e}")

    def _get_chrome_options(self) -> Options:
        """Get Chrome options based on configuration."""
        options = Options()

        if self.headless:
            options.add_argument("--headless")

        if self.additional_options:
            additional_args = [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1920,1080",
                "--disable-gpu",
                "--disable-extensions",
                "--disable-blink-features=AutomationControlled"
            ]
            for arg in additional_args:
                options.add_argument(arg)

        return options

    def quit_driver(self):
        """Quit the driver safely."""
        if self._driver:
            try:
                self._driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.warning(f"Error closing driver: {e}")
            finally:
                self._driver = None