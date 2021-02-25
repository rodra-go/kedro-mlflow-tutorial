import time
import pandas as pd
import scipy as sci
from typing import Tuple, Dict, Any
from sklearn import svm
from sklearn.preprocessing._data import StandardScaler
from sklearn.metrics import mean_squared_error


def train(
        X: pd.DataFrame,
        Y: pd.DataFrame,
        kernel: str,
        gamma: str,
    ) -> Tuple[svm._classes.SVR,Dict]:

    # Initializing hyperparameters
    response_scale = sci.stats.iqr(Y)
    box_constraint = response_scale/1.349
    epsilon = 2*response_scale/13.49

    # Initializing the model
    model = svm.SVR(
        kernel = kernel,
        C = box_constraint,
        gamma = gamma,
        epsilon = epsilon
    )

    # Training the model
    time_start = time.time()
    model.fit(X.drop('partition_key', axis=1), Y)
    time_end = time.time()

    # Elapsed time in seconds for tp_x
    elapsed_time = time_end - time_start

    metrics = {
        "training_elapsed_time": {
            "value": float(elapsed_time),
             "step": 1
         },
    }

    return model, metrics


def test(
        model: svm._classes.SVR,
        X_scaler: StandardScaler,
        Y_scaler: StandardScaler,
        X_test: pd.DataFrame,
        Y_test: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:

    # Removing partition key from the data frame
    X_test.drop('partition_key', axis=1, inplace=True)

    # Generate predictions
    Y_pred = model.predict(X_test)

    # Inverse transform the data with the scaler
    X_test_inversed = X_scaler.inverse_transform(X_test)
    Y_test_inversed = Y_scaler.inverse_transform(Y_test)
    Y_pred_inversed = Y_scaler.inverse_transform(Y_pred)

    rmse = mean_squared_error(
        y_true = Y_test_inversed,
        y_pred = Y_pred_inversed
    )

    return {
        "rmse": {"value": float(rmse), "step": 1},
    }
