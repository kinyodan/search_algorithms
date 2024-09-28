
import io
import logging
import mmap
import time
from typing import Any, List, Optional, Type
import concurrent.futures

import numpy as np

from lib.file_server import FileServer


class FileReader:
    '''
    A class to handle file reading operations with mmap for efficient reading.
    '''

    def __init__(self):
        self.cached_content: str = ""
        self.cached_lines: List[str] = []
        self.caching_done = False

    def hashing_data(self, content_data):
        hash_map = {}
        for line in content_data.split('\n'):
            hash_map[line.strip()] = True

        return hash_map

    def read_file(self, file_path: str, args: Optional[Type] = None) -> Any:
        '''
        Reads the content of a file efficiently using mmap for large files.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The entire content of the file as a string.
        '''
        try:
            start_time = time.time()
            hash_map = {}

            with open(file_path, 'r+', encoding='utf-8') as file:
                logging.debug("DEBUG: Reading the file with mmap")
                with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as m:
                    self.cached_content = m.read().decode('utf-8')
                    # Update the FileServer with new read file data
                    file_server = FileServer()
                    file_server.update_file_content(self.cached_content)
                    is_updated = file_server.is_file_server_updated
                    logging.debug("Data updated to FileServer at FileReader")
                    logging.debug(
                        f"is_file_server_updated?: {is_updated}")

                    # Add data into a hash map
                    hash_map = self.hashing_data(self.cached_content)
                    self.cached_lines = self.cached_content
                    logging.debug("Data added to Hash map at FileReader")

            self.caching_done = True
            elapsed_time = time.time() - start_time
            logging.debug(
                f"Time taken to read and cache: {elapsed_time * 1000:.2f} ms")

            return self.cached_content, hash_map

        except FileNotFoundError:
            raise FileNotFoundError(
                f"DEBUG: The file '{file_path}' was not found.")
        except IOError as e:
            raise IOError(
                f"An I/O error occurred while reading file '{file_path}': {e}")

    def read_data(self, content_data: Optional[Type] = None) -> Any:
        '''
        Reads the content of a file efficiently .

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The entire content of the file as a string.
        '''

        try:
            start_time = time.time()
            hash_map = {}

            logging.debug("Reading FileServer content at FileReader")
            # Get the preloaded or updated file contents from
            # the FileServer.
            file_server = FileServer()

            # Add data into a hash map
            self.cached_content = file_server._shared_file_content
            hash_map = file_server._shared_hash_map
            self.cached_lines = self.cached_content

            self.caching_done = True
            elapsed_time = time.time() - start_time
            logging.debug(f"Time taken to read : {elapsed_time * 1000:.2f} ms")

            return self.cached_content, hash_map

        except ValueError:
            raise ValueError(f"Problem accessing global shared data.")
