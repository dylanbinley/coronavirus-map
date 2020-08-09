"""
Service to retrieve news articles from GDELT news tracker.
Usage:
    import src.domain.news_retrieval_service as news_retrieval_service
    retriever = news_retrieval_service.NewsRetrievalService(
        sample_size,
        blacklisted_domains,
        gdelt_columns_to_keep
    )
    # to generate articles from the last 15 minutes
    retriever.scrape_latest_gdelt_dataset()
    # to generate articles from the last n_datasets:
    retriever.scrape_latest_gdelt_datasets(n_datasets)
    # to generate articles from a known GDELT dataset URL
    retriever.scrape_gdelt_dataset(url)
"""

import json

import requests
import pandas as pd
from newspaper import Article, ArticleException

with open('data/news_retrieval_service/config.txt', 'r') as file:
    CONFIG = json.load(file)

EXCEPTION_CAUSING_URLS = CONFIG['EXCEPTION_CAUSING_URLS']
GDELT_COLUMN_NAMES = CONFIG['GDELT_COLUMN_NAMES']
NECESSARY_GDELT_COLUMNS = CONFIG['NECESSARY_GDELT_COLUMNS']
GDELT_LATEST_UPDATE_URL = CONFIG['GDELT_LATEST_UPDATE_URL']
GDELT_MASTER_LIST_URL = CONFIG['GDELT_MASTER_LIST_URL']


class NewsRetrievalService:
    """
    Service to retrieve news articles and write to JSON files, with added support for GDELT TSVs.
    Methods:
        scrape_latest_gdelt_dataset: generates articles from last 15 minutes
        scrape_latest_gdelt_datasets: generates articles from last n_datasets
        scrape_gdelt_dataset: generates articles from known GDELT dataset URL
    """

    def __init__(self,
                 sample_size=.1,
                 blacklisted_domains=EXCEPTION_CAUSING_URLS,
                 gdelt_columns_to_keep=NECESSARY_GDELT_COLUMNS):
        self.blacklisted_domains = blacklisted_domains
        assert all(c in gdelt_columns_to_keep for c in NECESSARY_GDELT_COLUMNS)
        self.gdelt_columns = gdelt_columns_to_keep
        self.sample_size = sample_size

    def scrape_gdelt_dataset(self, url):
        """Scrape articles linked GDELT dataset and write them to files"""
        df_gdelt = self._format_gdelt_dataframe(url)
        for _, row in df_gdelt.iterrows():
            try:
                article_dict = self._build_article_dict(row)
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

    # pylint: disable=no-self-use
    def _get_latest_gdelt_dataset_url(self):
        """Get URL for latest GDELT dataset"""
        information_on_latest_dataset = requests.get(GDELT_LATEST_UPDATE_URL).text
        line_with_latest_dataset, *_ = information_on_latest_dataset.splitlines()
        *_, latest_dataset_url = line_with_latest_dataset.split()
        return latest_dataset_url

    # pylint: disable=no-self-use
    def _get_number_of_gdelt_dataset_urls(self, n_datasets):
        """Get URL for latest n GDELT datasets"""
        gdelt_master_list = requests.get(GDELT_MASTER_LIST_URL).text
        gdelt_master_list = gdelt_master_list.splitlines()
        gdelt_datasets = [l for l in gdelt_master_list if l.endswith('.export.CSV.zip')]
        for dataset in gdelt_datasets[-n_datasets:]:
            *_, dataset_url = dataset.split()
            yield dataset_url

    def _format_gdelt_dataframe(self, url):
        """Create dataframe from URL containing zipped CSV of GDELT data"""
        df_gdelt = pd.read_csv(url, names=GDELT_COLUMN_NAMES, delimiter='\t')
        df_gdelt = df_gdelt[self.gdelt_columns]
        df_gdelt = df_gdelt.drop_duplicates(subset=["SOURCEURL"])
        df_gdelt = df_gdelt.dropna()
        df_gdelt = df_gdelt.sample(frac=self.sample_size)
        return df_gdelt

    # pylint: disable=no-self-use
    def _extract_article_contents(self, url):
        """Get title and text from URL"""
        article = Article(url)
        article.download()
        article.parse()
        return {'TITLE': article.title,
                'TEXT': article.text,
                'METADATA': dict(article.meta_data)}

    def _build_article_dict(self, row):
        """Create article dictionary from dataframe row"""
        article_dict = dict(row)
        url = article_dict['SOURCEURL']
        if any(url.startswith(u) for u in self.blacklisted_domains):
            return article_dict
        article_contents = self._extract_article_contents(url)
        article_dict.update(article_contents)
        return article_dict
