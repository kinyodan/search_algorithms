from typing import List, Optional

def binary_search(arr: List[str], target: str, left: int, right: int) -> int:
    """
    Perform a binary search on a sorted array.

    Args:
        arr (List[str]): The sorted array to search.
        target (str): The string to find.
        left (int): The starting index of the search range.
        right (int): The ending index of the search range.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def exponential_search(arr: List[str], target: str) -> int:
    """
    Perform an exponential search on a sorted array.

    Args:
        arr (List[str]): The sorted array to search.
        target (str): The string to find.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    # Check if the first element is the target
    if arr[0] == target:
        return 0
    
    # Find the range for binary search by doubling the index
    index = 1
    while index < len(arr) and arr[index] <= target:
        index *= 2

    # Perform binary search in the found range
    return binary_search(arr, target, index // 2, min(index, len(arr) - 1))

class GraphBasedSearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the search instance with the given file path.

        Args:
            file_path (str): The path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content = file_content

    def load_strings_from_file(self) -> List[str]:
        """
        Load strings from the file and return them as a list.

        Returns:
            List[str]: A list of strings loaded from the file.
        """

        strings_list = self.file_content.strip().split('\n')  # Split the content by lines into a list of strings
        return strings_list

    def search(self, target_string: str) -> int:
        """
        Search for a target string using exponential search.

        Args:
            target_string (str): The string to search for.

        Returns:
            int: The index of the target string if found, otherwise -1.
        """
        strings_list = self.load_strings_from_file()
        return exponential_search(strings_list, target_string)
