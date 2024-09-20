from typing import Tuple

class LinearSearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the LinearSearch with the specified file path.

        Args:
            file_path (str): The path to the file containing the text to be searched.
        """
        self.file_path = file_path
        self.file_content = file_content

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Perform a linear search for the target string in the file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple where the first element indicates whether
            the target string was found and the second element is the target string 
            if found, or None if not found.
        """
        words = self.file_content.split()

        # Iterate through the list of words to find the target string
        for word in words:
            if word.strip() == target_string:
                return True, word.strip()  # Return the found word

        return False, None  # Return None if the target string is not found
