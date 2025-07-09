import logging
from dotenv import load_dotenv
from cookie_extractor import CookieExtractor
from message_sender import Sender
from messages import Messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main(new_cookies=False):
    load_dotenv()
    if new_cookies:
        try:
            extractor = CookieExtractor(headless=True, additional_options=True)
            success = extractor.extract_cookies()

            if success:
                print("Cookies extracted successfully!")
            else:
                print("Cookie extraction failed!")
        except Exception as e:
            print(f"Error in cookie extractor: {e}")
            return 1
    try:
        sender = Sender(headless=False, additional_options=True)
        sender.send_message("cookies.pkl", "passenger", start_page=1, end_page=1, start_price="10000",end_price="150000",messages=Messages())
    except Exception as e:
        print(f"Error in sender: {e}")
        return 1


if __name__ == "__main__":
    exit(main())