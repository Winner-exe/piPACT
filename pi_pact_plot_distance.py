import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
from pathlib import Path

DROP_COLUMNS = ['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'TEMPERATURE',
                'HUMIDITY', 'PRESSURE', 'PITCH', 'ROLL', 'YAW', 'SCAN']
INDEPEND: str = 'DISTANCE'
INDEPEND_UNITS: str = 'm'
DEPEND: str = 'RSSI'
DEPEND_UNITS: str = 'dBm'
SAMPLE_SIZE: int = 4000
BINS: int = 50  # Number of bins to be passed to plt.hist2d.


def main():
    """Samples data across all relevant .csv files and
       shows a 2D histogram depicting RSSI vs. Distance data."""

    # Initialize DataFrame
    data_copy: pd.DataFrame = pd.DataFrame(columns=['RSSI', 'DISTANCE'])
    csv_file: Path
    for csv_file in Path('.').glob('*/*.csv'):
        datapart: pd.DataFrame = pd.read_csv(csv_file)
        for column in DROP_COLUMNS:
            if column in datapart.columns:
                datapart = datapart.drop([column], 1)
        if datapart.shape[0] > SAMPLE_SIZE:
            datapart = datapart.head(SAMPLE_SIZE)
        data_copy = data_copy.append(datapart)
    data: pd.DataFrame = pd.DataFrame(columns=['RSSI', 'DISTANCE'])

    # Sample RSSI values from each pre-measured distance
    for distance in data_copy[INDEPEND].unique():
        datapart: pd.DataFrame = data_copy[data_copy.DISTANCE == distance]
        datapart = datapart.sample(SAMPLE_SIZE)
        data = data.append(datapart)

    # Plot a 2D histogram of RSSI vs. Distance
    style.use("ggplot")
    fig, axs = plt.subplots()
    h = axs.hist2d(data[INDEPEND], data[DEPEND], bins=BINS, cmap=plt.get_cmap('viridis'))
    axs.set_xlabel(f'{INDEPEND} ({INDEPEND_UNITS})')
    axs.set_ylabel(f'{DEPEND} ({DEPEND_UNITS})')
    axs.set_title(f'{INDEPEND} ({INDEPEND_UNITS}) vs. {DEPEND} ({DEPEND_UNITS})')

    figure = plt.gcf()
    figure.canvas.set_window_title('RSSI-Distance Histogram')

    plt.colorbar(h[3])
    plt.show()


if __name__ == "__main__":
    """Script execution."""
    main()
