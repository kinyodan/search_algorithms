from collections import deque

class BreadthFirstSearch:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()

    def search(self, start, target):
        queue = deque([start])
        self.visited.add(start)

        while queue:
            node = queue.popleft()

            # Check if we've found the target
            if node == target:
                return True

            # Add neighbors to the queue
            for neighbor in self.graph.get(node, []):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append(neighbor)
                    
        return False

class AnchorBreadthGraphBasedSearch:
    def __init__(self, file_path, file_content: str) -> None:
        self.file_path = file_path
        self.file_content = file_content

    def load_graph_from_file(self):
        graph = {}
        unique_strings = []

        for line in self.file_content.splitlines():  # Ensure we split the file content by lines
            line = line.strip()  # Strip any whitespace/newlines
            if line:  # Only process non-empty lines
                unique_strings.append(line)  # Add each line to unique_strings
                graph[line] = []  # Initialize an empty list for neighbors (or relationships)
                    
        return graph, unique_strings

    def breadth_first_search(self, target):
        graph, unique_strings = self.load_graph_from_file()

        if not unique_strings:
            raise ValueError("DEBUG: The file does not contain any nodes.")
        
        start_node = unique_strings[0]  # Set start_node to the first node in the file

        # Ensure target string is properly stripped, just like the file content
        target = target.strip()

        search_instance = BreadthFirstSearch(graph)
        return search_instance.search(start_node, target)


#