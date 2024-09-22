from typing import Tuple, Dict

class HashTableSearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the HashTableSearch instance with the given file path
        and build the hash table for efficient searching.

        Args:
            file_path (str): The path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content = file_content
        self.index: Dict[str, str] = self.build_hash_table()

    def build_hash_table(self) -> Dict[str, str]:
        """
        Build a hash table from the file content for quick lookups.

        Returns:
            Dict[str, str]: A dictionary mapping words to themselves for easy access.
        """
        hash_table = {}
        words = self.file_content.split()
        for word in words:
            hash_table[word.strip()] = word.strip()  # Store the word in the hash table
        return hash_table

    def search(self, target_string: str) -> Tuple[bool, str]:
        """
        Search for a target string in the hash table.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: A tuple indicating if the string was found and the string itself.
        """
        if target_string in self.index:
            return True, self.index[target_string]  # Return True if found
        return False  # Return False if not found
