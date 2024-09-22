import math
from typing import Tuple

class JumpSearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the JumpSearch with the specified file path.

        Args:
            file_path (str): The path to the file containing the text to be searched.
        """
        self.file_path = file_path
        self.file_content = file_content


    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Perform a jump search for the target string in the file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple where the first element indicates whether
            the target string was found and the second element is the target string 
            if found, or None if not found.
        """

        words = sorted(self.file_content.split())
        n = len(words)
        jump = int(math.sqrt(n))
        prev = 0

        # Jump through the sorted list to find the block where the target might be
        while words[min(jump, n) - 1] < target_string:
            prev = jump
            jump += int(math.sqrt(n))
            if prev >= n:
                return False, None
        
        # Perform a linear search within the identified block
        for i in range(prev, min(jump, n)):
            if words[i] == target_string:
                return True, words[i]

        return False
