"""Application-wide command line utilities"""

import os
import json

import click

import training_scripts.application.data_generation_service as data_generation_service
import training_scripts.application.data_balancing_service as data_balancing_service
import training_scripts.domain.dataframe_balancing_service as dataframe_balancing_service


@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--hours', type=click.INT, default=0)
@click.option('--days', type=click.INT, default=0)
def generate_data(output_directory, sample_size, hours, days):
    """
    Function to generate and save training / testing data.
    Args:
        ouput_directory: string, directory where files will be written
        sample_size: float (0, 1), fraction of total news articles to sample
        hours: int, number of hours of news to scrape; or
        days: int, number of days of news to scrape
    Command line usage:
        generate_data --output_directory=$OUTPUT_DIR --sample_size=$SAMPLE_SIZE --days=$DAYS
    """
    generator = data_generation_service.DataGenerationService()
    generator.generate_data(output_directory, sample_size, hours, days)


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


@click.command()
@click.option('--data_directory', required=True, type=click.STRING)
@click.option('--output_file', type=click.STRING, default='dataset.balanced')
def generate_balanced_dataset(data_directory, output_file):
    keys_to_balance = (
        'GDELT',
        'Actor1Geo_CountryCode'
    )
    keys_to_keep = [
        ('GDELT', 'GlobalEventID'),
        ('GDELT', 'Actor1Geo_CountryCode'),
        ('GDELT', 'SOURCEURL')
    ]
    n_means = 5
    data_dicts = load_files_from_directory(data_directory)
    dataframe_balancer = dataframe_balancing_service.DataFrameBalancingService(n_means)
    data_balancer = data_balancing_service.DataBalancingService(dataframe_balancer)
    df = data_balancer.balance_data(data_dicts, keys_to_balance, keys_to_keep)
    df.to_csv(output_file)
