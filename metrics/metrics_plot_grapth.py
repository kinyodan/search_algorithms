import configparser
import json
import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from matplotlib.ticker import LogLocator, FuncFormatter

# Algorithms list
algorithms = [
    "default",
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, file_path)

    config = configparser.ConfigParser()
    config.read(config_file)
    metrics_path = config['settings']['metrics_plotting_path']

    # Construct an absolute path to the metrics file
    json_file_path = os.path.join(script_dir, metrics_path)

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(
            f"The metrics file was not found at {json_file_path}")

    return json_file_path


def load_execution_times(
        json_file_path: str) -> tuple[list[float], list[float]]:
    """Load execution times from the JSON file.

    Args:
        json_file_path (str): Path to the JSON file.

    Returns:
        tuple: Two lists containing execution times
        for REREAD_ON_QUERY and REREAD_ON_QUERY_False.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return (
        data.get('execution_times_REREAD_ON_QUERY', []),
        data.get('execution_times_REREAD_ON_QUERY_False', [])
    )


def plot_metrics(execution_times: List[list[float]],
                 algorithms: List[str],
                 reread_on_query: bool) -> None:
    """Plot the average execution times for given algorithms.

    Args:
        execution_times (List[list[float]]):
        List of execution times for algorithms.
        algorithms (List[str]): List of algorithm names.

    Raises:
        ValueError: If execution times data
        does not match the number of algorithms.
    """
    average_execution_times = [
        np.mean(times) if times else 0 for times in execution_times]

    if len(average_execution_times) < len(algorithms):
        raise ValueError(
            "Execution times data does not match the number of algorithms.")

    x_positions = np.arange(len(algorithms))
    bars = plt.bar(x_positions, average_execution_times, color='skyblue')

    plt.title(f'Execution Times REREAD_ON_QUERY ({reread_on_query})')
    plt.xlabel('Algorithms')
    plt.ylabel('Average Execution Time (ms)')
    plt.xticks(x_positions, algorithms, rotation=90)

    # Set y-axis to a logarithmic scale
    plt.yscale('log')

    # Set y-axis limits if needed (optional)
    # Adjust the lower limit to accommodate very small values
    plt.ylim(bottom=1e-3)

    # Adjust the y-axis tick frequency (optional)
    plt.gca().yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))

    # Format y-axis to display values as regular numbers
    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: '{:.3f}'.format(y)))

    # Annotate bars with the average execution times
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval / 2, f'{yval:.1f}',
                 ha='center', va='center', color='black', fontsize=8)

    plt.tight_layout()
    plt.savefig(
        f'algorithm_bar_execution_times_REREAD_ON_QUERY_{reread_on_query}.pdf')
    plt.show()


def main() -> None:
    """Main function to execute the script."""
    config_path = '../config.ini'
    json_file_path = load_config(config_path)
    exec_REREAD_ON_QUERY, exec_REREAD_ON_QUERY_False = load_execution_times(
        json_file_path)

    # Call the method to plot the metrics data for REREAD_ON_QUERY
    plot_metrics(exec_REREAD_ON_QUERY_False, algorithms, True)
    plot_metrics(exec_REREAD_ON_QUERY_False, algorithms, False)


if __name__ == '__main__':
    main()
