import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for the cookie extractor."""
    login_url: str = "https://auto.am/login"
    cookies_file: str = "AppData/cookies.pkl"
    login_timeout: int = 10
    page_load_delay: int = 2
    login_completion_delay: int = 3
    cookie_export_delay: int = 5
    login_email: str = ""
    login_password: str = ""



