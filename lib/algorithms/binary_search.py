from typing import List, Tuple

class BinarySearch:
    def __init__(self, file_path: str,file_content: str):
        """
        Initialize the BinarySearch instance with the given file path.

        Args:
            file_path (str): The path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content = file_content

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Search for a target string using binary search on the content of the file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple indicating if the string was found and the string itself.
        """
        print("DEBUGGING TEST SUITES BINARY SEARCH")
        words = sorted(self.file_content.split())  # Sort the content as a list
            
        # Perform binary search on the sorted list
        return self.perform_iterative_search(words, target_string)

    def perform_iterative_search(self, content: List[str], query: str) -> Tuple[bool, str]:
        """
        Perform an iterative binary search on the provided content.

        Args:
            content (List[str]): The sorted list of strings to search.
            query (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple indicating if the string was found and the string itself.
        """
        # Strip any extra spaces from the query
        query_clean = query.strip()
        
        # Define initial search boundaries
        left, right = 0, len(content) - 1

        while left <= right:
            mid = (left + right) // 2
            current_item = content[mid].strip()

            if current_item == query_clean:
                return True, current_item

            elif current_item < query_clean:
                left = mid + 1

            else:
                right = mid - 1

        # If we exit the loop, the item was not found
        return False
