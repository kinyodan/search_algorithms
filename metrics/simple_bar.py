import matplotlib.pyplot as plt
from reading_execution_data import load_execution_times_data

data = load_execution_times_data()

execution_times = data["execution_times"
                       ]
# Calculate average execution time for each algorithm
average_times = [np.mean(times) for times in execution_times]

# Create bar graph
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.4
index = np.arange(len(algorithms))

ax.bar(index, average_times, bar_width, label='Average Execution Time (ms)')
ax.set_xlabel('Algorithms')
ax.set_ylabel('Execution Time (ms)')
ax.set_title('Algorithm Performance Comparison (Average Execution Time)')
ax.set_xticks(index)
ax.set_xticklabels(algorithms, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.savefig('algorithm_performance_comparison_avg.pdf')
plt.show()
