import numpy as np
import pandas as pd
import sklearn
from sklearn import svm
# import matplotlib.pyplot as plt
# from matplotlib import style
from pathlib import Path


# import pickle


def main():
    data: pd.DataFrame = pd.DataFrame(columns=['ADDRESS', 'TIMESTAMP',
                                               'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'RSSI', 'DISTANCE'])
    csv_file: Path
    for csv_file in Path('.').glob('*.csv'):
        data = data.append(pd.read_csv(csv_file))
    data = data.drop(['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR'], 1)

    PREDICT: str = 'DISTANCE'
    TEST_SIZE: float = 0.1

    X: np.array = np.array(data.drop([PREDICT], 1))
    y: np.array = np.array(data[PREDICT])

    X_train: np.array
    y_train: np.array
    X_test: np.array
    y_test: np.array

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=TEST_SIZE)
    svr_model = svm.SVR(kernel='linear', C=1)
    svr_model.fit(X_train, y_train)

    acc: float = svr_model.score(X_test, y_test)

    print(acc)


if __name__ == "__main__":
    main()
