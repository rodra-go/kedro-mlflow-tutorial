import time
import math as mt
import numpy as np
import scipy as sci
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn import svm
from matplotlib.figure import Figure
from scipy import signal
from typing import Tuple, List, Any, Dict, Callable
from erc.core.estimator import estimate_natural_period
from sklearn.preprocessing._data import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score


def train_svm_classifier(
        X_train: pd.DataFrame,
        Y_train: pd.DataFrame,
        kernel: str,
        gamma: str,
    ) -> Tuple[svm._classes.SVR,Dict]:

    # Initializing hyperparameters
    response_scale = sci.stats.iqr(Y_train)
    box_constraint = response_scale/1.349
    epsilon = 2*response_scale/13.49

    # Initializing the model
    model = svm.SVC(
        kernel = kernel,
        C = box_constraint,
        gamma = gamma
    )

    # Training the tp_x model
    time_start = time.time()
    model.fit(X_train.drop('partition_key', axis=1), Y_train)
    time_end = time.time()
    elapsed_time = time_end - time_start

    metrics = {
        "classifier_training_elapsed_time": {
            "value": float(elapsed_time),
             "step": 1
         },
    }

    return model, metrics


def evaluate_svm_classifier(
        model: svm._classes.SVR,
        X_test: pd.DataFrame,
        Y_test: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:

    # Removing partition key from the data frame
    X_test.drop('partition_key', axis=1, inplace=True)

    # Generate predictions
    Y_pred = model.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)


    return {
        "test_accuracy": {"value": float(accuracy), "step": 1},
    }
    return Y_pred


def train_svm_regressor(
        X_train: pd.DataFrame,
        tp_x_train: pd.DataFrame,
        tp_y_train: pd.DataFrame,
        kernel: str,
        gamma: str,
    ) -> Tuple[svm._classes.SVR,Dict]:

    # Initializing hyperparameters for tp_x
    tp_x_response_scale = sci.stats.iqr(tp_x_train)
    tp_x_box_constraint = tp_x_response_scale/1.349
    tp_x_epsilon = 2*tp_x_response_scale/13.49

    # Initializing hyperparameters for tp_y
    tp_y_response_scale = sci.stats.iqr(tp_y_train)
    tp_y_box_constraint = tp_y_response_scale/1.349
    tp_y_epsilon = 2*tp_y_response_scale/13.49

    # Initializing the model for tp_x
    tp_x_model = svm.SVR(
        kernel = kernel,
        C = tp_x_box_constraint,
        gamma = gamma,
        epsilon = tp_x_epsilon
    )

    # Initializing the model for tp_y
    tp_y_model = svm.SVR(
        kernel = kernel,
        C = tp_y_box_constraint,
        gamma = gamma,
        epsilon = tp_y_epsilon
    )

    # Training the tp_x model
    time_start = time.time()
    tp_x_model.fit(X_train.drop('partition_key', axis=1), tp_x_train)
    time_end = time.time()

    # Elapsed time in seconds for tp_x
    tp_x_elapsed_time = time_end - time_start

    # Training the tp_y model
    time_start = time.time()
    tp_y_model.fit(X_train.drop('partition_key', axis=1), tp_y_train)
    time_end = time.time()

    # Elapsed time in seconds for tp_x
    tp_y_elapsed_time = time_end - time_start

    metrics = {
        "tp_x_training_elapsed_time": {
            "value": float(tp_x_elapsed_time),
             "step": 1
         },
        "tp_y_training_elapsed_time": {
            "value": float(tp_y_elapsed_time),
            "step": 1
        },
    }

    return tp_x_model, tp_y_model, metrics


def evaluate_svm_regressor(
        tp_x_model: svm._classes.SVR,
        tp_y_model: svm._classes.SVR,
        X_scaler: StandardScaler,
        tp_x_scaler: StandardScaler,
        tp_y_scaler: StandardScaler,
        X_test: pd.DataFrame,
        tp_x_test: pd.DataFrame,
        tp_y_test: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:

    # Removing partition key from the data frame
    X_test.drop('partition_key', axis=1, inplace=True)

    # Generate predictions for tp_x
    tp_x_pred = tp_x_model.predict(X_test)
    tp_x_scaled_rmse = mean_squared_error(
        y_true = tp_x_test.values.reshape(tp_x_test.values.shape[0],),
        y_pred = tp_x_pred
    )

    # Generate predictions for tp_y
    tp_y_pred = tp_y_model.predict(X_test)
    tp_y_scaled_rmse = mean_squared_error(
        y_true = tp_y_test.values.reshape(tp_y_test.values.shape[0],),
        y_pred = tp_y_pred
    )

    # Inverse transform the data with the scaler
    inversed_X_test_data = X_scaler.inverse_transform(X_test)
    inversed_tp_x_test = tp_x_scaler.inverse_transform(tp_x_test)
    inversed_tp_y_test = tp_y_scaler.inverse_transform(tp_y_test)
    inversed_tp_x_pred = tp_x_scaler.inverse_transform(tp_x_pred)
    inversed_tp_y_pred = tp_y_scaler.inverse_transform(tp_y_pred)

    tp_x_unscaled_rmse = mean_squared_error(
        y_true = inversed_tp_x_test,
        y_pred = inversed_tp_x_pred
    )

    tp_y_unscaled_rmse = mean_squared_error(
        y_true = inversed_tp_y_test,
        y_pred = inversed_tp_y_pred
    )


    return {
        "tp_x_scaled_rmse": {"value": float(tp_x_scaled_rmse), "step": 1},
        "tp_x_unscaled_rmse": {"value": float(tp_x_unscaled_rmse), "step": 1},
        "tp_y_scaled_rmse": {"value": float(tp_y_scaled_rmse), "step": 1},
        "tp_y_unscaled_rmse": {"value": float(tp_y_unscaled_rmse), "step": 1},
    }


def estimator(
        partitioned_input: Dict[str, Callable[[], Any]],
        sgs_session_id: int,
        sgs_env_cond_id: int,
        expected_tp: float,
        target_columns: str,
        delta: float,
        repetitions: int,
        window_size: int,

    ) -> Tuple[Dict[str, Any]]:

    psd_figures = {}
    tp_figures = {}
    estimated_values = list()
    partition_key = '{}_{}_pos.csv'.format(sgs_session_id,str(sgs_env_cond_id).zfill(4))
    partition_data = partitioned_input[partition_key]()


    estimated_tp_x, tp_x_max, tp_x_min, tp_x_psd_figure, tp_x_figure = estimate_natural_period(
        time_serie = partition_data[target_columns[0].replace('tp_','')].values,
        expected_tp = expected_tp,
        delta = delta,
        repetitions = repetitions,
        window_size = window_size,
    )

    estimated_tp_y, tp_y_max, tp_y_min, tp_y_psd_figure, tp_y_figure = estimate_natural_period(
        time_serie = partition_data[target_columns[1].replace('tp_','')].values,
        expected_tp = expected_tp,
        delta = delta,
        repetitions = repetitions,
        window_size = window_size,
    )

    metrics = {
        "estimated_tp_x": {"value": float(estimated_tp_x), "step": 1},
        "tp_x_max": {"value": float(tp_x_max), "step": 1},
        "tp_x_min": {"value": float(tp_x_min), "step": 1},
        "estimated_tp_y": {"value": float(estimated_tp_y), "step": 1},
        "tp_y_max": {"value": float(tp_y_max), "step": 1},
        "tp_y_min": {"value": float(tp_y_min), "step": 1},
    }

    return metrics, tp_x_psd_figure, tp_x_figure, tp_y_psd_figure, tp_y_figure
