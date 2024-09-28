from lib.file_reader import FileReader
import logging
import mmap
from lib.file_server import FileServer


class DataPreloader:

    def __init__(self) -> None:
        logging.debug("Running data preloader in DataPreloader")

    def preload_file_data(self, pathname) -> str:
        file_reader = FileReader()
        logging.debug("Reading preloader data the file with mmap")

        # Open the file first to get a file descriptor
        with open(pathname, 'r') as f:
            # Use the file descriptor (f.fileno()) for mmap
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                shared_file_content = m.read().decode('utf-8')
                file_server_instance = FileServer()
                file_server_instance.update_file_content(shared_file_content)
                logging.debug("DEBUG: File content updated.")

        return file_server_instance.get_file_content()
