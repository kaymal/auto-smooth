"""Core module."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from auto_smooth import metrics, plotting


def savgol(
    data: pd.Series,
    window_length: int,
    polyorder: int,
    plot: bool = True,
    **kwargs,
) -> pd.Series:
    """Apply savgol filter.

    Parameters
    ----------
    window_length:
        Window size.
    polyorder:
        Order of the polinomial.
    plot:
        Whether to plot the comparison of the original
        data and the filtered data.
    kwargs:
        Keyword arguments to be passed to the scipy
        savgol_filter function.

    Returns
    -------
    df_filtered

    """
    x = data.dropna()

    # apply savgol filter
    y = savgol_filter(x=x, window_length=window_length, polyorder=polyorder, **kwargs)

    # convert y to Series
    data_filtered = pd.Series(y, index=x.index, name=f"{data.name}_filtered")

    # reindex back with the original index
    data_filtered = data_filtered.reindex(data.index)

    if plot:
        plotting.subplots(data, data_filtered)
        # plotting.residuals(data, data_filtered)

    return data_filtered


def auto_savgol(
    data: pd.Series,
    wl_min: int | None = None,
    wl_max: int | None = None,
    po_min: int | None = None,
    po_max: int | None = None,
    max_samples: int = 50,
    metric: str = "rmse",
    plot: bool = True,
    verbose: int = 0,
) -> pd.Series:
    """Perform auto-savgol to detect best wl/po values.

    Parameters
    ----------
    data:
        Pandas Series.
    wl_min:
        Minimum window length. If None, wl_min will be
        automatically selected.
    wl_max:
        Maximum window length.
    po_min:
        Minimum value of the polyorder.
    po_max:
        Maximum value of the polyorder.
    max_samples:
        Maximum number of samples between wl_min/po_min
        and wl_max/po_max to generate.
    metric: {"rmse", "mae", "r2"}
        Metric to choose the best wl/po parameters.
    verbose:
        Whether to print out results.
        - 0: silent
        - 1: best results
        - 2: all results

    Returns
    -------
    data_filtered

    """
    max_wl_po_ratio = 3

    if po_min is None:
        po_min = 2

    if po_max is None:
        po_max = 10

    if wl_min is None:
        wl_min = int(po_min * max_wl_po_ratio)

    if wl_max is None:
        wl_max = int(np.sqrt(data.size) * 2)

    # create an array of numbers spaced evenly
    wl_grid = np.unique(np.linspace(wl_min, wl_max, max_samples).astype(int))
    # on a log scale (a geometric progression)
    # wl_grid = np.unique(np.geomspace(wl_min, wl_max).astype(int))

    results: dict = {}

    for wl in wl_grid:
        for po in range(po_min, po_max + 1):
            # make sure the po is significantly lower than coefficients
            if wl / po < max_wl_po_ratio:
                continue

            # filtered data
            data_filtered = savgol(data, window_length=wl, polyorder=po, plot=False)

            # get scores
            result = metrics.get_scores(y_true=data, y_hat=data_filtered)

            if verbose == 2:
                print(f"{wl=:2}, {po=:2} >> {result}")

            results[(wl, po)] = result

    # create a DatFrame of scores for each (wl,po) pair
    df_scores = pd.DataFrame(results)
    # get the best (minimum scored) (wl,po) pair
    wl_best, po_best = df_scores.loc[metric].idxmin()

    if verbose:
        print(f"{wl_best=}, {po_best=}")

    data_filtered = savgol(data, window_length=wl_best, polyorder=po_best, plot=plot)

    return data_filtered
