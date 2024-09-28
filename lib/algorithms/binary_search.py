import logging
from typing import List, Tuple


class BinarySearch:
    def __init__(self, file_path: str, file_content: str):
        """
        Initialize the BinarySearch instance with the file path and content.
        Args:
            file_path (str): The path to the file for searching strings.
            file_content (str): The content of the file as a single string.
        """
        self.file_path = file_path
        self.file_content = file_content[0]

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Search for a target string using binary search on file content.
        Args:
            target_string (str): The string to search for.
        Returns:
            Tuple[bool, str]: Tuple indicating if the string was found.
        """
        logging.debug(f"Running BinarySearch on {target_string}")
        # Split content into a list and sort it
        words = sorted(self.file_content.split('\n'))

        # Perform the iterative binary search
        result = self.perform_iterative_search(words, target_string)

        if result:
            return True
        else:
            return False

    def perform_iterative_search(self, content: List[str], query: str) -> bool:
        """
        Perform iterative binary search on a list of strings.
        Args:
            content (List[str]): A sorted list of strings for searching.
            query (str): The target string to search.
        Returns:
            bool: A boolean indicating if the string was found.
        """
        # Clean up extra spaces from the search query
        query_clean = query.strip()

        # Set initial search bounds
        left, right = 0, len(content) - 1

        while left <= right:
            mid = (left + right) // 2
            current_item = content[mid].strip()

            if current_item == query_clean:
                logging.debug("Match found")
                return True  # Item found
            elif current_item < query_clean:
                left = mid + 1
            else:
                right = mid - 1

        # Return False if the item wasn't found
        print("Match not found")
        return False
