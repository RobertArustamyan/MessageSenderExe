# messages.py
import random
from typing import List, Optional
import logging
import os, datetime, json

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


class MessageDatabase:
    """Simple JSON-based message database"""

    def __init__(self, db_file="AppData/messages_db.json"):
        self.db_file = db_file
        self.messages = self._load_messages()

    def _load_messages(self) -> List[str]:
        """Load messages from JSON file"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('messages', [])
            return []
        except Exception as e:
            print(f"Error loading messages: {e}")
            return []

    def save_messages(self) -> bool:
        """Save messages to JSON file"""
        try:
            data = {
                'messages': self.messages,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving messages: {e}")
            return False

    def add_message(self, message: str) -> bool:
        """Add a new message"""
        if message.strip() and message not in self.messages:
            self.messages.append(message.strip())
            return self.save_messages()
        return False

    def remove_message(self, message: str) -> bool:
        """Remove a message"""
        if message in self.messages:
            self.messages.remove(message)
            return self.save_messages()
        return False

    def get_messages(self) -> List[str]:
        """Get all messages"""
        return self.messages.copy()
