from typing import List, Tuple, Optional

class FibonacciSearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the FibonacciSearch instance with the given file path.

        Args:
            file_path (str): The path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content =  file_content

    def load_file_content(self) -> List[str]:
        """
        Load and sort the file content.

        Returns:
            List[str]: A list of sorted strings from the file.
        """
  
        words = sorted(self.file_content.splitlines())  # Sort lines for Fibonacci search
        return words

    def search(self, target_string: str) -> Tuple[bool, Optional[str]]:
        """
        Search for a target string using the Fibonacci search algorithm.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        words = self.load_file_content()  # Load and sort the file content
        return self.fibonacci_search(words, target_string)

    def fibonacci_search(self, arr: List[str], target: str) -> Tuple[bool, Optional[str]]:
        """
        Perform Fibonacci search on a sorted array.

        Args:
            arr (List[str]): The sorted list of strings to search in.
            target (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        fib_m2 = 0  # (m-2)'th Fibonacci number
        fib_m1 = 1  # (m-1)'th Fibonacci number
        fib_m = fib_m2 + fib_m1  # m'th Fibonacci number

        n = len(arr)

        # Find the smallest Fibonacci number greater than or equal to n
        while fib_m < n:
            fib_m2, fib_m1 = fib_m1, fib_m
            fib_m = fib_m2 + fib_m1

        offset = -1

        # Perform the search
        while fib_m > 1:
            i = min(offset + fib_m2, n - 1)

            if arr[i] < target:
                fib_m = fib_m1
                fib_m1 = fib_m2
                fib_m2 = fib_m - fib_m1
                offset = i
            elif arr[i] > target:
                fib_m = fib_m2
                fib_m1 -= fib_m2
                fib_m2 = fib_m - fib_m1
            else:
                return True, arr[i]  # Target found

        # Check the last remaining element
        if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
            return True, arr[offset + 1]

        return False  # Target not found
