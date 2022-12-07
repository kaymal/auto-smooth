"""Core module."""
from __future__ import annotations

import pandas as pd

from auto_smooth import savgol

TYPES = ["savgol"]


def main(
    data: pd.Series | pd.DataFrame,
    kind: str | None = None,
    verbose: int = 0,
) -> pd.Series | pd.DataFrame:
    if kind is None:
        kind = "savgol"

    if kind == "savgol":
        data_filtered = savgol.auto_savgol(data, verbose=verbose)
    else:
        raise NotImplementedError(
            "Only the following smoothing/filtering techniques are implemented:"
            f"{TYPES}"
        )

    return data_filtered
