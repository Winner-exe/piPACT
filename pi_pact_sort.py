import math


def categorize(distance: float) -> int:
    """Distance binning method to be referenced across all data analysis files and classifiers."""
    return math.floor(distance)
