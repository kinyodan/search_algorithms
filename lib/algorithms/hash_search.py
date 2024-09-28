from typing import Tuple, Dict


class HashTableSearch:
    def __init__(self, file_path: str, file_content: str) -> None:
        """
        Initialize the HashTableSearch instance with the given file path
        and build the hash table for efficient searching.

        Args:
            file_path (str): Path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content = file_content[0]
        self.index: Dict[str, str] = self.build_hash_table()

    def build_hash_table(self) -> Dict[str, str]:
        """
        Build a hash table from the file content for quick lookups.

        Returns:
            Dict[str, str]:
            A dictionary mapping words to themselves for easy access.
        """
        hash_table = {}
        words = self.file_content.split()
        for word in words:
            # Sort lines for Interpolation search
            hash_table[word.strip()] = word.strip()
        return hash_table

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Search for a target string in the hash table.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: Tuple indicating if string was found.
        """
        if target_string in self.index:
            return True  # Return True if found
        return False  # Return False if not found
