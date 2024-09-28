from collections import defaultdict
from typing import Dict, List, Optional


class InvertedIndexSearch:
    def __init__(self, file_path: str, file_content: str) -> None:
        """
        Initialize the InvertedIndexSearch with the given file path.

        Args:
            file_path (str): Path to file containing the text to be indexed.
        """
        self.file_path = file_path
        self.file_content = file_content[0]

    def build_inverted_index(self) -> Optional[Dict[str, List[int]]]:
        """
        Build an inverted index from the file at the specified path.

        Returns:
            Optional[Dict[str, List[int]]]:
            A dictionary mapping words to their indices in the file.
            Returns None if an error occurs during processing.
        """
        try:
            # Split the content into words and create an index
            index = defaultdict(list)
            words = self.file_content.split()
            for i, word in enumerate(words):
                index[word].append(i)
            return index

        except Exception as error:
            print(f"DEBUG: Error processing query raised error - {error}")
            return False

    def search(self, target_string: str) -> bool:
        """
        Search for the target string in the inverted index.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: True if the target string is found in the index, else False.
        """
        inverted_index = self.build_inverted_index()
        if inverted_index is not None:
            return target_string in inverted_index
        return False
