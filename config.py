import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for the cookie extractor."""
    login_url: str = "https://auto.am/login"
    cookies_file: str = "cookies.pkl"
    login_timeout: int = 10
    page_load_delay: int = 2
    login_completion_delay: int = 3
    cookie_export_delay: int = 5
    login_email: str = ""
    login_password: str = ""



@dataclass
class Categories:
    all = "https://auto.am/search/all?q={{%22category%22:%2251%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"

    passenger = "https://auto.am/search/passenger-cars?q={{%22category%22:%221%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"

    trucks = "https://auto.am/search/trucks?q={{%22category%22:%225%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"

    motorcycles = "https://auto.am/search/motorcycles?q={{%22category%22:%222%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"

    special = "https://auto.am/search/special-motor-vehicle?q={{%22category%22:%226%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"

    buses = "https://auto.am/search/buses?q={{%22category%22:%224%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"

    trailers = "https://auto.am/search/trailers?q={{%22category%22:%2230%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"

    water = "https://auto.am/search/water-vehicles?q={{%22category%22:%2225%22,%22page%22:%22{page_number}%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{{%22dealer%22:%220%22,%22official%22:%220%22,%22id%22:%22%22}},%22year%22:{{%22gt%22:%221911%22,%22lt%22:%222026%22}},%22usdprice%22:{{%22gt%22:%22{start_price}%22,%22lt%22:%22{end_price}%22}},%22custcleared%22:%221%22,%22mileage%22:{{%22gt%22:%2210%22,%22lt%22:%221000000%22}}}}"
