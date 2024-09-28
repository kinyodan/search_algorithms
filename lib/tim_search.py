from typing import List, Tuple
from lib.check_hash import CheckHash


class TimSortSearch:
    """
    A class for searching a target string using TimSort (Python's default
    sorting algorithm) followed by binary search.

    Attributes:
        file_path (str): Path to the file containing strings to search.
        file_content (str): The content of the file as a string.
    """

    def __init__(self, file_path: str, file_content: str):
        """
        Initializes the instance with the given file path and content.

        Args:
            file_path (str): Path to the file.
            file_content (str): Content of the file to search.
        """
        self.file_path = file_path
        self.file_content = file_content

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Searches for a target string using TimSort, followed by binary search.

        Args:
            target_string (str): The string to find.

        Returns:
            Tuple[bool, str]: Tuple with a bool for found/not found.
        """
        print("DEBUG: Initiating search for target string.")
        # Split the file content into words and sort them
        words = sorted(self.file_content[0])  # uses TimSort

        # Perform binary search on the sorted list of words
        result = self.binary_search(words, target_string)

        if result:
            return True  # found_string found."
        else:
            return False  # target_string not found."

    def binary_search(self,
                      arr: List[str],
                      target_string: str) -> Tuple[bool, str]:
        """
        Searches for target string in a sorted list using binary search.

        Args:
            arr (List[str]): The sorted list to search.
            target_string (str): The string to find.

        Returns:
            Tuple[bool, str]: A tuple with a bool for found/not found and the
                              string itself if found, or None.
        """
        left, right = 0, len(arr) - 1

        while left <= right:
            mid = (left + right) // 2
            current_item = arr[mid].strip()

            if current_item == target_string.strip():
                return True  # Return True and the found string
            elif current_item < target_string.strip():
                left = mid + 1
            else:
                right = mid - 1

        # Return False if the item was not found
        return False
