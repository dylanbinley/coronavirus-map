"""
Service to retrieve news articles from GDELT news tracker.
Usage:
    # write how to use service
"""

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

def extract_article_contents(url):
    """Get title and text from URL"""
    article = Article(url)
    article.download()
    article.parse()
    return {'TITLE': article.title,
            'TEXT': article.text,
            'METADATA': dict(article.meta_data)}

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
        assert all(c in gdelt_columns for c in NECESSARY_GDELT_COLUMNS)
        self.gdelt_columns = gdelt_columns
        self.sample_size = sample_size

    def build_article_dict(self, row):
        """Create article dictionary from dataframe row"""
        article_dict = dict(row)
        url = article_dict['SOURCEURL']
        if any(url.startswith(u) for u in self.urls_to_skip):
            return article_dict
        article_contents = extract_article_contents(url)
        article_dict.update(article_contents)
        return article_dict


    def scrape_gdelt_dataset(self, url):
        """Scrape articles linked GDELT dataset and write them to files"""
        df_gdelt = self._format_gdelt_dataframe(url)
        for _, row in df_gdelt.iterrows():
            try:
                article_dict = self.build_article_dict(row)
                yield article_dict
            except ArticleException as exception:
                print(repr(exception))

    def scrape_latest_gdelt_dataset(self):
        """Scrape latest GDELT dataset"""
        latest_dataset_url = self._get_latest_gdelt_dataset_url()
        for result in self.scrape_gdelt_dataset(latest_dataset_url):
            yield result

    def scrape_latest_gdelt_datasets(self, n_datasets):
        """Scrape latest GDELT dataset"""
        for dataset_url in self._get_number_of_gdelt_dataset_urls(n_datasets):
            for result in self.scrape_gdelt_dataset(dataset_url):
                yield result


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
