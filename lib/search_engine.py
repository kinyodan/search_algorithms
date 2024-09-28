import os
import logging
from typing import Dict, Optional, Tuple, Any, Union
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
from lib.file_server import FileServer
from lib.hash_map_search import HashSearch
from lib.optimized_file_reader import FileReader
from lib.tim_search import TimSortSearch
from lib.algorithms.trie_search import TrieSearch

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class SearchEngine:
    """
    A class that encapsulates various search algorithms for locating
    a target string in specified files or data structures.
    """

    _class_cache = {}

    def __init__(
            self,
            reread_on_query: str,
            file_path: str,
            shared_file_content: str):
        """
        Initializes the SearchEngine instance.

        Args:
            reread_on_query (str): A flag to check whether to re-read the file.
            file_path (str): Path to the file to be searched.
        """
        self.reread_on_query = reread_on_query
        self.file_path = file_path
        self.shared_file_content = shared_file_content

    def load_file_content(self) -> str:
        """
        Loads the file content, either from cache or by reading it again.

        Returns:
            str: The content of the file.

        Raises:
            ValueError: If error occurs when loading file content.
        """
        try:
            file_data = None
            file_reader = FileReader()
            file_server = FileServer()
            file_server_updated = file_server.is_file_server_updated()

            if not file_server_updated:
                file_data = file_reader.read_file(
                    self.file_path, self.reread_on_query)
            else:
                file_data = file_reader.read_data(
                    self.shared_file_content)

            if self.reread_on_query:
                logging.debug("Rereading file content")
                return file_data
            else:
                if self.file_path not in SearchEngine._class_cache:
                    logging.debug("Caching file content")
                    self._class_cache[self.file_path] = (
                        file_server._shared_file_content
                    )

                    self._class_cache["hash_map"] = (
                        file_server._shared_hash_map
                    )
                    return (self._class_cache[self.file_path],
                            self._class_cache["hash_map"])
                else:
                    logging.debug("Returning cached content")
                    return (self._class_cache[self.file_path],
                            self._class_cache["hash_map"])

        except Exception as e:
            message = f"Error in FileReader problem loading file content: {e}"
            logging.debug(message)
            raise ValueError(message)

    def default_search(self, target_string: str) -> Tuple[bool, str]:
        search_instance = HashSearch(self.load_file_content())
        return search_instance.search(target_string)

    def binary_search(self, target_string: str) -> Tuple[bool, str]:
        """
        Runs the BinarySearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: Search result as a tuple of success & result.
        """
        search_instance = BinarySearch(
            self.file_path, self.load_file_content())
        return search_instance.search(target_string)

    def inverted_index_search(self, target_string: str) -> Tuple[bool, str]:
        """
        Runs InvertedIndexSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: Search result as a tuple of success & result.
        """
        search_instance = InvertedIndexSearch(self.file_path,
                                              self.load_file_content())
        return search_instance.search(target_string)

    def linear_search(self, target_string: str) -> Tuple[bool, str]:
        """
        Runs the LinearSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: Search result as a tuple of success & result.
        """
        search_instance = LinearSearch(
            self.file_path, self.load_file_content())
        return search_instance.search(target_string)

    def jump_search(self, target_string: str) -> Tuple[bool, str]:
        """
        Runs the JumpSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: Search result as a tuple of success & result.
        """
        search_instance = JumpSearch(self.file_path, self.load_file_content())
        return search_instance.search(target_string)

    def ternary_search(self, target_string: str) -> Tuple[bool, str]:
        """
        Runs the TernarySearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: Search result as a tuple of success & result.
        """
        search_instance = TernarySearch(
            self.file_path, self.load_file_content())
        return search_instance.search(target_string)

    def hash_table_search(self, target_string: str) -> Tuple[bool, str]:
        """
        Runs the HashTableSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, str]: Search result as a tuple of success & result.
        """
        search_instance = HashTableSearch(self.file_path,
                                          self.load_file_content())
        return search_instance.search(target_string)

    def graph_search(self, target_string: str) -> bool:
        """
        Runs GraphBasedSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: Search result as a success flag.
        """
        search_instance = GraphBasedSearch(self.file_path,
                                           self.load_file_content())
        return search_instance.search(target_string)

    def exponential_search(self, target_string: str) -> bool:
        """
        Runs ExponentialSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: Search result as a success flag.
        """
        search_instance = ExponentialSearch(self.file_path,
                                            self.load_file_content())
        return search_instance.search(target_string)

    def interpolation_search(self, target_string: str) -> bool:
        """
        Runs InterpolationSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: Search result as a success flag.
        """
        search_instance = InterpolationSearch(self.file_path,
                                              self.load_file_content())
        return search_instance.search(target_string)

    def fibonacci_search(self, target_string: str) -> bool:
        """
        Runs the FibonacciSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: Search result as a success flag.
        """
        search_instance = FibonacciSearch(
            self.file_path, self.load_file_content())
        return search_instance.search(target_string)

    def tim_search(self, target_string: str) -> bool:
        """
        Runs the TimSortSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: Search result as a success flag.
        """
        search_instance = TimSortSearch(
            self.file_path, self.load_file_content())
        return search_instance.search(target_string)

    def trie_search(self, target_string: str) -> bool:
        """
        Runs the TrieSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: Search result as a success flag.
        """
        search_instance = TrieSearch(self.file_path, self.load_file_content())
        return search_instance.search(target_string)

    def shell_search(self, target_string: str) -> bool:
        """
        Runs the ShellSearch algorithm to locate a target in a string file.

        Args:
            target_string (str): The string to search for.

        Returns:
            bool: Search result as a success flag.
        """
        search_instance = ShellSearch(self.file_path, self.load_file_content())
        return search_instance.search(target_string)


def search_alg_setup(
    algorithm: str,
    reread_on_query: bool,
    file_path: str,
    target_string: str,
    shared_file_content: Optional[Union[str, bytes]] = None
) -> Tuple[bool, str]:
    """
    Sets up the search algorithm and runs it to locate the target string.

    Args:
        algorithm (str): The name of the search algorithm to use.
        reread_on_query (bool): Whether to re-read the file on each query.
        file_path (str): The path to the file to search.
        target_string (str): The string to search for.

    Returns:
        Tuple[bool, str]: The result of the search, and if the target was found
        and the found string (if applicable).
    """
    # try:
    logging.debug(
        f"Using '{algorithm}' algorithm to find '{target_string}'")
    algorithm_name = f"{algorithm}_search"
    search_engine = SearchEngine(
        reread_on_query,
        file_path,
        shared_file_content)
    search_method = getattr(search_engine, algorithm_name)
    return search_method(target_string)
    # except Exception as error:
    #     logging.debug(f"Error in SearchEngine Search_alg_setup: {error} ")
    #     raise
