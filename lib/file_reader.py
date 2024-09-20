from typing import Any

class FileReader:
    """
    A class to handle file reading operations.

    This class provides methods to read the content of a file as a string or as a list of lines,
    with support for exception handling and input validation.
    """

    def read_file(self, file_path: str, reread_on_query: bool) -> Any:
        """
        Reads the content of a file based on the reread_on_query flag.

        Args:
            file_path (str): The path to the file to be read.
            reread_on_query (bool): If True, reads the entire file as a string.
                                    If False, reads the file line by line.

        Returns:
            Any: The content of the file as a string or a list of lines.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            IOError: If an I/O error occurs while reading the file.
            ValueError: If the provided file path is invalid.
        """
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("Invalid file path provided. It must be a non-empty string.")

        try:
            if reread_on_query:
                with open(file_path, 'r') as file:
                    return file.read()
            else:
                with open(file_path, 'r') as file:
                    return file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"DEBUG: The file '{file_path}' was not found.")
        except IOError as e:
            raise IOError(f"DEBUG: An I/O error occurred while reading the file '{file_path}': {e}")

# Example usage:
# file_reader = FileReader()
# content = file_reader.read_file('example.txt', True)
