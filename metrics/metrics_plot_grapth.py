import configparser
import json
import matplotlib.pyplot as plt
import numpy as np
from typing import List


# Algorithms list
algorithms = [
    "linear",
    "binary",
    "hash_table",
    "inverted_index",
    "ternary",
    "graph",
    "jump",
    "trie",
    "fibonacci",
    "exponential",
    "interpolation",
    "quick_select",
    "shell",
    "tim"
]


def load_config(file_path: str) -> str:
    """Load the configuration file and return the metrics JSON path.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        str: The metrics JSON file path.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['settings']['metrics_json_path']

def load_execution_times(json_file_path: str) -> tuple[list[float], list[float]]:
    """Load execution times from the JSON file.

    Args:
        json_file_path (str): Path to the JSON file.

    Returns:
        tuple: Two lists containing execution times for REREAD_ON_QUERY and REREAD_ON_QUERY_False.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return (
        data.get('execution_times_REREAD_ON_QUERY', []),
        data.get('execution_times_REREAD_ON_QUERY_False', [])
    )

def plot_metrics(execution_times: List[list[float]], algorithms: List[str],reread_on_query: bool) -> None:
    """Plot the average execution times for given algorithms.

    Args:
        execution_times (List[list[float]]): List of execution times for algorithms.
        algorithms (List[str]): List of algorithm names.

    Raises:
        ValueError: If execution times data does not match the number of algorithms.
    """
    average_execution_times = [np.mean(times) if times else 0 for times in execution_times]

    if len(average_execution_times) < len(algorithms):
        raise ValueError("Execution times data does not match the number of algorithms.")

    x_positions = np.arange(len(algorithms))
    plt.bar(x_positions, average_execution_times, color='skyblue')

    plt.title('Algorithm Execution Time Comparison')
    plt.xlabel('Algorithms')
    plt.ylabel('Average Execution Time (ms)')
    plt.xticks(x_positions, algorithms, rotation=90)

    plt.tight_layout()
    plt.savefig(f'algorithm_bar_execution_times_REREAD_ON_QUERY_{reread_on_query}.pdf')
    plt.show()

def main() -> None:
    """Main function to execute the script."""
    config_path = 'config.ini'
    json_file_path = load_config(config_path)
    execution_times_REREAD_ON_QUERY, execution_times_REREAD_ON_QUERY_False = load_execution_times(json_file_path)

    # Call the method to plot the metrics data for REREAD_ON_QUERY
    plot_metrics(execution_times_REREAD_ON_QUERY, algorithms, True)
    plot_metrics(execution_times_REREAD_ON_QUERY_False, algorithms, False)

if __name__ == '__main__':
    main()
