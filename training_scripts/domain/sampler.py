"""Service to sample dataframe to N*mean with respect to a specific column."""

import pandas as pd

def _sample(dataframe_group, sample_size):
    if sample_size > dataframe_group.shape[0]:
        sample_size = dataframe_group.shape[0]
    dataframe_group_sampled = dataframe_group.sample(sample_size).reset_index(drop=True)
    return dataframe_group_sampled

def sample_dataframe(self, dataframe, column, n_means=5):
    """
    Function to sample dataframe with respect to a specifc column.
    Args:
        dataframe: pandas dataframe
        column: string, column to sample on
        n_means: maximum multiples of the mean number of samples per column value to allow
    """
    dataframe_grouped = dataframe.groupby(column)
    sample_size = self.n_means*int(dataframe_grouped.size().mean())
    dataframe_grouped_sampled = dataframe_grouped.apply(
        lambda dataframe_group: _sample(dataframe_group, sample_size)
    )
    dataframe_sampled = pd.DataFrame(dataframe_grouped_sampled)
    dataframe_sampled = dataframe_sampled.droplevel(level=0)
    return dataframe_sampled
