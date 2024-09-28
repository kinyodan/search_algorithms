import json
from typing import List


def set_metrics_data(
        metric_value: float,
        target_item: str,
        algorithms_list: List[str],
        json_file: str,
        reread_on_query: bool):
    """
    Append the metric_value to the 'execution_times'
    array in the JSON file based on the algorithm's index.

    Args:
        metric_value (float): The metric value to append.
        target_item (str): The name of the algorithm to find.
        algorithms_list (List[str]): List of algorithm names.
        json_file (str): Path to the JSON file.
    """
    # Find the index of the target algorithm in the algorithms_list
    try:
        index = algorithms_list.index(target_item)
    except ValueError:
        print(f"DEBUG: Algorithm '{target_item}' not found in the list.")
        return

    # added to comply with PEP8 standards
    exec_time_string = f"execution_times_REREAD_ON_QUERY_{reread_on_query}"

    try:
        # Load the JSON file
        with open(json_file, 'r+') as f:
            data = json.load(f)

            # Ensure 'execution_times' exists in the JSON
            if f"{exec_time_string}" not in data:
                data[exec_time_string] = []

            # Ensure there are enough sublists in 'execution_times' for index
            while len(
                    data[exec_time_string]) <= index:
                data[exec_time_string].append([
                ])

            # Append the metric value to the corresponding algorithm's list
            data[
                f"{exec_time_string}"][index].append(
                metric_value)

            # Write the updated data back to the JSON file
            f.seek(0)  # Go to the start of the file
            json.dump(data, f, indent=4)
            f.truncate()  # Ensure file is properly truncated after updating

        print(
            f"DEBUG: Metric value {metric_value} added.")
    except Exception as error:
        print(f"DEBUG: problem loading metrics json, or writing to file")
