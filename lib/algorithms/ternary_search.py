from typing import Tuple, List, Optional

class TernarySearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the TernarySearch instance with the given file path.

        Args:
            file_path (str): The path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content = file_content

    def search(self, target_string: str) -> Tuple[bool, Optional[str]]:
        """
        Search for a target string in the file using ternary search.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """

        words = sorted(self.file_content.split())  # Sort words for searching
        return self.ternary_search(words, target_string, 0, len(words) - 1)

    def ternary_search(self, arr: List[str], target_string: str, left: int, right: int) -> Tuple[bool, Optional[str]]:
        """
        Perform ternary search on a sorted array.

        Args:
            arr (List[str]): The sorted list of strings to search in.
            target_string (str): The string to search for.
            left (int): The left index for the search range.
            right (int): The right index for the search range.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        if left > right:
            return False  # Base case: target not found

        third_length = (right - left) // 3
        mid1 = left + third_length
        mid2 = right - third_length

        if arr[mid1] == target_string:
            return True, arr[mid1]  # Target found at mid1
        if arr[mid2] == target_string:
            return True, arr[mid2]  # Target found at mid2

        if target_string < arr[mid1]:
            return self.ternary_search(arr, target_string, left, mid1 - 1)  # Search in the first third
        elif target_string > arr[mid2]:
            return self.ternary_search(arr, target_string, mid2 + 1, right)  # Search in the last third
        else:
            return self.ternary_search(arr, target_string, mid1 + 1, mid2 - 1)  # Search in the middle third
