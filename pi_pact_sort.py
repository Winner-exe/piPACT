def categorize(distance: float) -> int:
    """Distance binning method to be referenced across all data analysis files and classifiers."""

    if distance < 2:
        return 1
    else:
        return 0
