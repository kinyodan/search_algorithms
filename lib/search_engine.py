import os
from typing import Tuple, Any
from lib.algorithms.binary_search import BinarySearch
from lib.algorithms.exponential_search import ExponentialSearch
from lib.algorithms.fibonacci_search import FibonacciSearch
from lib.algorithms.graph_search import GraphBasedSearch
from lib.algorithms.hash_search import HashTableSearch
from lib.algorithms.interpolation_search import InterpolationSearch
from lib.algorithms.inverted_index_search import InvertedIndexSearch
from lib.algorithms.jump_search import JumpSearch
from lib.algorithms.linear_search import LinearSearch
from lib.algorithms.shell_search import ShellSearch
from lib.algorithms.ternary_search import TernarySearch
from lib.file_reader import FileReader
from lib.tim_search import TimSortSearch
from lib.algorithms.trie_search import TrieSearch

class SearchEngine:
    """
    A class that encapsulates various search algorithms for locating a target string
    in specified files or data structures.
    """

    _class_cache = {}

    def __init__(self, reread_on_query: str,file_path: str):
        self.reread_on_query = reread_on_query
        self.file_path = file_path

    def load_file_content(self) -> str:
        try:
            file_reader = FileReader()
            if self.reread_on_query:
                print("DEBUG: Rereading file content")
                return file_reader.read_file(self.file_path)
            else:
                if self.file_path not in SearchEngine._class_cache:
                    print("DEBUG: Caching file content")
                    SearchEngine._class_cache[self.file_path] = file_reader.read_file(self.file_path, self.reread_on_query)
                else:
                    print("DEBUG: Returning cached content")
                return SearchEngine._class_cache[self.file_path]
        except Exception as e:
            message = f"Error with FileReader problem loading file content:: {e}"
            print(message)
            raise ValueError(message)


    def binary_search(self, target_string: str) -> Tuple[bool, str]:
        """Executes the BinarySearch algorithm to find a target string in the specified file."""
        search_instance = BinarySearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def inverted_index_search(self, target_string: str) -> Tuple[bool, str]:
        """Executes the InvertedIndexSearch algorithm to locate a target string in the specified file."""
        search_instance = InvertedIndexSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def linear_search(self, target_string: str) -> Tuple[bool, str]:
        """Executes the LinearSearch algorithm to find a target string in the specified file."""
        search_instance = LinearSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def jump_search(self, target_string: str) -> Tuple[bool, str]:
        """Executes the JumpSearch algorithm to locate a target string in the specified file."""
        search_instance = JumpSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def ternary_search(self, target_string: str) -> Tuple[bool, str]:
        """Executes the TernarySearch algorithm to find a target string in the specified file."""
        search_instance = TernarySearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def hash_table_search(self, target_string: str) -> Tuple[bool, str]:
        """Executes the HashTableSearch algorithm to locate a target string in the specified file."""
        search_instance = HashTableSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def graph_search(self, target_string: str) -> bool:
        """Executes the GraphBasedSearch algorithm to find a target in a graph starting from a given node."""
        search_instance = GraphBasedSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def exponential_search(self, target_string: str) -> bool:
        """Executes the ExponentialSearch algorithm to find a target in a sorted array."""
        search_instance = ExponentialSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def interpolation_search(self,target_string: str) -> bool:
        """Executes the InterpolationSearch algorithm to find a target in a sorted array."""
        search_instance = InterpolationSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def fibonacci_search(self, target_string: str) -> bool:
        """Executes the FibonacciSearch algorithm to find a target in a sorted array."""
        search_instance = FibonacciSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def tim_search(self, target_string: str) -> bool:
        """Executes the QuickSelectSearch algorithm to find a target in a large string file."""
        search_instance = TimSortSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)

    def trie_search(self, target_string: str) -> bool:
        """Executes the TrieSearch  algorithm to find a target in a large string file."""
        search_instance = TrieSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)
    
    def shell_search(self, target_string: str) -> bool:
        """Executes the ShellSearch  algorithm to find a target in a large string file."""
        search_instance = ShellSearch(self.file_path,self.load_file_content())
        return search_instance.search(target_string)
    
def search_alg_setup(algorithm: str, reread_on_query: bool, file_path: str, target_string: str) -> Tuple[bool, str]:
    """
    Sets up the specified search algorithm and executes it to find the target string in the file.

    Args:
        algorithm (str): The name of the search algorithm to use.
        file_path (str): The path to the file to search.
        target_string (str): The string to search for.

    Returns:
        Tuple[bool, str]: The result of the search, including whether the target was found
        and the found string (if applicable).
    """
    print(f"DEBUG: Setting up '{algorithm}' algorithm to search for '{target_string}'")
    algorithm_name = f"{algorithm}_search"
    search_engine = SearchEngine(reread_on_query,file_path)
    search_method = getattr(search_engine, algorithm_name)

    return search_method(target_string)
