import pickle
import time
import logging
from typing import List, Dict, Any
from Configurations.config import Config
from Utils.exceptions import CookieExportError

logger = logging.getLogger(__name__)


class CookieManager:
    """Manages cookie extraction and export operations."""

    def __init__(self, driver, config: Config):
        self.driver = driver
        self.config = config

    def export_cookies(self) -> bool:
        """Export cookies to file."""
        try:
            logger.info("Exporting cookies")
            time.sleep(self.config.cookie_export_delay)

            cookies = self._get_cookies()
            if not cookies:
                logger.warning("No cookies found to export")
                return False

            self._save_cookies_to_file(cookies)
            logger.info(f"Successfully exported {len(cookies)} cookies")
            return True

        except Exception as e:
            logger.error(f"Failed to export cookies: {e}")
            raise CookieExportError(f"Cookie export failed: {e}")

    def _get_cookies(self) -> List[Dict[str, Any]]:
        """Get cookies from the driver."""
        self.driver.get('https://auto.am/')
        return self.driver.get_cookies()

    def _save_cookies_to_file(self, cookies: List[Dict[str, Any]]):
        """Save cookies to pickle file."""
        with open(self.config.cookies_file, "wb") as cookies_file:
            pickle.dump(cookies, cookies_file)
