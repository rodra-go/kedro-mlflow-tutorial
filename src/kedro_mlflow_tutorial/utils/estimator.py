import math as mt
import numpy as np
import scipy as sci
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.figure import Figure
from scipy import signal
from typing import Tuple, List, Any, Dict, Callable, Union


def window_filter(
        f: np.ndarray,
        S: np.ndarray,
        low_limit: float,
        high_limit: float
    ) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Filter the Power Spectral Density S(f) between a low frequency
    and a high frequency limits.

        Parameters:
            f (np.ndarray): array representing the frequency vector
            S (np.ndarray): array representing the spectral density vector
            low_limit (float): low frequency limit in Hertz (Hz)
            high_limit (float): high frequency limit in Hertz (Hz)

        Returns:
        Returns:
            (tuple): tuple containing:

                f_filtered (np.ndarray): filtered frequency vector
                S_filtered (np.ndarray): filtered spectral density vector
    '''

    # Build a data matrix from f and S
    data = np.transpose(np.array([f,S]))

    # Filtering with low_limit
    low_filter = data[:,0] >= low_limit
    filtered_data = data[low_filter]

    # Filtering with high_limit
    high_filter = filtered_data[:,0] <= high_limit
    filtered_data = filtered_data[high_filter]

    # Prepare filtered series
    filtered_data = np.transpose(filtered_data)
    f_filtered = filtered_data[0]
    S_filtered = filtered_data[1]

    return f_filtered, S_filtered


def calculate_centered_momentum(
        center: float,
        delta: float,
        S: np.ndarray,
        f: np.ndarray,
        time_step: float = 1
    ) -> Tuple[float, float, float, float]:

    '''
    Calculates the moments of a function S(f).

    It uses the expected frequency to center the
    frequency spectrum in order to calculate to
    moments.

    Parameters:
            center (float): expected measured frequency value.
                The S(f) function will be filtered around this
                value in order to avoind uncessary frequencies.
            delta (float): the size of the segment used to filter
                around the given center [center-delta,center+delta].
            S (np.ndarray): spectral density vector
            f (np.ndarray): frequency as an independente variable.
            time_step (:obj:`int`, optional): integration step

    Returns:
            (tuple): tuple containing:

                m0 (np.float64): zero order momentum
                m2 (np.float64): second order momentum
                t_min (np.float64): min period considered
                t_max (np.float64): max period considered
    '''

    # Filter the spectrum around the given center
    low_limit = center - delta
    high_limit = center + delta

    f, S = window_filter(f,S,low_limit,high_limit)

    #Zero order moment
    m0 = sci.integrate.simps(S, dx=time_step)

    #Second order moment
    m2 = sci.integrate.simps(np.multiply(f**2,S), dx=time_step)

    #Max. period considered
    Tmax = 1/f[0]

    #Min period considered
    Tmin = 1/f[-1]

    return m0, m2, Tmin, Tmax


def welch_method(
        timeserie: np.ndarray,
        center: float,
        delta: float,
        repetitions: int,
        window_size: int,
        window_division: int = 1,
        window_shift_rate: float = 0.01,
        segment_overlap_rate: float = 0.5,
        sampling_frequency: float = 1.0
    ) -> Tuple[np.ndarray,
               np.ndarray,
               np.ndarray,
               np.ndarray,
               np.float64,
               np.float64,
               np.float64]:
    '''
    Calculates the natural period from a time serie using
    the welch method.


    Parameters:
            timeserie (np.ndarray):
            center (float): expected measured frequency value.
                The S(f) function will be filtered around this
                value in order to avoind uncessary frequencies.
            delta (float): the size of the segment used to filter
                around the given center [center-delta,center+delta].
            repetitions (int): number of repetitions to apply to
                each window extracted from the time serie.
            window_size (int): size of the window extracted from
                the time serie.
            window_division (int): number of divisions per window
                when calculating the mean values
            window_shift_rate (float): percentage of the window
                size to be used as shift lenght between the windows.
            segment_overlap_rate (float): wealch's method segment
                overlap rate.
            sampling_frequency (float): wealch's method sampling
                frequency.


    Returns:
            (tuple): tuple containing:

                t (np.ndarray): time as an independent variable
                measured_tp (np.ndarrary): natural periods measured
                    on each window.
                Of (np.ndarray): frequency as an independent variable
                PSD (np.ndarray): power spectral density PSD(Of)
                t_max (np.float64): maximum period identified
                t_min (np.float64): minimum period identified
                t_0 (np.float64): estimated natural period
    '''


    measured_tp = np.array([])
    t = np.array([])
    window_shift = int(window_shift_rate * window_size)
    window_total_number = int((timeserie.size - window_size) / (window_shift))


    for i in range(window_total_number):

        #Repeat the signal
        index_from = i * window_shift
        index_to = i * window_shift + window_size
        repeated = np.tile(timeserie[index_from:index_to], repetitions)
        time = np.arange(repeated.size)

        #Calculates the welch spectrum
        segment_size = repetitions * window_size / window_division
        segment_overlap = segment_overlap_rate * segment_size
        Of, PSD = signal.welch(
            x=repeated,
            fs=sampling_frequency,
            nperseg=segment_size,
            noverlap=segment_overlap
        )

        t = np.append(t,time[index_to])

        #Calculate the moments
        m0, m2, t_min, t_max = calculate_centered_momentum(center, delta, PSD, Of)

        t_0 = mt.sqrt(m0/m2)
        measured_tp = np.append(measured_tp, t_0)

    return t, measured_tp, Of, PSD, t_max, t_min


def return_plot_figure(
        x: np.ndarray,
        y: np.ndarray,
        xlabel: str = 'x',
        ylabel: str = 'y',
        title: str = 'title',
        x_range: List[float] = None,
        y_range: List[float] = None,
    ) -> Figure:
    '''
    Returns a plot figure given the x and y axis.


    Parameters:
        x (np.ndarray): numpy array corresponding to x axis
        x (np.ndarray): numpy array corresponding to y axis
        xlabel (:obj:`str`, optional): label for x axis
        ylabel (:obj:`str`, optional): label for y axis
        title (:obj:`str`, optional): plot title


    Returns:
        figure (matplotlib.figure.Figure): matplotlib figure object
    '''

    fig, ax = plt.subplots()
    ax.plot(x, y)
    if x_range:
        plt.xlim([x_range[0],x_range[1]])
    if y_range:
        plt.ylim([y_range[0],y_range[1]])

    ax.set(
        xlabel=xlabel,
        ylabel=ylabel,
        title=title
    )
    ax.grid()

    plt.close()

    return fig


def estimate_natural_period(
        time_serie: np.ndarray,
        expected_tp: float,
        delta: float,
        repetitions: int,
        window_size: int,
    ) -> Tuple[Union[
        np.float64,
        Figure
    ]]:
    '''
    Estimates the natural period of a given time serie using the Welch's Method.


    Parameters:
        time_serie (np.ndarray): time serie to be analyzed
        expected_tp (float): expected value for the natural period
        delta (float): the size of the segment used to filter around the given
            center [center-delta,center+delta].
        repetitions (int): number of repetitions to apply to
            each window extracted from the time serie.
        window_size (int): size of the window extracted from
            the time serie


    Returns:
            (tuple): tuple containing:

                tp_mean (np.ndarray): time as an independent variable
                tp_max (np.ndarrary): natural periods measured
                    on each window.
                tp_min (np.ndarray): frequency as an independent variable
                psd_figure (matplotlib.figure.Figure): matplotlib figure object
                    with the plot of the Power Spectrum Density for the given
                    time serie.
                tp_figure (matplotlib.figure.Figure): matplotlib figure object
                    with the plot of the natural periods obtained on each window.
    '''

    t, estimated_tp, Of, PSD, tp_max, tp_min = welch_method(
        timeserie = time_serie,
        center = 1/expected_tp,
        delta = delta,
        repetitions = repetitions,
        window_size = window_size,
    )

    tp_mean = estimated_tp.mean()
    psd_figure = return_plot_figure(
        x = Of,
        y = PSD,
        xlabel = 'Frequency [Hz]',
        ylabel = 'Power Spectrum Density',
        title = 'Tp_mean = {:.2f}s, Tp_max = {:.2f}s, Tp_min = {:.2f}s'.format(
                tp_mean, tp_max, tp_min
        ),
        x_range = [1/tp_max, 1/tp_min]
    )
    tp_figure = return_plot_figure(
        x = np.arange(estimated_tp.size),
        y = estimated_tp,
        xlabel = 'Window Number',
        ylabel = 'Estimated Natural Period [s]',
        title = 'Tp_mean = {:.2f}s, Tp_max = {:.2f}s, Tp_min = {:.2f}s'.format(
                tp_mean, tp_max, tp_min
        ),
    )


    return tp_mean, tp_max, tp_min, psd_figure, tp_figure
