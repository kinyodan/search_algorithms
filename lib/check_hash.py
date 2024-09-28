
class CheckHash:

    def __init__(self, hash_content):
        self.hash_content = hash_content

    def search(self, target_string):
        if target_string in self.hash_content:
            print("String found! hash map")
            return True
        else:
            return False
