from typing import List, Tuple

class QuickSelectSearch:
    """
    Class that implements Quick Select Search algorithm.
    
    The algorithm works by selecting a pivot and partitioning the list 
    such that all elements on one side of the pivot are less than or equal 
    to the pivot, and all elements on the other side are greater. The search 
    continues on the partition containing the target string.
    
    Attributes:
        file_path (str): Path to the file.
        file_content (str): Content of the file to search in.
    """

    def __init__(self, file_path: str, file_content: str):
        """
        Initialize the search object with the given file path and content.

        Args:
            file_path (str): Path to the file.
            file_content (str): Content of the file.
        """
        self.file_path = file_path
        self.file_content = file_content

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Search for a target string using the Quick Select Search algorithm.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple containing whether the string was found 
                              and the string itself if found.
        """
        # Split file content and sort
        words = sorted(self.file_content.split())
        return self.quick_select_search(words, target_string)

    def partition(self, arr: List[str], low: int, high: int) -> int:
        """
        Partition the array around a pivot.

        Args:
            arr (List[str]): The array to partition.
            low (int): Starting index.
            high (int): Ending index.

        Returns:
            int: The index of the pivot.
        """
        pivot = arr[high]  # Select the pivot as the last element
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_select_search(self, arr: List[str], target_string: str) -> Tuple[bool, str]:
        """
        Perform Quick Select search to find the target string.

        Args:
            arr (List[str]): The array of strings.
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple containing whether the string was found 
                              and the string itself if found.
        """
        left, right = 0, len(arr) - 1
        
        while left <= right:
            # Partition the array and get pivot index
            pivot_index = self.partition(arr, left, right)
            
            if arr[pivot_index] == target_string:
                return True, arr[pivot_index]
            elif arr[pivot_index] < target_string:
                left = pivot_index + 1
            else:
                right = pivot_index - 1
        
        return False, None
