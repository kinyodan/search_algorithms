from typing import List

def binary_search(arr: List[str], target: str, left: int, right: int) -> bool:
    """
    Perform a binary search on a sorted array.

    Args:
        arr (List[str]): The sorted array to search.
        target (str): The string to find.
        left (int): The starting index of the search range.
        right (int): The ending index of the search range.

    Returns:
        bool: True if the target is found, otherwise False.
    """
    target = target.strip()  # Strip the target for clean comparison
    while left <= right:
        mid = (left + right) // 2
        current_string = arr[mid].strip()  # Strip the current string
        # Debugging output
        print(f"Binary search: left={left}, right={right}, mid={mid}, checking='{current_string}' against '{target}'")
        print(f"Lengths: len(current)={len(current_string)}, len(target)={len(target)}")  # Debugging lengths
        if current_string == target:
            return True
        elif current_string < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


def exponential_search(arr: List[str], target: str) -> bool:
    """
    Perform an exponential search on a sorted array.

    Args:
        arr (List[str]): The sorted array to search.
        target (str): The string to find.

    Returns:
        bool: True if the target is found, otherwise False.
    """
    # Check if the first element is the target
    if arr[0] == target:
        return True
    
    # Find the range for binary search by doubling the index
    index = 1
    while index < len(arr) and arr[index] <= target:
        index *= 2

    # Perform binary search in the found range
    return binary_search(arr, target, index // 2, min(index, len(arr) - 1))

class GraphBasedSearch:
    def __init__(self, file_path: str, file_content: str) -> None:
        """
        Initialize the search instance with the given file path.

        Args:
            file_path (str): The path to the file containing strings to search.
            file_content (str): The content of the file to search in.
        """
        self.file_path = file_path
        self.file_content = file_content

    def load_strings_from_file(self) -> List[str]:
        """
        Load strings from the file and return them as a list.

        Returns:
            List[str]: A list of strings loaded from the file.
        """
        return self.file_content.strip().split('\n')  # Split the content by lines into a list of strings

    def search(self, target_string: str) -> str:
        """
        Search for a target string using exponential search.

        Args:
            target_string (str): The string to search for.

        Returns:
            str: "STRING FOUND" if the target string is found, otherwise "STRING NOT FOUND".
        """
        strings_list = self.load_strings_from_file()
        
        if not strings_list:  # Check if the list is empty
            print("No strings loaded for searching.")
            return "STRING NOT FOUND"

        found = exponential_search(strings_list, target_string)
        return True if found else False
