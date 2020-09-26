"""Training script command line utilities"""

import click

import training_scripts.application.data_generator as data_generator
import training_scripts.application.dataset_selector as dataset_selector
import training_scripts.application.data_labeler as data_labeler
import training_scripts.domain.sampler as sampler


@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--hours', type=click.INT, default=0)
@click.option('--days', type=click.INT, default=0)
@click.option('--balance_data', type=click.BOOL, default=False)
def generate_data(output_directory, sample_size, hours, days, balance_data):
    """
    Function to generate and save training / testing data.
    Args:
        output_directory: string, directory where files will be written
        sample_size: float (0, 1), fraction of total news articles to sample
        hours: int, number of hours of news to scrape; or
        days: int, number of days of news to scrape
        balance_data: bool, whether or not to geographically balance dataset
    """
    data_generator.generate_data(output_directory, balance_data, sample_size, hours, days)


@click.command()
@click.option('--data_directory', required=True, type=click.STRING)
@click.option('--output_file', 'output_path', type=click.STRING, default='dataset.balanced')
def select_balanced_dataset(data_directory, output_path):
    """
    Function to generate CSV of GDELT GlobalID's for geographically balanced dataset.
    Args:
        data_directory: directory containing JSON-formatted data
        output_file: location to write CSV
    """
    dataset_selector.select_data(data_directory, output_path)


@click.command()
@click.option('--data_directory', required=True, type=click.STRING)
def label_data(data_directory):
    data_labeler.label_directory(data_directory)
