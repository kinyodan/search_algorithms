from typing import List, Tuple

class TimSortSearch:
    """
    A class that implements searching for a target string using TimSort (Python's default sorting algorithm) 
    combined with binary search.

    Attributes:
        file_path (str): The path to the file containing strings to search.
        file_content (str): The content of the file as a string.
    """

    def __init__(self, file_path: str, file_content: str):
        """
        Initializes the TimSortSearch instance with the given file path and content.

        Args:
            file_path (str): The path to the file.
            file_content (str): The content of the file to be searched.
        """
        self.file_path = file_path
        self.file_content = file_content

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Searches for a target string using Python's default sorting algorithm (TimSort) followed by binary search.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple where the first value indicates if the string was found, and the second value
                              is the string itself if found, otherwise None.
        """
        words = sorted(self.file_content.split())  # Python uses TimSort for sorting
        return self.binary_search(words, target_string)

    def binary_search(self, arr: List[str], target_string: str) -> Tuple[bool, str]:
        """
        Performs a binary search on a sorted list to find the target string.

        Args:
            arr (List[str]): The sorted list of strings to search.
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple where the first value indicates if the string was found, and the second value
                              is the string itself if found, otherwise None.
        """
        left, right = 0, len(arr) - 1

        while left <= right:
            mid = (left + right) // 2
            current_item = arr[mid]

            if current_item == target_string:
                return True, current_item
            elif current_item < target_string:
                left = mid + 1
            else:
                right = mid - 1

        # If we exit the loop, the item was not found
        return False, None

