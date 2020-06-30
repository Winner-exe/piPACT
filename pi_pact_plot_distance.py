import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import gaussian_kde


def main():  # TODO lower and equalize data volume
    data: pd.DataFrame = pd.DataFrame(columns=['ADDRESS', 'TIMESTAMP',
                                               'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'RSSI', 'DISTANCE'])
    csv_file: Path
    for csv_file in Path('.').glob('*/*.csv'):
        datapart: pd.DataFrame = pd.read_csv(csv_file)
        if datapart.shape[0] > 10000:
            datapart = datapart.head(10000)
        data = data.append(datapart)
    data = data.drop(['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'SCAN'], 1)
    independ: str = 'DISTANCE'
    predict: str = 'RSSI'

    # fit an array of size [Ndim, Nsamples]
    new_data = np.vstack([data[independ].to_numpy(dtype=np.float16), data[predict].to_numpy(dtype=np.int8)])
    print(type(new_data))
    kde = gaussian_kde(new_data)

    # evaluate on a regular grid
    xgrid = data[independ].to_numpy(dtype=np.float16)
    ygrid = data[predict].to_numpy(dtype=np.int8)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid, sparse=True)
    Z = kde.evaluate(np.vstack([Xgrid.ravel(), Ygrid.ravel()]))

    # Plot the result as an image
    plt.imshow(Z.reshape(Xgrid.shape),
               origin='lower', aspect='auto',
               extent=[-3.5, 3.5, -6, 6],
               cmap='Blues')
    cb = plt.colorbar()
    cb.set_label("density")
"""
    style.use("ggplot")
    fig, axs = plt.subplots()
    axs.hist2d(data[independ], data[predict], bins=30, cmap=plt.get_cmap('viridis'))
    axs.set_xlabel(independ)
    axs.set_ylabel(predict)
    axs.set_title(f'{independ} vs. {predict}')

    # fig.savefig("pi_pact_plot.png")
    plt.show()
"""

if __name__ == "__main__":
    main()
