"""Training script command line utilities"""

import click

import training_scripts.application.data_generation_service as data_generation_service
import training_scripts.application.dataset_selection_service as dataset_selection_service
import training_scripts.application.data_labeling_service as data_labeling_service
import training_scripts.domain.dataframe_sampling_service as dataframe_sampling_service
import training_scripts.domain.news_retrieval_service as news_retrieval_service

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
    balancer = dataframe_sampling_service.DataFrameSamplingService()
    retriever = news_retrieval_service.NewsRetrievalService(balancer, sample_size, balance_data)
    generator = data_generation_service.DataGenerationService(retriever)
    generator.generate_data(output_directory, hours, days)


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
    balancer = dataframe_sampling_service.DataFrameSamplingService()
    selector = dataset_selection_service.DatasetSelectionService(balancer)
    selector.select_data(data_directory, output_path)

@click.command()
@click.option('--data_directory', required=True, type=click.STRING)
def label_data(data_directory):
    labeler = data_labeling_service.DataLabelingService()
    labeler.label_directory(data_directory)
