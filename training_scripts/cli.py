"""Application-wide command line utilities"""

import click

import training_scripts.application.data_generation_service as data_generation_service
import training_scripts.application.dataset_generator_service as dataset_generator_service
import training_scripts.domain.dataframe_balancing_service as dataframe_balancing_service


@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--hours', type=click.INT, default=0)
@click.option('--days', type=click.INT, default=0)
@click.option('--geographically_balance_data', default=False)
def generate_data(output_directory, sample_size, hours, days):
    """
    Function to generate and save training / testing data.
    Args:
        ouput_directory: string, directory where files will be written
        sample_size: float (0, 1), fraction of total news articles to sample
        hours: int, number of hours of news to scrape; or
        days: int, number of days of news to scrape
    """
    generator = data_generation_service.DataGenerationService()
    generator.generate_data(output_directory, sample_size, hours, days)


@click.command()
@click.option('--data_directory', required=True, type=click.STRING)
@click.option('--output_file', 'output_path', type=click.STRING, default='dataset.balanced')
def generate_balanced_dataset(data_directory, output_path):
    """
    Function to generate CSV of GDELT GlobalID's for geographically balanced dataset.
    Args:
        data_directory: directory containing JSON-formatted data
        output_file: location to write CSV
    """
    dataframe_balancer = dataframe_balancing_service.DataFrameBalancingService(5)
    dataset_generator = dataset_generator_service.DatasetGeneratorService(dataframe_balancer)
    dataset_generator.balance_data(data_directory, output_path)
