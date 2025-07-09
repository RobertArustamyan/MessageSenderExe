from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import logging
from config import Config
from exceptions import LoginError

logger = logging.getLogger(__name__)


class LoginHandler:
    """Handles login operations for auto.am website."""

    def __init__(self, driver, config: Config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.login_timeout)

    def login(self) -> bool:
        """Perform complete login process."""
        try:
            self._navigate_to_login_page()
            self._perform_login()
            return True
        except Exception as e:
            logger.error(f"Login process failed: {e}")
            raise LoginError(f"Login failed: {e}")

    def _navigate_to_login_page(self):
        """Navigate to the login page."""
        try:
            logger.info("Opening auto.am login page")
            self.driver.get(self.config.login_url)
            time.sleep(self.config.page_load_delay)
        except WebDriverException as e:
            logger.error(f"Failed to open website: {e}")
            raise LoginError(f"Failed to navigate to login page: {e}")

    def _perform_login(self):
        """Perform the actual login."""
        try:
            logger.info("Attempting to log in")

            # Fill email
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.clear()
            email_input.send_keys(self.config.login_email)

            # Fill password
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.clear()
            password_input.send_keys(self.config.login_password)

            # Submit form
            submit_button = self.wait.until(EC.element_to_be_clickable((By.NAME, "login")))
            self.driver.execute_script("arguments[0].click();", submit_button)

            time.sleep(self.config.login_completion_delay)
            logger.info("Login attempt completed")

        except TimeoutException as e:
            logger.error("Login timeout - elements not found")
            raise LoginError("Login elements not found within timeout period")
        except WebDriverException as e:
            logger.error(f"Login failed: {e}")
            raise LoginError(f"Login operation failed: {e}")