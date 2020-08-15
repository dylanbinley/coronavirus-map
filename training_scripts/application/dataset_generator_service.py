import os
import json

import pandas as pd

import training_scripts.domain.dataframe_balancing_service as dataframe_balancing_service


keys_to_balance = (
    'GDELT',
    'Actor1Geo_CountryCode'
)
keys_to_keep = [
    ('GDELT', 'GlobalEventID'),
    ('GDELT', 'Actor1Geo_CountryCode'),
    ('GDELT', 'SOURCEURL')
]


def load_files_from_directory(directory):
    """Function to load JSONs of data from a directory."""
    file_contents = []
    for file_path in os.listdir(directory):
        full_file_path = os.path.join(directory, file_path)
        if os.path.isdir(full_file_path):
            continue
        with open(full_file_path, 'r') as file:
            file_content = json.load(file)
        file_contents.append(file_content)
    return file_contents


class DatasetGeneratorService:

    def __init__(self, dataframe_balancer: dataframe_balancing_service):
        self.dataframe_balancer = dataframe_balancer

    def balance_data(self, directory, output_path):
        data_dicts = load_files_from_directory(directory)
        column_to_balance = '.'.join(keys_to_balance)
        columns_to_keep = ['.'.join(keys) for keys in keys_to_keep]
        df = self._file_contents_to_dataframe(data_dicts, columns_to_keep)
        df_balanced = self.dataframe_balancer.balance_dataframe(df, column_to_balance)
        df_balanced.to_csv(output_path)

    def _file_contents_to_dataframe(self, data_dicts, columns_to_keep):
        df = pd.json_normalize(data_dicts)
        df = df[columns_to_keep]
        return df
