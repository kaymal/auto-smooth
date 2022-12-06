"""Metrics module.

This module allows user to evaluated the filtering results.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def mse(y_true: pd.Series, y_hat: pd.Series) -> pd.Series:
    """Mean squared error."""
    return ((y_true - y_hat) ** 2).mean()


def rmse(y_true: pd.Series, y_hat: pd.Series) -> pd.Series:
    """Root mean squared error."""
    return np.sqrt(mse(y_true, y_hat))


def mae(y_true: pd.Series, y_hat: pd.Series) -> pd.Series:
    """Mean absolute error."""
    return np.mean(np.abs(y_true - y_hat))


def r2(y_true: pd.Series, y_hat: pd.Series) -> pd.Series:
    "R-squared."
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    ss_res = ((y_true - y_hat) ** 2).sum()
    return 1 - (ss_res / ss_tot)


def get_scores(y_true: pd.Series, y_hat: pd.Series) -> dict[str, pd.Series]:
    """Get all scores."""
    scores = {
        "rmse": rmse(y_true, y_hat),
        "mae": mae(y_true, y_hat),
        "r2": r2(y_true, y_hat),
    }

    return scores
