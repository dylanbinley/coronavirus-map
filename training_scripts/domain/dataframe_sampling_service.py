"""Service to sample dataframe to N*mean with respect to a specific column."""

# pylint: disable=too-few-public-methods

import pandas as pd

class DataFrameSamplingService:
    """
    Class to sample dataframe to N*mean with respect to a specific column.
    Args:
        n_means: maximum multiples of the mean number of samples per column value to allow
    Methods:
        sample_dataframe: method to sample dataframe
    """

    def __init__(self, n_means=5):
        self.n_means = n_means

    def sample_dataframe(self, dataframe, column):
        """
        Function to sample dataframe with respect to a specifc column.
        Args:
            dataframe: pandas dataframe
            column: string, column to sample on
        """
        dataframes = dataframe.groupby(column, dropna=False)
        sample_size = self.n_means*int(dataframes.size().mean())

        def sample(dataframe, max_sample_size):
            sample_size = min(dataframe.shape[0], max_sample_size)
            return dataframe.sample(sample_size)

        dataframe_sampled = pd.concat(sample(dataframe, sample_size) for _, dataframe in dataframes)
        return dataframe_sampled
