import pandas as pd

from auto_smooth import utils


def test_generate_series():
    num_periods = 100
    seed = 1
    data = utils.generate_series(num_periods, seed)

    assert isinstance(data, pd.Series)
    assert data.size == num_periods
    assert int(data.iloc[-1]) == 92
