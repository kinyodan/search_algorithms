import mmap
import time
from typing import Any, List, Optional, Type
import pandas as pd


class FileReader:
    """
    A class to handle file reading operations.

    This class provides methods to read the content of a file as a string or as a list of lines,
    with support for exception handling, input validation, and the option to re-read the file
    based on the query.
    """

    def __init__(self):
        self.cached_content: str = ""
        self.cached_lines: List[str] = []
        self.caching_done = False

    def read_file(self, file_path: str,args: Optional[Type] = None) -> Any:
        """
        Reads the content of a file based on the reread_on_query flag.

        Args:
            file_path (str): The path to the file to be read.
            reread_on_query (bool): If True, reads the entire file on every query.
                                    If False, reads the file once and caches the content.

        Returns:
            Any: The content of the file as a string (if reread_on_query is True)
                 or a list of lines (if reread_on_query is False).

        Raises:
            FileNotFoundError: If the specified file does not exist.
            IOError: If an I/O error occurs while reading the file.
            ValueError: If the provided file path is invalid.
        """
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("Invalid file path provided. It must be a non-empty string.")

        try:
            chunk_size = 8192 
            start_time = time.time()

            with open(file_path, 'r') as file:
                print("DEBUG: Reading the file in FileReader")
                while chunk := file.read(chunk_size):
                    self.cached_content = chunk
            self.caching_done = True
            elapsed_time = time.time() - start_time
            print(f"Time taken: {elapsed_time * 1000:.2f} ms")
  
            return self.cached_content
            
        except FileNotFoundError:
            raise FileNotFoundError(f"DEBUG: The file '{file_path}' was not found.")
        except IOError as e:
            raise IOError(f"DEBUG: An I/O error occurred while reading the file '{file_path}': {e}")

