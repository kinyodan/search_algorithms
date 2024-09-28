from typing import Tuple


class LinearSearch:
    def __init__(self, file_path: str, file_content: str) -> None:
        """
        Initialize the LinearSearch with the specified file path.

        Args:
            file_path (str): path to the file containing text to be searched.
        """
        self.file_path = file_path
        self.file_content = file_content[0]

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Perform a linear search for the target string in the file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple where the first element indicates whether
            target string was found and the second element is the target string
            if found, or None if not found.
        """
        words = self.file_content.split()

        # Iterate through the list of words to find the target string
        for word in words:
            if word.strip() == target_string:
                # Return true if found
                return True
        # Return False if the target string is not found
        return False
