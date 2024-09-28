import logging
import threading


class FileServer:

    _shared_file_content = ""
    _server_updated = False
    _shared_hash_map = {}

    def __init__(self):
        self.lock = threading.Lock()

    def hashing_data(self):
        for line in self._shared_file_content.split('\n'):
            FileServer._shared_hash_map[line.strip()] = True

    def update_file_content(self, content: str):
        with self.lock:
            FileServer._shared_file_content = content
            FileServer._server_updated = True
            self.hashing_data()
        logging.debug(f"updating FileServer at FileServer ")

    def get_file_content(self):
        with self.lock:
            cont_len = len(self._shared_file_content)
            logging.debug(F"The current file content ln is {cont_len}")
            return self._shared_hash_map

    def is_file_server_updated(self) -> bool:
        logging.debug(
            f"is_file_server_updated?: {FileServer._server_updated} ")
        return FileServer._shared_file_content
