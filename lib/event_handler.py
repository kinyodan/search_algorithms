import mmap
import pyinotify
import logging
from lib.optimized_file_reader import FileReader
from lib.file_server import FileServer


class EventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        file_reader = FileReader()
        logging.debug(f"DEBUG: {event.pathname} has been modified.")
        logging.debug("DEBUG: pyinotify: Reading the file with mmap")

        # Open the file first to get a file descriptor
        with open(event.pathname, 'r') as f:
            # Use the file descriptor (f.fileno()) for mmap
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                shared_file_content = m.read().decode('utf-8')
                file_server_instance = FileServer()
                file_server_instance.update_file_content(shared_file_content)
                logging.debug("DEBUG: File content updated.")

        return
