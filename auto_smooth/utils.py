"""Utilities module."""
import numpy as np
import pandas as pd


def generate_series(
    num_periods: int = 100,
    seed: int | None = None,
) -> pd.Series:
    """Generate time series."""
    # Generate random steps with mean=0 and std=1
    rng = np.random.default_rng(seed=seed)
    random_steps = rng.normal(loc=0, scale=1.0, size=num_periods)
    # legacy
    # random_steps = np.random.normal(loc=0, scale=1.0, size=num_periods)
     
    # Simulate stock prices, with a starting price of 100
    random_steps[0]=0
    price = 100 + np.cumsum(random_steps)

    # convert to series with datetime index
    data = pd.Series(
        price, 
        index=pd.date_range(start="2022", periods=num_periods),
        name="data"
        )

    return data