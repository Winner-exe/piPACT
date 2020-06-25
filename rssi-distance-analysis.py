import numpy as np
import pandas as pd
import sklearn
from sklearn import svm, metrics
#import matplotlib.pyplot as plt
#from matplotlib import style
from pathlib import Path
#import pickle


def main():
    data: pd.DataFrame = pd.DataFrame(columns=['ADDRESS', 'TIMESTAMP',
                                               'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'RSSI', 'DISTANCE'])
    csv_file: Path
    for csv_file in Path('.').glob('*.csv'):
        data.append(pd.read_csv(csv_file.name))

    PREDICT: str = 'DISTANCE'
    TEST_SIZE: float = 0.1

    x: np.array = np.array(data.drop([PREDICT], 1))
    y: np.array = np.array(data[PREDICT])

    x_train: np.array
    y_train: np.array
    x_test: np.array
    y_test: np.array

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=TEST_SIZE)
    svr_model = svm.SVR(kernel='linear', C=1)
    svr_model.fit(x_train, y_train)

    y_pred = svr_model.predict(x_test)

    acc: float = metrics.accuracy_score(y_test, y_pred)

    print(acc)

if __name__ == "__main__":
    main()
