import random

def generate_test_file(filename, num_lines):
    with open(filename, 'w') as f:
        for _ in range(num_lines):
            # Generate a random semicolon-separated string
            line = ';'.join(str(random.randint(0, 50)) for _ in range(8))  # Adjust the range as needed
            f.write(line + '\n')

# Generate files with different sizes
file_sizes = [10000, 50000, 100000, 500000, 1000000]
for size in file_sizes:
    filename = f'test_file_{size}.txt'
    generate_test_file(filename, size)
    print(f"DEBUG: Generated file '{filename}' with {size} lines.")
