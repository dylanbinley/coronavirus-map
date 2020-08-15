"""Application-wide command line utilities"""

import click

import coronavirus_map.application.data_generation_service as data_generation_service

@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--hours', required=False, type=click.INT, default=0)
@click.option('--days', required=False, type=click.INT, default=0)
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
