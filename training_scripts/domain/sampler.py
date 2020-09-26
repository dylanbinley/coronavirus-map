"""Service to sample dataframe to N*mean with respect to a specific column."""

import pandas as pd


def _sample(dataframe: pd.DataFrame, sample_size: float) -> pd.DataFrame:
    if sample_size > dataframe.shape[0]:
        sample_size = dataframe.shape[0]
    dataframe_sampled = dataframe.sample(sample_size).reset_index(drop=True)
    return dataframe_sampled


def sample_dataframe(dataframe: pd.DataFrame, column: str, n_means=5) -> pd.DataFrame:
    dataframe_grouped = dataframe.groupby(column)
    sample_size = n_means*int(dataframe_grouped.size().mean())
    dataframe_grouped_sampled = dataframe_grouped.apply(
        lambda dataframe: _sample(dataframe, sample_size)
    )
    dataframe_sampled = pd.DataFrame(dataframe_grouped_sampled)
    dataframe_sampled = dataframe_sampled.droplevel(level=0)
    return dataframe_sampled
