"""Service to retrieve news articles from GDELT news tracker."""

import requests
import pandas as pd
from newspaper import Article, ArticleException

import training_scripts.domain.sampler as sampler

EXCEPTION_CAUSING_URLS = [
    'https://www.newsweek.com/',
    'https://www.forbes.com',
    'https://www.malaysiasun.com/',
]

GDELT_LATEST_UPDATE_URL = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'

GDELT_MASTER_LIST_URL = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'

GDELT_COLUMNS = [
    'GlobalEventID',
    'Day',
    'MonthYear',
    'Year',
    'FractionDate',
    'Actor1Code',
    'Actor1Name',
    'Actor1CountryCode',
    'Actor1KnownGroupCode',
    'Actor1EthnicCode',
    'Actor1Religion1Code',
    'Actor1Religion2Code',
    'Actor1Type1Code',
    'Actor1Type2Code',
    'Actor1Type3Code',
    'Actor2Code',
    'Actor2Name',
    'Actor2CountryCode',
    'Actor2KnownGroupCode',
    'Actor2EthnicCode',
    'Actor2Religion1Code',
    'Actor2Religion2Code',
    'Actor2Type1Code',
    'Actor2Type2Code',
    'Actor2Type3Code',
    'IsRootEvent',
    'EventCode',
    'EventBaseCode',
    'EventRootCode',
    'QuadClass',
    'GoldsteinScale',
    'NumMentions',
    'NumSources',
    'NumArticles',
    'AvgTone',
    'Actor1Geo_Type',
    'Actor1Geo_Fullname',
    'Actor1Geo_CountryCode',
    'Actor1Geo_ADM1Code',
    'Actor1Geo_ADM2Code',
    'Actor1Geo_Lat',
    'Actor1Geo_Long',
    'Actor1Geo_FeatureID',
    'Actor2Geo_Type',
    'Actor2Geo_Fullname',
    'Actor2Geo_CountryCode',
    'Actor2Geo_ADM1Code',
    'Actor2Geo_ADM2Code',
    'Actor2Geo_Lat',
    'Actor2Geo_Long',
    'Actor2Geo_FeatureID',
    'Action2Geo_Type',
    'Action2Geo_Fullname',
    'Action2Geo_CountryCode',
    'Action2Geo_ADM1Code',
    'Action2Geo_ADM2Code',
    'Action2Geo_Lat',
    'Action2Geo_Long',
    'Action2Geo_FeatureID',
    'DATEADDED',
    'SOURCEURL',
]


def scrape_gdelt_dataset(url,
                         balance_data,
                         sample_size,
                         blacklisted_domains=EXCEPTION_CAUSING_URLS):
    """Scrape articles linked GDELT dataset and write them to files"""
    df_gdelt = _format_gdelt_dataframe(url, balance_data, sample_size)
    for _, row in df_gdelt.iterrows():
        try:
            article_dict = _build_article_dict(row, blacklisted_domains)
            yield article_dict
        except ArticleException as exception:
            print(repr(exception))


def scrape_latest_gdelt_dataset(balance_data,
                                sample_size,
                                blacklisted_domains=EXCEPTION_CAUSING_URLS):
    """Scrape latest GDELT dataset"""
    latest_dataset_url = _get_latest_gdelt_dataset_url()
    for result in scrape_gdelt_dataset(latest_dataset_url, balance_data,
                                       sample_size, blacklisted_domains):
        yield result


def scrape_latest_gdelt_datasets(n_datasets):
    """Scrape latest GDELT dataset"""
    for dataset_url in _get_number_of_gdelt_dataset_urls(n_datasets):
        for result in scrape_gdelt_dataset(dataset_url):
            yield result


def _get_latest_gdelt_dataset_url():
    """Get URL for latest GDELT dataset"""
    information_on_latest_dataset = requests.get(GDELT_LATEST_UPDATE_URL).text
    line_with_latest_dataset, *_ = information_on_latest_dataset.splitlines()
    *_, latest_dataset_url = line_with_latest_dataset.split()
    return latest_dataset_url


def _get_number_of_gdelt_dataset_urls(n_datasets):
    """Get URL for latest n GDELT datasets"""
    gdelt_master_list = requests.get(GDELT_MASTER_LIST_URL).text
    gdelt_master_list = gdelt_master_list.splitlines()
    gdelt_datasets = [
        l for l in gdelt_master_list if l.endswith('.export.CSV.zip')
    ]
    for dataset in gdelt_datasets[-n_datasets:]:
        *_, dataset_url = dataset.split()
        yield dataset_url


def _format_gdelt_dataframe(url, balance_data, sample_size):
    """Create dataframe from URL containing zipped CSV of GDELT data"""
    df_gdelt = pd.read_csv(url, names=GDELT_COLUMNS, delimiter='\t')
    df_gdelt = df_gdelt.sample(frac=sample_size)
    df_gdelt = df_gdelt.drop_duplicates(subset=['SOURCEURL'])
    if balance_data:
        df_gdelt = sampler.sample_dataframe(df_gdelt, 'Actor1Geo_CountryCode')
    return df_gdelt


def _extract_article_contents(url):
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


def _build_article_dict(row, blacklisted_domains):
    """Create article dictionary from dataframe row"""
    article_dict = {}
    article_dict['GDELT'] = dict(row.dropna())
    url = article_dict['GDELT']['SOURCEURL']
    if any(url.startswith(u) for u in blacklisted_domains):
        return article_dict
    article_dict['ARTICLE'] = _extract_article_contents(url)
    return article_dict
