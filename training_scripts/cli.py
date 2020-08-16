"""Application-wide command line utilities"""

import click

import training_scripts.application.data_generation_service as data_generation_service
import training_scripts.application.dataset_selection_service as dataset_selection_service
import training_scripts.domain.dataframe_sampling_service as dataframe_sampling_service

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
        ouput_directory: string, directory where files will be written
        sample_size: float (0, 1), fraction of total news articles to sample
        hours: int, number of hours of news to scrape; or
        days: int, number of days of news to scrape
    """
    if balance_data:
        balancer = dataframe_sampling_service.DataFrameBalancingService(5)
    else:
        balancer = None
    generator = data_generation_service.DataGenerationService()
    generator.generate_data(output_directory, sample_size, hours, days, balancer)


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
    balancer = dataframe_sampling_service.DataFrameBalancingService(5)
    selector = dataset_selection_service.DatasetGeneratorService(balancer)
    selector.select_data(data_directory, output_path)
