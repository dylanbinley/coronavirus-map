import pandas as pd

class DataFrameBalancingService:

    def __init__(self, n_means):
        self.n_means = n_means

    def balance_dataframe(self, df, column):
        df_grouped = df.groupby(column)
        sample_size = self.n_means*int(df_grouped.size().mean())

        def sample(df_group, sample_size):
            if sample_size > df_group.shape[0]:
                sample_size = df_group.shape[0]
            df_group_sampled = df_group.sample(sample_size).reset_index(drop=True)
            return df_group_sampled

        df_grouped_sampled = df_grouped.apply(lambda df_group: sample(df_group, sample_size))
        df_sampled = pd.DataFrame(df_grouped_sampled)
        df_sampled = df_sampled.droplevel(level=0)
        return df_sampled
