"""Service to select geographically balanced dataset and write to CSV."""

# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods

import os
import json

import pandas as pd

import training_scripts.domain.dataframe_sampling_service as dataframe_sampling_service

KEYS_TO_BALANCE = (
    'GDELT',
    'Actor1Geo_CountryCode'
)
KEYS_TO_KEEP = [
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


class DatasetSelectionService:
    """
    Class to select geographically balanced dataset and write to CSV.
    Args:
        sampler: DataFrameSamplingService
    Methods:
        select_data: selects geographically balanced subset of data and writes to CSV
    """

    def __init__(self, sampler: dataframe_sampling_service.DataFrameSamplingService):
        self.sampler = sampler

    def select_data(self, directory, output_path):
        """
        Function to geographically balance dataset and write output to CSV.
        Args:
            data_directory: directory containing JSON-formatted data
            output_file: location to write CSV
        """
        data_dicts = load_files_from_directory(directory)
        column_to_balance = '.'.join(KEYS_TO_BALANCE)
        columns_to_keep = ['.'.join(keys) for keys in KEYS_TO_KEEP]
        dataframe = self._file_contents_to_dataframe(data_dicts, columns_to_keep)
        dataframe_balanced = self.sampler.sample_dataframe(dataframe, column_to_balance)
        dataframe_balanced.to_csv(output_path)

    def _file_contents_to_dataframe(self, data_dicts, columns_to_keep):
        """
        Function to create pandas DataFrame from Python dictionaries.
        Args:
            data_dicts: list, Python dictionaries of data
            columns_to_keep: list, columns to keep
        Returns:
            dataframe
        """
        dataframe = pd.json_normalize(data_dicts)
        dataframe = dataframe[columns_to_keep]
        return dataframe
