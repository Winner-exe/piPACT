import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
from pathlib import Path
from pi_pact_sort import categorize

DROP_COLUMNS = ['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER',
                'DISTANCE', 'PITCH', 'ROLL', 'YAW', 'SCAN']
INDEPEND: str = 'PRESSURE'
INDEPEND_UNITS: str = '%'
DEPEND: str = 'RSSI'
DEPEND_UNITS: str = 'dBm'


def main():
    """Samples data across all relevant .csv files and
       shows a line plot depicting the relationship between RSSI and another environmental variable."""

    # Initialize DataFrame
    data: pd.DataFrame = pd.DataFrame(columns=[DEPEND, INDEPEND])
    csv_file: Path
    for csv_file in Path('.').glob('indoor-noObstruct-SenseHat*/*.csv'):
        datapart: pd.DataFrame = pd.read_csv(csv_file)
        for column in DROP_COLUMNS:
            if column in datapart.columns:
                datapart = datapart.drop([column], 1)
        data = data.append(datapart)
    data.sort_values(by=[INDEPEND, DEPEND], inplace=True)

    # Take the mode RSSI value from each unique independent varaible value
    modes: pd.DataFrame = pd.DataFrame(columns=[DEPEND, INDEPEND])
    for value in data[INDEPEND].unique():
        datapart: pd.DataFrame = data.query(f'{INDEPEND} == {value}')
        datapart = datapart.agg(func='mode')
        modes = modes.append([datapart])

    # Plot a line plot depicting the relationship between RSSI and some other variable
    style.use("ggplot")
    fig, axs = plt.subplots()
    axs.plot(modes[INDEPEND], modes[DEPEND], marker='o')
    axs.set_xlabel(f'{INDEPEND} ({INDEPEND_UNITS})')
    axs.set_ylabel(f'{DEPEND} ({DEPEND_UNITS})')
    axs.set_title(f'{INDEPEND} ({INDEPEND_UNITS}) vs. {DEPEND} ({DEPEND_UNITS})')

    figure = plt.gcf()
    figure.canvas.set_window_title('RSSI-Distance Centers')

    plt.show()


if __name__ == "__main__":
    """Script execution."""
    main()
