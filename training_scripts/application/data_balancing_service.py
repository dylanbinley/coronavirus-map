import os
import json

import pandas as pd

import training_scripts.domain.dataframe_balancing_service as dataframe_balancing_service


class DataBalancingService:

    def __init__(self, dataframe_balancer: dataframe_balancing_service):
        self.dataframe_balancer = dataframe_balancer

    def balance_data(self, data_dicts, keys_to_balance, keys_to_keep):
        column_to_balance = '.'.join(keys_to_balance)
        columns_to_keep = ['.'.join(keys) for keys in keys_to_keep]
        df = self._file_contents_to_dataframe(data_dicts, columns_to_keep)
        df_balanced = self.dataframe_balancer.balance_dataframe(df, column_to_balance)
        return df_balanced

    def _file_contents_to_dataframe(self, data_dicts, columns_to_keep):
        df = pd.json_normalize(data_dicts)
        df = df[columns_to_keep]
        return df
