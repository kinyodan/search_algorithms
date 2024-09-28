
import logging


class HashSearch:

    def __init__(self, file_content):
        self.hash_content = file_content[1]

    def search(self, target_string):
        if target_string in self.hash_content:
            logging.debug("String found! in Hash map")
            return True
        else:
            return False
