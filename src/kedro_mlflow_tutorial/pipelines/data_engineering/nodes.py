import math as mt
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, Callable, Any, List, Union
from kedro_mlflow_tutorial.utils.estimator import estimate_natural_period


def transform_coordinates(
        partitioned_input: Dict[str, Callable[[], Any]],
    ) -> Dict[str, pd.DataFrame]:

    result = {}

    for partition_key, partition_load_func in tqdm(
            sorted(partitioned_input.items())
        ):
        partition_data = partition_load_func()  # load the actual partition data
        result[partition_key] = apply_rotation_matrix(
            partition_data['x'].values,
            partition_data['y'].values,
            partition_data['z'].values,
            partition_data['xx'].values,
            partition_data['yy'].values,
            partition_data['zz'].values,
        )

    return result


def apply_rotation_matrix(
        X: np.ndarray,
        Y: np.ndarray,
        Z: np.ndarray,
        XX: np.ndarray,
        YY: np.ndarray,
        ZZ: np.ndarray,
        ignore_size: int = 500
    ) -> np.ndarray:
    '''
    Applies the rotation matrix to transform absolute coordinates to
    local coordinates.

        Parameters:
            X (np.ndarray): X in absolute coordinates
            Y (np.ndarray): Y in absolute coordinates
            Z (np.ndarray): Z in absolute coordinates
            XX (np.ndarray): XX in absolute coordinates
            YY (np.ndarray): YY in absolute coordinates
            ZZ (np.ndarray): ZZ in absolute coordinates
            ignore_size (:obj:`int`, optional): Steps to ignore in the
                beggining of the series to remove transitive effects.
                Default value is 500 points

        Returns:
            rotated (np.ndarray): local coordinates
    '''
    # Transform roll, pitch, and yaw to radians
    roll = (XX*mt.pi)/180
    pitch = (YY*mt.pi)/180
    yaw = (ZZ*mt.pi)/180

    # Apply rotation matrix to X and Y
    x = X * np.cos(yaw) + Y * np.sin(yaw)
    y = -X * np.sin(yaw) + Y * np.cos(yaw)

    #Ignore the first points due to transitions effects
    return pd.DataFrame({
        'x': x[ignore_size:],
        'y': y[ignore_size:],
        'z': Z[ignore_size:],
        'roll': roll[ignore_size:],
        'pitch': pitch[ignore_size:],
        'yaw': yaw[ignore_size:],
    })


def generate_feature_data(
        partitioned_input: Dict[str, Callable[[], Any]],
        expected_tp: float,
        target_column: 'str',
        delta: float,
        repetitions: int,
        window_size: int,
    ) -> pd.DataFrame:
    '''
    Generates the master table for training the regressor model, given
    a partitioned dataset of time series. It estimates the natural period
    of time series using the Welch's Method. It also calcuates statistics
    of the time series.

    Parameters:
        partitioned_input (Dict[str, Callable[[], Any]]): kedro partitioned
            dataset, which is dict of callables.
        expected_tp (float): expected value for natural period
        delta (float): the size of the segment used to filter
            around the given center [center-delta,center+delta].
        repetitions (int): number of repetitions to apply to
            each window extracted from the time serie.
        window_size (int): size of the window extracted from
            the time serie.

    Returns:

        (pd.DataFrame): generated data


    '''

    result = []

    for partition_key, partition_load_func in tqdm(
            sorted(partitioned_input.items())
        ):
        # Initializes regressor_data dict and sets partition key
        master_data = dict()
        master_data['partition_key'] = partition_key

        # Loading data with the partition function
        if isinstance(partition_load_func, pd.DataFrame):
            partition_data = partition_load_func
        else:
            partition_data = partition_load_func()

        # Calculating statistics
        statistics_data = calculate_position_statistics(partition_data)
        master_data = {**master_data, **statistics_data}

        # Calculating natural period
        master_data[target_column], _, _, _, _ =  estimate_natural_period(
            time_serie = partition_data[target_column.replace('tp_','')].values,
            expected_tp = expected_tp,
            delta = delta,
            repetitions = repetitions,
            window_size = window_size,
        )

        # Append generated data to final result
        result.append(master_data)

    return pd.DataFrame(result)


def calculate_position_statistics(
        data: pd.DataFrame,
    ):

    return {
        'off_x': np.mean(data['x'].values),
        'off_y': np.mean(data['y'].values),
        'off_z': np.mean(data['z'].values),
        'off_roll': np.mean(data['roll'].values),
        'off_pitch': np.mean(data['pitch'].values),
        'off_yaw': np.mean(data['yaw'].values),
        'std_x': np.std(data['x'].values),
        'std_y': np.std(data['y'].values),
        'std_z': np.std(data['z'].values),
        'std_roll': np.std(data['roll'].values),
        'std_pitch': np.std(data['pitch'].values),
        'std_yaw': np.std(data['yaw'].values),
   }


def generate_training_data(
        master_dataset: pd.DataFrame,
        target_column: str,
        test_size: float,
        valid_size: float,
        shuffle: bool,
    ):

    # Generate Targets
    X, Y = define_target_data(target_column, master_dataset)

    # Scaling the data
    X_scaled, X_scaler, Y_scaled, Y_scaler = scale_regressor_data(X,Y)

    # Spliting the data
    X_train, X_valid, X_test,Y_train, Y_valid, Y_test = split_data(
        X_scaled,
        Y_scaled,
        test_size,
        valid_size,
        shuffle,
    )

    return X_train, X_valid, X_test, X_scaler, Y_train, Y_valid, Y_test, Y_scaler


def define_target_data(
        target_column: str,
        master_dataset: pd.DataFrame
    ) -> Tuple[pd.DataFrame]:

    # Drop target column in X
    X = master_dataset.drop(target_column, axis=1)

    # Get target data
    Y = master_dataset[target_column]

    return X, Y


def scale_regressor_data(
        X: pd.DataFrame,
        Y: pd.DataFrame,
    ) -> Tuple[pd.DataFrame]:

    # Set partition keys
    partition_keys = X['partition_key']

    # Scale X
    X_scaled, X_scaler = scale_data(X.drop('partition_key', axis=1))

    # Scale Y
    Y_scaled, Y_scaler = scale_data(Y.values.reshape(-1,1))

    X_scaled['partition_key'] = partition_keys

    return X_scaled, X_scaler, Y_scaled, Y_scaler


def scale_data(
        data: Union[pd.DataFrame, np.ndarray],
    ) -> Tuple:

    scaler = StandardScaler()
    scaler.fit(data)

    if isinstance(data, pd.DataFrame):
        scaled_data = pd.DataFrame(
            scaler.transform(data),
            columns = data.columns,
            index = data.index
        )
    elif isinstance(data, np.ndarray):
        scaled_data = pd.DataFrame(
            scaler.transform(data),
            columns=['y']
        )

    return scaled_data, scaler


def split_data(
        X: pd.DataFrame,
        Y: pd.DataFrame,
        test_size: float,
        valid_size: float,
        shuffle: bool,
    ) -> Tuple[pd.DataFrame]:

    x_train, x_test, y_train, y_test = train_test_split(
        X,
        Y,
        test_size=test_size,
        shuffle=shuffle
    )

    if valid_size:

        x_train, x_valid, y_train, y_valid = train_test_split(
            x_train,
            y_train,
            test_size=valid_size/(1 - test_size),
            shuffle=shuffle
        )

        return x_train, x_valid, x_test, y_train, y_valid, y_test
    else:
        return x_train, x_test, y_train, y_test
