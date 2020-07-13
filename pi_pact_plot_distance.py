import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
from pathlib import Path
from pi_pact_sort import categorize

DROP_COLUMNS = ['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'TEMPERATURE',
                'HUMIDITY', 'PRESSURE', 'PITCH', 'ROLL', 'YAW', 'SCAN']
SAMPLE_SIZE: int = 15000


def main():
    """Samples data across all relevant .csv files and
       shows a KDE plot depicting RSSI vs. Distance data."""

    # Initialize DataFrame
    data: pd.DataFrame = pd.DataFrame(columns=['RSSI', 'DISTANCE'])
    data_copy: pd.DataFrame = data.copy()
    csv_file: Path
    for csv_file in Path('.').glob('indoor*/*.csv'):
        datapart: pd.DataFrame = pd.read_csv(csv_file)
        for column in DROP_COLUMNS:
            if column in datapart.columns:
                datapart = datapart.drop([column], 1)
        data_copy = data_copy.append(datapart)

    # Categorize distance
    data_copy['DISTANCE'] = data_copy['DISTANCE'].map(categorize)

    # Sample data from each distance category
    for value in data_copy['DISTANCE'].unique():
        datapart = data_copy[data_copy.DISTANCE == value]
        datapart = datapart.sample(SAMPLE_SIZE)
        data = data.append(datapart)
    data_dict = {'H0': data[data.DISTANCE == 0]['RSSI'].to_numpy(dtype=int),
                 'H1': data[data.DISTANCE == 1]['RSSI'].to_numpy(dtype=int)}
    data = pd.DataFrame.from_dict(data_dict)

    # Plot a histogram of RSSI vs. Distance
    style.use("ggplot")
    data.plot.kde(bw_method=1, legend=True, backend='matplotlib')
    figure = plt.gcf()
    figure.canvas.set_window_title("Binary Hypothesis KDE")
    plt.show()


if __name__ == "__main__":
    """Script execution."""
    main()
