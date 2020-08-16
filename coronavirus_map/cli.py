"""Coronavirus map command line utilities"""

import glob
import json

import click

import coronavirus_map.application.map_population_service as map_population_service
import coronavirus_map.domain.news_filtering_service as news_filtering_service
import coronavirus_map.domain.map_generation_service as map_generation_service
import training_scripts.application.data_generation_service as data_generation_service
import training_scripts.application.dataset_selection_service as dataset_selection_service
import training_scripts.domain.dataframe_sampling_service as dataframe_sampling_service
import training_scripts.domain.news_retrieval_service as news_retrieval_service

@click.command()
@click.option('--output_file', type=click.STRING, default='maps/populated.html')
def populate_map(output_file):
    """
    Function to populate a map with the last 15 minutes of GDELT data.
    Args:
        output_file: string, HTML file to write
    """
    sampler = dataframe_sampling_service.DataFrameSamplingService()
    retriever = news_retrieval_service.NewsRetrievalService(sampler, 1, False)
    filterer = news_filtering_service.NewsFilteringService()
    mapper = map_generation_service.MapGenerationService()
    populator = map_population_service.MapPopulationService(retriever, filterer, mapper)
    plotly_map = populator.populate_map()
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
    filterer = news_filtering_service.NewsFilteringService()
    news_articles = filterer.find_coronavirus_stories(
        json_load(path) for path in glob.glob('data/news_articles/balanced_dataset/*')
    )
    mapper = map_generation_service.MapGenerationService()
    plotly_map = mapper.generate_map(news_articles)
    plotly_map.write_html(output_file)