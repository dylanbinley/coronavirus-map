"""Coronavirus map command line utilities"""

import glob
import json

import click
import coronavirus_map.application.map_populator as map_populator
import coronavirus_map.domain.classifier as classifier
import coronavirus_map.domain.mapper as mapper
import training_scripts.application.data_generation_service as data_generation_service
import training_scripts.domain.sampler as sampler


@click.command()
@click.option('--output_file', type=click.STRING, default='maps/populated.html')
def populate_map(output_file):
    """
    Function to populate a map with the last 15 minutes of GDELT data.
    Args:
        output_file: string, HTML file to write
    """
    plotly_map = map_populator.populate_map(False, 1)
    plotly_map.write_html(output_file)


@click.command()
@click.option('--output_file', type=click.STRING, default='maps/backfilled.html')
def backfill_map(output_file):
    """
    Function to populate a map from a static dataset.
    Args:
        output_file: string, HTML file to write
    """
    def json_load(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    news_articles = classifier.find_coronavirus_stories(
        json_load(path) for path in glob.glob('data/news_articles/balanced_dataset/*')
    )
    plotly_map = mapper.generate_map(news_articles)
    plotly_map.write_html(output_file)
