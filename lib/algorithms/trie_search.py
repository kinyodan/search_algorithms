from typing import List, Tuple, Optional

class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.is_end_of_word = False

class TrieSearch:
    def __init__(self, file_path: str, file_content: str) -> None:
        """
        Initialize the Trie instance with the given file path and content.

        Args:
            file_path (str): The path to the file containing strings to search.
            file_content (str): The content to be inserted into the Trie.
        """
        self.file_path = file_path
        self.file_content = file_content
        self.root = TrieNode()
        self.build_trie()

    def build_trie(self) -> None:
        """Build the Trie from the provided file content."""
        for word in self.file_content.split():
            self.insert(word.strip())

    def insert(self, word: str) -> None:
        """Insert a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, target_string: str) -> Tuple[bool, Optional[str]]:
        """
        Search for a target string using the Trie.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found and the string itself.
        """
        node = self.root
        for char in target_string:
            if char not in node.children:
                return False
            node = node.children[char]
        return True if node.is_end_of_word else False
