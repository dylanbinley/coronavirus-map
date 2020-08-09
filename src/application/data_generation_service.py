"""
Service to generate and save training / testing data.
Use via CLI:
$ generate_data --output_directory=$OUTPUT_DIR --sample_size=$SAMPLE_SIZE --n_days=$N_DAYS
"""

import json
import os

import src.domain.news_retrieval_service as news_retrieval_service

def write_output_file(file_path, file_content):
    """Use JSON dump to write file"""
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as file:
        json.dump(file_content, file)


# pylint: disable=too-few-public-methods
class DataGenerationService:
    """Class to generate and save training / testing data."""

    def __init__(self):
        pass

    # pylint: disable=no-self-use
    def generate_data(self, output_directory, sample_size, n_hours, n_days):
        """
        Method to generate and save training / testing data.
        Args:
            ouput_directory: string, directory where files will be written
            sample_size: float (0, 1), fraction of total news articles to sample
            n_hours: int, number of hours of news to scrape; or
            n_days: int, number of days of news to scrape
        """
        retriever = news_retrieval_service.NewsRetrievalService(sample_size=sample_size)
        if not n_hours and not n_days:
            news = retriever.scrape_latest_gdelt_dataset()
        elif n_hours:
            news = retriever.scrape_latest_gdelt_datasets(4*n_hours)
        else:
            news = retriever.scrape_latest_gdelt_datasets(4*24*n_days)
        for article in news:
            file_path = os.path.join(output_directory, f"{article['GlobalEventID']}.json")
            write_output_file(file_path, article)
