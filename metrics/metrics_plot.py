import configparser
import json
import matplotlib.pyplot as plt
import numpy as np

# Load the configuration file
try:
    config = configparser.ConfigParser()
    config.read('config.ini')

    json_file_path = config['settings']['metrics_json_path']
except Exception as e:
    raise ValueError("Error getting data from config.ini: " + str(e))

# Load the JSON data
try:
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Extract execution_times and algorithms
    execution_times = data.get('execution_times_REREAD_ON_QUERY_False', [])
    algorithms = data.get('algorithms', [])
except Exception as e:
    raise ValueError("Error getting plot data from the JSON file: " + str(e))

# Calculate the average execution time per algorithm, ignoring the first index
average_execution_times = [
    np.mean(times[1:]) if len(times) > 1 else 0 for times in execution_times
]

# Match the lengths by filling in zeros for missing algorithms
while len(average_execution_times) < len(algorithms):
    average_execution_times.append(0)  # or handle it as needed

# Define positions for the bars on the x-axis
x_positions = np.arange(len(algorithms))

# Plot a simple bar chart
plt.bar(x_positions, average_execution_times, color='skyblue')

# Adding labels and titles
plt.title('Algorithm Execution Time Comparison')
plt.xlabel('Algorithms')
plt.ylabel('Average Execution Time (ms)')
# Add algorithm names as x-tick labels
plt.xticks(x_positions, algorithms, rotation=90)

# Save as PDF
plt.tight_layout()  # To avoid label overlap
plt.savefig('execution_times_REREAD_ON_QUERY_False.pdf')

# Show the plot
plt.show()
