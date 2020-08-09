"""
Service to generate and save training / testing data.
Use via CLI:
$ generate_data --output_directory=$OUTPUT_DIR --sample_size=$SAMPLE_SIZE --days=$DAYS
"""

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

import json
import os

import coronavirus_map.domain.news_retrieval_service as news_retrieval_service

def write_output_file(file_path, file_content):
    """Use JSON dump to write file"""
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as file:
        json.dump(file_content, file)


class DataGenerationService:
    """Class to generate and save training / testing data."""

    def __init__(self):
        pass

    def generate_data(self, output_directory, sample_size, hours, days):
        """
        Method to generate and save training / testing data.
        Args:
            ouput_directory: string, directory where files will be written
            sample_size: float (0, 1), fraction of total news articles to sample
            hours: int, number of hours of news to scrape; or
            days: int, number of days of news to scrape
        """
        retriever = news_retrieval_service.NewsRetrievalService(sample_size=sample_size)
        if not hours and not days:
            news = retriever.scrape_latest_gdelt_dataset()
        elif hours:
            news = retriever.scrape_latest_gdelt_datasets(4*hours)
        else:
            news = retriever.scrape_latest_gdelt_datasets(4*24*days)
        for article in news:
            file_path = os.path.join(output_directory, f"{article['GlobalEventID']}.json")
            write_output_file(file_path, article)
