"""Service to sample dataframe to N*mean with respect to a specific column."""

# pylint: disable=too-few-public-methods

import pandas as pd

class DataFrameSamplingService:
    """Class to sample dataframe to N*mean with respect to a specific column."""

    def __init__(self, n_means=5):
        self.n_means = n_means

    def sample_dataframe(self, dataframe, column):
        """
        Function to sample dataframe with respect to a specifc column.
        Args:
            dataframe: pandas dataframe
            column: string, column to sample on
        """
        dataframe_grouped = dataframe.groupby(column)
        sample_size = self.n_means*int(dataframe_grouped.size().mean())

        def sample(dataframe_group, sample_size):
            if sample_size > dataframe_group.shape[0]:
                sample_size = dataframe_group.shape[0]
            dataframe_group_sampled = dataframe_group.sample(sample_size).reset_index(drop=True)
            return dataframe_group_sampled

        dataframe_grouped_sampled = dataframe_grouped.apply(
            lambda dataframe_group: sample(dataframe_group, sample_size)
        )
        dataframe_sampled = pd.DataFrame(dataframe_grouped_sampled)
        dataframe_sampled = dataframe_sampled.droplevel(level=0)
        return dataframe_sampled
