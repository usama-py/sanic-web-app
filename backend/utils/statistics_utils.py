import statistics

def calculate_statistics(values):
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "standard_deviation": statistics.stdev(values)
    }
