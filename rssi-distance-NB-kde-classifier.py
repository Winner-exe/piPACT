from kde_classifier import KDEClassifier
import pandas as pd
from pathlib import Path
from pi_pact_sort import categorize
import numpy as np
from sklearn.model_selection import GridSearchCV

DROP_COLUMNS = ['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'TEMPERATURE',
                'PITCH', 'ROLL', 'YAW', 'SCAN']
SAMPLE_SIZE = 30000


def main():
    """Creates a Naive Bayes classifier with KDE to predict a distance range given RSSI values and other variables.

       KDEClassifier class used from Chapter 5 of the Python Data Science Handbook by Jake VanderPlas:
       https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html
    """

    # Initialize DataFrame
    data: pd.DataFrame = pd.DataFrame(columns=['RSSI', 'DISTANCE', 'HUMIDITY', 'PRESSURE'])
    data_copy: pd.DataFrame = data.copy()
    csv_file: Path
    for csv_file in Path('.').glob('indoor-noObstruct-SenseHat*/*.csv'):
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
        datapart = datapart.sample(SAMPLE_SIZE, random_state=1)
        data = data.append(datapart)

    # Assign features and labels
    X: np.array = data.drop(['DISTANCE'], 1).to_numpy()
    y: np.array = data['DISTANCE'].to_numpy(dtype=int)

    # Hyperparameter tuning
    # Code adapted from Chapter 5 of the Python Data Science Handbook by Jake VanderPlas:
    # https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html
    bandwidths = np.around(np.linspace(0.5, 1, 5), decimals=4)
    grid = GridSearchCV(KDEClassifier(), {'bandwidth1': bandwidths, 'bandwidth2': bandwidths,
                                          'bandwidth3': bandwidths}, n_jobs=2)
    grid.fit(X, y)

    print(grid.best_params_)
    print('accuracy =', grid.best_score_)


if __name__ == "__main__":
    """Script execution."""
    main()
