"""Coronavirus map command line utilities"""

import glob
import json

import click
import coronavirus_map.application.map_populator as map_populator
import coronavirus_map.domain.classifier as classifier
import coronavirus_map.domain.mapper as mapper


def _load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


@click.command()
@click.option('--output_file', type=click.STRING, default='maps/populated.html')
@click.option('--n_datasets', type=click.INT, default=1)
def populate_map(output_file, n_datasets):
    """
    Function to populate a map with the last 15 minutes of GDELT data.
    Args:
        output_file: string, HTML file to write
        n_datasets: how much data to scrape 
    """
    plotly_map = map_populator.populate_map(False, 1, n_datasets)
    #plotly_map.write_html(output_file)

    # Write out HTML file
    with open(output_file, 'w') as f:
        f.write(plotly_map)


@click.command()
@click.option('--output_file', type=click.STRING, default='maps/backfilled.html')
@click.option('--input_source', type=click.STRING, default='data/news_articles/balanced_dataset')
def backfill_map(output_file,input_source):
    """
    Function to populate a map from a static dataset.
    Args:
        output_file: string, HTML file to write
    """
    
    if input_source[-1] == '/':
        input_files = input_source + '*'
    else:
        input_files = input_source + '/*'

    news_articles = classifier.find_coronavirus_stories(
        _load_json(path) for path in glob.glob(input_files)
    )
    plotly_map = mapper.generate_map(news_articles)
    #plotly_map.write_html(output_file)
    with open(output_file, 'w') as f:
        f.write(plotly_map)
