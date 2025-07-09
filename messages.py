# messages.py
import random
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class Messages:
    """Class to manage predefined messages with random selection capability."""

    def __init__(self):
        self._messages = [
            "1",
            "2",
            "3",
            "4",
            "5"
        ]

    def get_random_message(self) -> str:
        """
        Get a random message from the predefined list.

        Returns:
            str: A randomly selected message
        """

        message = random.choice(self._messages)
        # logger.info(f"Selected random message: {message[:30]}...")
        return message

    def get_all_messages(self) -> List[str]:
        """
        Get all available messages.

        Returns:
            List[str]: List of all messages
        """
        return self._messages.copy()

    def get_message_by_index(self, index: int) -> Optional[str]:
        """
        Get a specific message by index.

        Args:
            index: Index of the message (0-based)

        Returns:
            Optional[str]: Message at the specified index, or None if invalid index
        """
        if 0 <= index < len(self._messages):
            return self._messages[index]

        logger.warning(f"Invalid message index: {index}")
        return None

    def add_message(self, message):
        self._messages.append(message)