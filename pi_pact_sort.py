import math


def categorize(distance: float) -> int:
    """Distance binning method to be referenced across data analysis files and classifiers.

    Args:
        distance (float): The premeasured distance, in meters.

    Returns:
        The floor of the given distance amount.
    """
    return math.floor(distance)


def bin_categorize(distance: float) -> int:
    """Binary hypothesis binning method to be referenced across data analysis files and classifiers.

    Args:
        distance (float): The premeasured distance, in meters.

    Returns:
        1 if the distance is less than 2 meters, 0 otherwise.
    """

    if distance < 2:
        return 1
    else:
        return 0
