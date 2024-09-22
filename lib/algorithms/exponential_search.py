from typing import Tuple, Optional, List

class ExponentialSearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the ExponentialSearch instance with the given file path.

        Args:
            file_path (str): The path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content = file_content

    def search(self, target_string: str) -> Tuple[bool, Optional[str]]:
        """
        Search for a target string in the file using exponential search.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        try:
            words = sorted(self.file_content.split())  # Sort words for searching
            return self.exponential_search(words, target_string)
    
        except Exception as e:
            print(ValueError(f"DEBUG: ERROR=> {e}"))
            raise ValueError(f"SSL configuration is incomplete {e}")

        
    def exponential_search(self, arr: List[str], target_string: str) -> Tuple[bool, Optional[str]]:
        """
        Perform exponential search on a sorted array of strings.

        Args:
            arr (List[str]): The sorted list of strings to search in.
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        if arr[0] == target_string:
            return True, arr[0]

        index = 1
        while index < len(arr) and arr[index] <= target_string:
            index *= 2

        # Call binary search on the found range
        return self.binary_search(arr, target_string, index // 2, min(index, len(arr) - 1))

    def binary_search(self, arr: List[str], target_string: str, left: int, right: int) -> Tuple[bool, Optional[str]]:
        """
        Perform binary search on a given range of a sorted array.

        Args:
            arr (List[str]): The sorted list of strings to search in.
            target_string (str): The string to search for.
            left (int): The left index for the binary search.
            right (int): The right index for the binary search.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        while left <= right:
            mid = (left + right) // 2

            if arr[mid] == target_string:
                return True, arr[mid]
            elif arr[mid] < target_string:
                left = mid + 1
            else:
                right = mid - 1

        return False
