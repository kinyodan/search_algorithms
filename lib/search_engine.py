import os
from typing import Tuple, Any
from lib.binary_search import BinarySearch
# from lib.breadth_first_search import AnchorBreadthGraphBasedSearch
# from lib.depth_first_search import DepthFirstSearch
from lib.exponential_search import ExponentialSearch
from lib.fibonacci_search import FibonacciSearch
from lib.graph_search import GraphBasedSearch
from lib.hash_search import HashTableSearch
from lib.interpolation_search import InterpolationSearch
from lib.inverted_index_search import InvertedIndexSearch
from lib.jump_search import JumpSearch
from lib.linear_search import LinearSearch
from lib.quick_select import QuickSelectSearch
from lib.ternary_search import TernarySearch
from lib.file_reader import FileReader
from lib.tim_search import TimSortSearch

class SearchEngine:
    """
    A class that encapsulates various search algorithms for locating a target string
    in specified files or data structures.
    """
    def __init__(self, reread_on_query: str,file_path: str):
        self.reread_on_query = reread_on_query
        self.file_path = file_path

    def load_file_content(self) -> str:
        """
        Loads the file content based on the reread_on_query setting.

        Returns:
            str: The content of the file as a string.
        """
        file_reader = FileReader()
        return file_reader.read_file(self.file_path, self.reread_on_query)

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

    # def breadth_first_search(self, target_string: str) -> bool:
    #     """Executes the BreadthFirstSearch algorithm to find a target in a graph."""
    #     search_instance = AnchorBreadthGraphBasedSearch(self.file_path,self.load_file_content())
    #     return search_instance.breadth_first_search(target_string)

    # def depth_first_search(self, target_string: str) -> bool:
    #     """Executes the BreadthFirstSearch algorithm to find a target in a graph."""
    #     search_instance = DepthFirstSearch(self.file_path,self.load_file_content())
    #     return search_instance.dfs(target_string)

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

    def quick_select_search(self, target_string: str) -> bool:
        """Executes the QuickSelectSearch algorithm to find a target in a sorted array."""
        search_instance = QuickSelectSearch(self.file_path,self.load_file_content())
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
