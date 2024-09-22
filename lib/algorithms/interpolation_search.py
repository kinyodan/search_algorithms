from typing import List, Tuple, Optional

class InterpolationSearch:
    def __init__(self, file_path: str,file_content: str) -> None:
        """
        Initialize the InterpolationSearch instance with the given file path.

        Args:
            file_path (str): The path to the file containing strings to search.
        """
        self.file_path = file_path
        self.file_content = file_content

    def load_file_content(self) -> List[str]:
        """
        Load and sort the file content.

        Returns:
            List[str]: A list of sorted strings from the file.
        """

        words = sorted(self.file_content.splitlines())  # Sort lines for Interpolation search
        return words

    def search(self, target_string: str) -> Tuple[bool, Optional[str]]:
        """
        Search for a target string using the Interpolation search algorithm.

        Args:
            target_string (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        words = self.load_file_content()  # Load and sort the file content
        return self.interpolation_search(words, target_string)

    def interpolation_search(self, arr: List[str], target: str) -> Tuple[bool, Optional[str]]:
        """
        Perform Interpolation search on a sorted array.

        Args:
            arr (List[str]): The sorted list of strings to search in.
            target (str): The string to search for.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the string was found
            and the string itself, or None if not found.
        """
        low = 0
        high = len(arr) - 1

        while low <= high and arr[low] <= target <= arr[high]:
            if low == high:
                if arr[low] == target:
                    return True, arr[low]
                return False

            # Estimate the position using interpolation formula
            if arr[high] == arr[low]:
                break

            # Calculate the position using string comparison for interpolating position
            pos = low + int((high - low) * (self.estimate_position(arr[low], target) / self.estimate_position(arr[low], arr[high])))

            if pos < low or pos > high:
                break  # Avoid index out of range issues

            if arr[pos] == target:
                return True, arr[pos]
            elif arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1

        return False

    def estimate_position(self, low_str: str, target_str: str) -> int:
        """
        Estimate a comparison value between two strings for interpolation.

        Args:
            low_str (str): The lower bound string.
            target_str (str): The target string to compare.

        Returns:
            int: An estimated numeric value representing the difference between strings.
        """
        # Convert the first part of the string to integer to get a rough estimate for interpolation
        try:
            return int(target_str.split(";")[0]) - int(low_str.split(";")[0])
        except ValueError:
            # Fallback to regular string comparison
            return (target_str > low_str) - (target_str < low_str)
