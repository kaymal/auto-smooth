"""Plotting module."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

# set style
plt.style.use("fivethirtyeight")
plt.rcParams["lines.linewidth"] = 3
plt.rcParams["font.size"] = 10
plt.rcParams["figure.figsize"] = (6, 3)


def smooth(
    data: pd.DataFrame | pd.Series,
    data_filtered: pd.DataFrame | pd.Series,
    ax=None,
) -> None:
    """Plot smooth data along with the original."""
    ax = data.plot(alpha=0.7, label="Original", ax=ax)
    data_filtered.plot(ax=ax, label="Smooth")

    ax.xaxis.grid(False)
    ax.set_title("Original vs. Smooth", fontsize=12)
    ax.legend(fontsize=8)


def residuals(
    data: pd.DataFrame | pd.Series,
    data_filtered: pd.DataFrame | pd.Series,
    ax=None,
) -> None:
    """Plot residuals."""
    ax = (data - data_filtered).plot(style="o", alpha=0.7, ax=ax)
    ax.xaxis.grid(False)

    ax.axhline(y=0, linestyle="-", linewidth=2)
    ax.set_title("Residuals", fontsize=12)


def subplots(
    data: pd.DataFrame | pd.Series,
    data_filtered: pd.DataFrame | pd.Series,
) -> None:
    """Plot smoothing and residuals in subplots."""
    fig, ax = plt.subplots(nrows=2, ncols=1, gridspec_kw={"height_ratios": [3, 2]})
    fig.set_size_inches(6, 6)
    fig.tight_layout(pad=4.0)

    smooth(data, data_filtered, ax=ax[0])
    residuals(data, data_filtered, ax=ax[1])
    plt.show()
