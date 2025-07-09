import logging
from typing import Optional
from config import Config
from driver_manager import DriverManager
from login_handler import LoginHandler
from cookie_manager import CookieManager
from exceptions import CookieExtractorError

logger = logging.getLogger(__name__)


class CookieExtractor:
    """Main class for extracting cookies from auto.am website."""

    def __init__(self, headless: bool = False, additional_options: bool = False, config: Optional[Config] = None,
                 login: str = "", password: str = ""):
        self.headless = headless
        self.additional_options = additional_options
        self.config = config or Config()
        self.config.login_email = login
        self.config.login_password = password

    def extract_cookies(self) -> bool:
        """Extract cookies from the website."""
        try:
            with DriverManager(self.headless, self.additional_options) as driver:
                # Initialize handlers
                login_handler = LoginHandler(driver, self.config)
                cookie_manager = CookieManager(driver, self.config)

                # Perform operations
                login_handler.login()

                cookie_manager.export_cookies()

                logger.info("Cookie extraction completed successfully")
                return True

        except CookieExtractorError as e:
            logger.error(f"Cookie extraction failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during cookie extraction: {e}")
            return False
