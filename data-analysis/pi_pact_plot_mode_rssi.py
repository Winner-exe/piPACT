import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from pathlib import Path

DROP_COLUMNS = ['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'TEMPERATURE',
                'HUMIDITY', 'PRESSURE', 'PITCH', 'ROLL', 'YAW', 'SCAN']
INDEPEND: str = 'DISTANCE'
INDEPEND_UNITS: str = 'm'
DEPEND: str = 'RSSI'
DEPEND_UNITS: str = 'dBm'


def main():
    """Shows a plot depicting mode RSSI vs. Distance data."""

    # Initialize DataFrame
    data: pd.DataFrame = pd.DataFrame(columns=['RSSI', 'DISTANCE'])
    csv_file: Path
    for csv_file in Path('.').glob('indoor*/*.csv'):
        datapart: pd.DataFrame = pd.read_csv(csv_file)
        for column in DROP_COLUMNS:
            if column in datapart.columns:
                datapart = datapart.drop([column], 1)
        data = data.append(datapart)
        data.sort_values(by=['DISTANCE', 'RSSI'], inplace=True)
    modes: pd.DataFrame = pd.DataFrame(columns=['RSSI', 'DISTANCE'])

    # Take the mode RSSI value from each pre-measured distance
    for distance in data[INDEPEND].unique():
        datapart: pd.Series = data[data.DISTANCE == distance]
        datapart = datapart.agg(func='mode')
        modes = modes.append([datapart])

    # Plot mode RSSI vs. Distance
    style.use("ggplot")
    fig, axs = plt.subplots()
    axs.plot(modes[INDEPEND], modes[DEPEND], marker='>', label='mode')
    axs.legend(loc='upper right')
    axs.set_xlabel(f'{INDEPEND} ({INDEPEND_UNITS})')
    axs.set_ylabel(f'{DEPEND} ({DEPEND_UNITS})')
    axs.set_title(f'{INDEPEND} ({INDEPEND_UNITS}) vs. {DEPEND} ({DEPEND_UNITS})')

    figure = plt.gcf()
    figure.canvas.set_window_title('RSSI-Distance Modes')

    plt.show()


if __name__ == "__main__":
    """Script execution."""
    main()
