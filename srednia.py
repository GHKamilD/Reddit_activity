import ast
import statistics

def read_existing_data(filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            author, count = ast.literal_eval(line.strip())
            data[author] = count
    return data

def calculate_average(data):
    """Calculate the average (mean) of the comment/post counts."""
    counts = list(data.values())
    if not counts:
        return 0
    return sum(counts) / len(counts)

def calculate_median(data):
    """Calculate the median of the comment/post counts."""
    counts = list(data.values())
    if not counts:
        return 0
    return statistics.median(counts)

# Example usage:
filename = 'posty.txt'  # or 'posty.txt' for post data
data = read_existing_data(filename)

average = calculate_average(data)
median = calculate_median(data)

print(f"Average number of comments: {average:.2f}")
print(f"Median number of comments: {median:.2f}")