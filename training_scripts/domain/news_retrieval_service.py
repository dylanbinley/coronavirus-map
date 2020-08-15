"""
Service to retrieve news articles from GDELT news tracker.
Usage:
    import coronavirus_map.domain.news_retrieval_service as news_retrieval_service
    retriever = news_retrieval_service.NewsRetrievalService(
        sample_size,
        blacklisted_domains,
    )
    # to generate articles from the last 15 minutes
    retriever.scrape_latest_gdelt_dataset()
    # to generate articles from the last n_datasets:
    retriever.scrape_latest_gdelt_datasets(n_datasets)
    # to generate articles from a known GDELT dataset URL
    retriever.scrape_gdelt_dataset(url)
"""

# pylint: disable=wildcard-import
# pylint: disable=dangerous-default-value
# pylint: disable=no-self-use

import requests
import pandas as pd
from newspaper import Article, ArticleException

from training_scripts.domain.news_retrieval_service_globals import *

class NewsRetrievalService:
    """
    Service to retrieve news articles and write to JSON files, with added support for GDELT TSVs.
    Args:
        sample_size: float (0, 1), fraction of articles to scrape
        blacklisted_domains: list, URL's not to scrape using newspaper
    Methods:
        scrape_latest_gdelt_dataset: generates articles from last 15 minutes
        scrape_latest_gdelt_datasets: generates articles from last N*15 minutes
        scrape_gdelt_dataset: generates articles from known GDELT dataset URL
    """

    def __init__(self,
                 sample_size=.1,
                 blacklisted_domains=EXCEPTION_CAUSING_URLS):
        self.blacklisted_domains = blacklisted_domains
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

    def _get_latest_gdelt_dataset_url(self):
        """Get URL for latest GDELT dataset"""
        information_on_latest_dataset = requests.get(GDELT_LATEST_UPDATE_URL).text
        line_with_latest_dataset, *_ = information_on_latest_dataset.splitlines()
        *_, latest_dataset_url = line_with_latest_dataset.split()
        return latest_dataset_url

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
        df_gdelt = pd.read_csv(url, names=GDELT_COLUMNS, delimiter='\t')
        df_gdelt = df_gdelt.sample(frac=self.sample_size)
        df_gdelt = df_gdelt.drop_duplicates(subset=["SOURCEURL"])
        return df_gdelt

    def _extract_article_contents(self, url):
        """Get title and text from URL"""
        article = Article(url)
        article.download()
        article.parse()
        article_content = {
            'TITLE': article.title,
            'TEXT': article.text,
            'METADATA': article.meta_data,
        }
        return article_content

    def _build_article_dict(self, row):
        """Create article dictionary from dataframe row"""
        article_dict = {}
        article_dict['GDELT'] = dict(row.dropna())
        url = article_dict['GDELT']['SOURCEURL']
        if any(url.startswith(u) for u in self.blacklisted_domains):
            return article_dict
        article_dict['ARTICLE'] = self._extract_article_contents(url)
        return article_dict
