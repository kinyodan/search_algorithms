
class DepthFirstSearch:
    def __init__(self, file_path,file_content: str) -> None:
        self.file_path = file_path
        self.visited = set()
        self.file_content = file_content

    # Load the strings from the file
    def load_strings_from_file(self):
        strings = []
        for line in self.file_content:
            strings.append(line.strip())  # Read and strip any extra whitespace/newlines
        return strings

    # Depth-First Search
    def dfs(self, target_string):
        strings = self.load_strings_from_file()

        # Internal DFS function
        def search(index):
            if index >= len(strings):  # Check if index is within the bounds
                return False
            current_string = strings[index]
            
            if current_string == target_string:
                return True
            
            # Mark the string as visited
            self.visited.add(current_string)

            # Move to the next neighbor (next string in the list)
            if index + 1 < len(strings) and strings[index + 1] not in self.visited:
                if search(index + 1):
                    return True
            
            return False

        # Start DFS from the first string
        return search(0)

