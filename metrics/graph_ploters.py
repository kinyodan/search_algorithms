
import socket
import json
import time
import concurrent.futures
import os
import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd


def plotting_data(json_file):
    # Load existing performance data if the file exists
    if os.path.exists(json_file):
        performance_data ={} 

        with open(json_file, 'r') as f:
            performance_data = json.load(f)
        return performance_data

# def plot_heatmap(performance_data):
#     """Plot a heatmap of execution times."""
#     df = pd.DataFrame(performance_data).T
#     df.columns = [str(q) for q in df.columns]  # Convert keys to strings for plotting

#     plt.figure(figsize=(10, 6))
#     sns.heatmap(df, annot=True, fmt=".1f", cmap='viridis', cbar_kws={'label': 'Avg Execution Time (ms)'})

#     plt.xlabel('Number of Queries')
#     plt.ylabel('File Size')
#     plt.title('Execution Time Heatmap')
#     plt.savefig(f'heatmap_report_{time.strftime("%Y-%m-%d_%H-%M-%S")}.pdf')
#     plt.show()

def plot_scatter_chart(performance_data):
    """Plot a scatter chart of performance data."""
    for file_size, query_data in performance_data.items():
        num_queries = list(query_data.keys())
        exec_times = [query_data[q] for q in num_queries]
        
        plt.scatter(num_queries, exec_times, label=f'File Size {file_size}', alpha=0.6)

    plt.xlabel('Number of Queries')
    plt.ylabel('Avg Execution Time (ms)')
    plt.title('Execution Time vs Number of Queries')
    plt.legend()
    plt.grid(True)

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'scatter_chart_report_{current_time}.pdf')
    plt.show()


def plot_bar_chart(performance_data):
    """Plot a bar chart of performance data."""
    num_queries = []
    execution_times = {key: [] for key in performance_data.keys()}

    for file_size, query_data in performance_data.items():
        for query_count, exec_time in query_data.items():
            if query_count not in num_queries:
                num_queries.append(query_count)
            execution_times[file_size].append(exec_time)

    bar_width = 0.15
    x_indices = range(len(num_queries))

    for i, (file_size, times) in enumerate(execution_times.items()):
        plt.bar([x + bar_width * i for x in x_indices], times, width=bar_width, label=f'File Size {file_size}')

    plt.xlabel('Number of Queries')
    plt.ylabel('Avg Execution Time (ms)')
    plt.title('Execution Time vs Number of Queries')
    plt.xticks([x + bar_width for x in x_indices], num_queries)
    plt.legend()
    plt.grid(axis='y')

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'bar_chart_report_{current_time}.pdf')
    plt.show()

def plot_line_with_markers(performance_data):
    """Plot line charts with markers for performance data."""
    for file_size, query_data in performance_data.items():
        num_queries = list(query_data.keys())
        exec_times = [query_data[q] for q in num_queries]

        plt.plot(num_queries, exec_times, marker='o', label=f'File Size {file_size}')

    plt.xlabel('Number of Queries')
    plt.ylabel('Avg Execution Time (ms)')
    plt.title('Execution Time vs Number of Queries')
    plt.legend()
    plt.grid(True)

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'line_with_markers_report_{current_time}.pdf')
    plt.show()

def plot_logarithmic_line_chart(performance_data):
    """Plot a line chart with logarithmic scaling."""
    for file_size, query_data in performance_data.items():
        num_queries = list(query_data.keys())
        exec_times = [query_data[q] for q in num_queries]

        plt.plot(num_queries, exec_times, marker='o', label=f'File Size {file_size}')

    plt.xlabel('Number of Queries (log scale)')
    plt.ylabel('Avg Execution Time (ms)')
    plt.title('Execution Time vs Number of Queries')
    plt.xscale('log')  # Logarithmic scale for better visualization
    plt.legend()
    plt.grid(True)

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'logarithmic_line_chart_report_{current_time}.pdf')
    plt.show()

def plot_stacked_line_chart(performance_data):
    """Plot a stacked line chart."""
    num_queries = list(performance_data[list(performance_data.keys())[0]].keys())
    total_exec_times = [0] * len(num_queries)

    for file_size in performance_data.keys():
        exec_times = [performance_data[file_size][q] for q in num_queries]
        total_exec_times = [total_exec_times[i] + exec_times[i] for i in range(len(exec_times))]
        plt.plot(num_queries, total_exec_times, label=f'File Size {file_size}')

    plt.xlabel('Number of Queries')
    plt.ylabel('Total Avg Execution Time (ms)')
    plt.title('Stacked Execution Time vs Number of Queries')
    plt.legend()
    plt.grid(True)

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'stacked_line_chart_report_{current_time}.pdf')
    plt.show()

def main() -> None:
    """Main function to execute the script."""
    json_file = "test_client_metrics.json"
    performance_data = plotting_data(json_file)
    plot_scatter_chart(performance_data)


if __name__ == '__main__':
    main()
