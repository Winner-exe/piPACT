def categorize(distance: float) -> int:
    """Distance sorting method to be referenced across all data analysis files."""

    if distance < 2:
        return 0
    else:
        return 1
