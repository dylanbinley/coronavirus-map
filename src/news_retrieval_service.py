"""
Service to retrieve news articles from GDELT news tracker.
Usage:
    # write how to use service
"""

# TODO(DBB): move file writing to application layer
# TODO(DBB): document usage
# TODO(CBB/DBB): write readme
# TODO(CBB): convert from package to application

import json
import os

import requests
import pandas as pd
from newspaper import Article, ArticleException

with open('data/news_retrieval_service/config.txt', 'r') as file:
    config = json.load(file)
    
EXCEPTION_CAUSING_URLS =  config['EXCEPTION_CAUSING_URLS']
GDELT_COLUMN_NAMES =  config['GDELT_COLUMN_NAMES']
NECESSARY_GDELT_COLUMNS = config['NECESSARY_GDELT_COLUMNS']
GDELT_LATEST_UPDATE_URL = config['GDELT_LATEST_UPDATE_URL']
GDELT_MASTER_LIST_URL = config['GDELT_MASTER_LIST_URL']

def write_output_file(file_directory, file_name, file_content):
    """Write JSON file"""
    file_path = os.path.join(file_directory, file_name)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as file:
        json.dump(file_content, file)

def get_title_and_text(url):
    """Get title and text from URL"""
    article = Article(url)
    article.download()
    article.parse()
    return article.title, article.text

class NewsRetrievalService:
    """
    Service to retrieve news articles and write to JSON files, with added support for GDELT TSVs.
    Methods:
        write_article_file: retrives one URL and writes to file
        scrape_gdelt_dataset: retrives all articles in a linked GDELT dataset
    """

    def __init__(self,
                 urls_to_skip=EXCEPTION_CAUSING_URLS,
                 gdelt_columns=NECESSARY_GDELT_COLUMNS,
                 sample_size=.1):
        self.urls_to_skip = urls_to_skip
        # TODO(CBB): custom exception
        assert all(c in gdelt_columns for c in NECESSARY_GDELT_COLUMNS)
        self.gdelt_columns = gdelt_columns
        self.sample_size = sample_size

    def write_article_file(self, url, event_id, file_directory):
        """Create article file from URL, date, and event_id"""
        # TODO(CBB): remove overhead from this function
        # TODO(CBB): custom exceptions
        if os.path.isdir(file_directory):
            existing_files = os.listdir(file_directory)
        else:
            existing_files = []
        if any(f.startswith(str(event_id)) for f in existing_files):
            return
        if any(url.startswith(u) for u in self.urls_to_skip):
            return
        try:
            title, text = get_title_and_text(url)
            # TODO(CBB): create a dict from the dataframe? then add this?
            file_content = {'event_id': event_id, 'url': url, 'title': title, 'text': text}
            write_output_file(file_directory, f'{event_id}.json', file_content)
        except ArticleException as exception:
            print(repr(exception))

    def scrape_gdelt_dataset(self, url, file_directory):
        """Scrape articles linked GDELT dataset and write them to files"""
        df_gdelt = self._format_gdelt_dataframe(url)
        for _, row in df_gdelt.iterrows():
            self.write_article_file(row['SOURCEURL'], row['GlobalEventID'], file_directory)

    def scrape_latest_gdelt_dataset(self, file_directory):
        """Scrape latest GDELT dataset"""
        latest_dataset_url = self._get_latest_gdelt_dataset_url()
        self.scrape_gdelt_dataset(latest_dataset_url, file_directory)

    def scrape_latest_gdelt_datasets(self, n_datasets, file_directory):
        """Scrape latest GDELT dataset"""
        for dataset_url in self._get_number_of_gdelt_dataset_urls(n_datasets):
            self.scrape_gdelt_dataset(dataset_url, file_directory)

    def _get_latest_gdelt_dataset_url(self):
        """Get URL for latest GDELT dataset"""
        information_on_latest_dataset = requests.get(GDELT_LATEST_UPDATE_URL).text
        line_with_latest_dataset, *_ = information_on_latest_dataset.splitlines()
        *_, latest_dataset_url = line_with_latest_dataset.split()
        return latest_dataset_url

    def _get_number_of_gdelt_dataset_urls(self, n_datasets):
        """Get URL for latest n GDELT datasets"""
        gdelt_master_list = requests.get(GDELT_MASTER_LIST_URL).text
        gdelt_master_list_lines = gdelt_master_list.splitlines()
        for line in gdelt_master_list_lines[-n_datasets:]:
            *_, dataset_url = line.split()
            yield dataset_url

    def _format_gdelt_dataframe(self, url):
        """Create dataframe from URL containing zipped CSV of GDELT data"""
        df_gdelt = pd.read_csv(url, names=GDELT_COLUMN_NAMES, delimiter='\t')
        df_gdelt = df_gdelt[self.gdelt_columns]
        df_gdelt = df_gdelt.drop_duplicates(subset=["SOURCEURL"])
        df_gdelt = df_gdelt.dropna()
        df_gdelt = df_gdelt.sample(frac=self.sample_size)
        return df_gdelt
