import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
# import matplotlib.pyplot as plt
# from matplotlib import style
from pathlib import Path
import pickle


def main():
    """Uses Random Forest Regression to model the relationship between distance, rssi, and other variables."""
    data: pd.DataFrame = pd.DataFrame(columns=['ADDRESS', 'TIMESTAMP',
                                               'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'RSSI', 'DISTANCE', 'TEMPERATURE',
                                               'HUMIDITY', 'PRESSURE', 'PITCH', 'ROLL', 'YAW'])
    csv_file: Path
    for csv_file in Path('.').glob('*/*.csv'):
        datapart: pd.DataFrame = pd.read_csv(csv_file)
        if datapart.shape[0] > 10000:
            datapart = datapart.head(10000)
        data = data.append(datapart)
    data = data.drop(['ADDRESS', 'TIMESTAMP', 'UUID', 'MAJOR', 'MINOR', 'TX POWER', 'SCAN'], 1)

    PREDICT: str = 'DISTANCE'
    TEST_SIZE: float = 0.1

    X: np.array = np.array(data.drop([PREDICT], 1))
    y: np.array = np.array(data[PREDICT])

    X_train: np.array
    y_train: np.array
    X_test: np.array
    y_test: np.array

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=TEST_SIZE)
    # svr_model = svm.SVR(kernel='linear', C=111)
    # svr_model.fit(X_train, y_train)

    # Perform Grid-Search
    gsc = GridSearchCV(
        estimator=RandomForestRegressor(),
        param_grid={
            'max_depth': range(3, 7),
            'n_estimators': range(10, 10000),
        },
        cv=5, scoring='neg_mean_squared_error', verbose=0, n_jobs=-1)

    grid_result = gsc.fit(X_train, y_train)
    best_params = grid_result.best_params_

    rfr = RandomForestRegressor(max_depth=best_params["max_depth"], n_estimators=best_params["n_estimators"],
                                random_state=False, verbose=False, njobs=-1)

    rfr.fit(X_train, y_train)

    with("rssi-distance-model.pickle", 'wb') as f:
        pickle.dump(rfr, f)

    acc: float = rfr.score(X_test, y_test)

    print(acc)


if __name__ == "__main__":
    """Script execution."""
    main()
