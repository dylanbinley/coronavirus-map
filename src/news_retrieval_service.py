"""
Service to retrieve news articles from GDELT news tracker.
Usage:
    # write how to use service
"""

import json
import os

import requests
import pandas as pd
from newspaper import Article, ArticleException

def read_input_file(file_name):
    """Read JSON file"""
    with open(file_name, 'r') as file:
        return json.load(file)

def write_output_file(file_directory, file_name, file_content):
    """Write JSON file"""
    file_path = os.path.join(file_directory, file_name)
    with open(file_path, 'w') as file:
        json.dump(file_content, file)

URLS_THAT_CAUSE_EXCEPTIONS = read_input_file('data/preprocessing/urls_that_cause_exceptions.json')
GDELT_COLUMN_NAMES = read_input_file('data/preprocessing/gdelt_column_names.json')

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
                 urls_to_skip=URLS_THAT_CAUSE_EXCEPTIONS,
                 gdelt_column_names=GDELT_COLUMN_NAMES,
                 gdelt_latest_update_url='http://data.gdeltproject.org/gdeltv2/lastupdate.txt',
                 gdelt_master_list_url='http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'):
        self.urls_to_skip = urls_to_skip
        self.gdelt_column_names = gdelt_column_names
        self.gdelt_latest_update_url = gdelt_latest_update_url
        self.gdelt_master_list_url = gdelt_master_list_url

    def write_article_file(self, url, event_id, file_directory):
        """Create article file from URL, date, and event_id"""
        existing_files = os.listdir(file_directory)
        if any(f.startswith(str(event_id)) for f in existing_files):
            return
        if any(url.startswith(u) for u in self.urls_to_skip):
            return
        try:
            title, text = get_title_and_text(url)
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
        information_on_latest_dataset = requests.get(self.gdelt_latest_update_url).text
        line_with_latest_dataset, *_ = information_on_latest_dataset.splitlines()
        *_, latest_dataset_url = line_with_latest_dataset.split()
        return latest_dataset_url

    def _get_number_of_gdelt_dataset_urls(self, n_datasets):
        """Get URL for latest n GDELT datasets"""
        gdelt_master_list = requests.get(self.gdelt_master_list_url).text
        gdelt_master_list_lines = gdelt_master_list.splitlines()
        for line in gdelt_master_list_lines[-n_datasets:]:
            *_, dataset_url = line.split()
            yield dataset_url

    def _format_gdelt_dataframe(self, url):
        """Create dataframe from URL containing zipped CSV of GDELT data"""
        df_gdelt = pd.read_csv(url, names=self.gdelt_column_names, delimiter='\t')
        df_gdelt = df_gdelt[['GlobalEventID', 'DATEADDED', 'SOURCEURL']]
        return df_gdelt
