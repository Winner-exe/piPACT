import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from pathlib import Path


def main():
    data: pd.DataFrame = pd.DataFrame(columns=['ADDRESS', 'TIMESTAMP',
                                               'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'RSSI', 'DISTANCE', 'TEMPERATURE',
                                               'HUMIDITY', 'PRESSURE', 'PITCH', 'ROLL', 'YAW'])
    csv_file: Path
    for csv_file in Path('.').glob('*/*.csv'):
        datapart: pd.DataFrame = pd.read_csv(csv_file)
        if datapart.shape[0] > 10000:
            datapart = datapart.head(10000)
        data = data.append(datapart)
    data = data.drop(['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER'], 1)
    predict: str = 'DISTANCE'

    style.use("ggplot")
    fig, axs = plt.subplots(2, int((len(data.columns) + 1) / 2))
    for i in range(len(data.columns)):  # TODO use a different plotting scheme to better represent center of the data.
        if data.columns[i] != predict:
            axs[int(i / int((len(data.columns) + 1) / 2)), i % int((len(data.columns) + 1) / 2)].scatter(
                data[data.columns[i]],
                data[predict])
            axs[int(i / int((len(data.columns) + 1) / 2)), i % int((len(data.columns) + 1) / 2)].set_xlabel(
                data.columns[i])
            axs[int(i / int((len(data.columns) + 1) / 2)), i % int((len(data.columns) + 1) / 2)].set_ylabel(predict)
            axs[int(i / int((len(data.columns) + 1) / 2)), i % int((len(data.columns) + 1) / 2)].set_title(
                f'{data.columns[i]} vs. {predict}')

    # fig.savefig("pi_pact_plot.png")
    plt.show()


if __name__ == "__main__":
    main()
