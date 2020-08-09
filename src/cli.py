import click

import src.application.data_generation_service as data_generation_service

@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--n_hours', required=False, type=click.INT)
@click.option('--n_days', required=False, type=click.INT)
def generate_data(output_directory, sample_size, n_hours=None, n_days=None):
    generator = data_generation_service.DataGenerationService()
    generator.generate_data(output_directory, sample_size, n_hours, n_days)
