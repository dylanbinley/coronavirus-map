import click

import src.application.data_generation_service as data_generation_service

@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--n_hours', required=False, type=click.INT)
@click.option('--n_days', required=False, type=click.INT)
def generate_data(output_directory, sample_size, n_hours=None, n_days=None):
    """
    Function to generate and save training / testing data.
    Args:
        ouput_directory: string, directory where files will be written
        sample_size: float (0, 1), fraction of total news articles to sample
        n_hours: int, number of hours of news to scrape; or
        n_days: int, number of days of news to scrape
    Command line usage:
        generate_data --output_directory=$OUTPUT_DIR --sample_size=$SAMPLE_SIZE --n_days=$N_DAYS
    """
    generator = data_generation_service.DataGenerationService()
    generator.generate_data(output_directory, sample_size, n_hours, n_days)
