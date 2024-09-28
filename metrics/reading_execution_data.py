import json
import matplotlib.pyplot as plt
import numpy as np
from server import ALGORITHMS_LIST


def load_execution_times_data():
    # Load execution times from JSON file
    with open('metrics/algorithm_metrics.json', 'r') as f:
        data = json.load(f)

    # List of lists of execution times
    execution_times = data['execution_times']

    # Ensure we have data for each algorithms
    return {
        "algorithms": ALGORITHMS_LIST["algorithms"],
        "execution_times": execution_times}
