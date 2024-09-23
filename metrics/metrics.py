

import json
from typing import List

def set_metrics_data(metric_value: float, target_item: str, algorithms_list: List[str], json_file: str,reread_on_query: bool ):
    """
    Append the metric_value to the 'execution_times' array in the JSON file based on the algorithm's index.

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

    # Load the JSON file
    with open(json_file, 'r+') as f:
        data = json.load(f)

        # Ensure 'execution_times' exists in the JSON
        if f"execution_times_REREAD_ON_QUERY_{reread_on_query}" not in data:
            data[f"execution_times_REREAD_ON_QUERY_{reread_on_query}"] = []

        # Ensure there are enough sublists in 'execution_times' for the index
        while len(data[f"execution_times_REREAD_ON_QUERY_{reread_on_query}"]) <= index:
            data[f"execution_times_REREAD_ON_QUERY_{reread_on_query}"].append([])

        # Append the metric value to the corresponding algorithm's list
        data[f"execution_times_REREAD_ON_QUERY_{reread_on_query}"][index].append(metric_value)

        # Write the updated data back to the JSON file
        f.seek(0)  # Go to the start of the file
        json.dump(data, f, indent=4)
        f.truncate()  # Ensure the file is properly truncated after updating

    print(f"DEBUG: Metric value {metric_value} added to 'execution_times_REREAD_ON_QUERY_{reread_on_query}' for algorithm '{target_item}' at index {index}.")
