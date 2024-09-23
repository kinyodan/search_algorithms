from typing import List, Tuple, Optional

class ShellSearch:
    def __init__(self, file_path: str, file_content: str) -> None:
        """
        Initialize the ShellSearch instance with the given file path and file content.

        Args:
            file_path (str): The path to the file containing strings to search.
            file_content (str): The content to search within (each line as an individual string).
        """
        self.file_path = file_path
        # Each line is treated as an individual string
        self.sorted_lines = file_content.strip().splitlines()

    def search(self, target_string: str) -> Tuple[bool, Optional[str]]:
        """
        Search for a target string in the sorted lines using shell search.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found and the string itself.
        """
        # Strip any trailing/leading whitespace from the target string
        target_string = target_string.strip()

        # Perform ShellSort on the lines
        self.perform_shell_sort()

        # Perform a linear search after sorting
        return self.perform_linear_search(target_string)

    def perform_shell_sort(self) -> None:
        """Helper function to perform ShellSort on the lines."""
        n = len(self.sorted_lines)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = self.sorted_lines[i]
                j = i

                while j >= gap and self.sorted_lines[j - gap] > temp:
                    self.sorted_lines[j] = self.sorted_lines[j - gap]
                    j -= gap

                self.sorted_lines[j] = temp

            gap //= 2

    def perform_linear_search(self, target_string: str) -> Tuple[bool, Optional[str]]:
        """Perform a linear search for the target string after sorting."""
        for line in self.sorted_lines:
            if line.strip() == target_string:
                return True  # Return the found string
        return False
