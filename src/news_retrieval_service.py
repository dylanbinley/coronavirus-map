"""
Service to retrieve news articles from GDELT news tracker.
Usage:
    # write how to use service
"""

# TOD(DLB): pylint
# TODO(DLB): delete unused variables

import json
import os
import re

import requests
import pandas as pd
from newspaper import Article

# TODO(DLB): move article parsing and writing to function
# TODO(DLB): move main loop to function
# TODO(DLB): add click cli

# TODO(DLB): test for URLs to add here
BANNED_URLS = [
    'https://www.newsweek.com/'
]

# TODO(DLB): move gdelt column names to new file for readability
# TODO(DLB): read gdelt column names
GDELT_COLUMN_NAMES = [
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

# TODO(DLB): decide how to handle GDELT files -- always go to most_recent_file_list?
# read master_file_list and grab N new entries? etc.


# GDELT_MASTER_FILE_LIST_URL = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'

GDELT_MOST_RECENT_FILE_LIST_URL = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'

GDELT_MOST_RECENT_FILE_LIST = requests.get(GDELT_MOST_RECENT_FILE_LIST_URL)

NEWS_ARTICLES = []

# TODO(DLB): determine which GDELT_COLUMNS are important
def create_gdelt_dataframe(url):
    """Create dataframe from URL containing zipped CSV of GDELT data"""
    df_gdelt = pd.read_csv(url, names=GDELT_COLUMN_NAMES, delimiter='\t')
    return df_gdelt[['DATEADDED', 'SOURCEURL']]

def clean_date(date):
    """Format date for file name"""
    date = str(date)
    return date

def get_publisher(url):
    """Format URL for file name"""
    starting_substrings = [
        'https://www.',
        'http://www.',
        'http://www3.',
        'https://',
        'http://',
    ]
    for substring in starting_substrings:
        start = url.find(substring)
        if start > -1:
            start += len(substring)
            break
    url = url[start:]
    end = url.find(r'/')
    url = url[:end]
    url = url[:end]
    url = re.sub(r'\.', '-', url)
    return url

def clean_title(title):
    """Format title for file name"""
    title = title.lower()
    title = re.sub(r'\W', '-', title)
    title = re.sub(r'-+', '-', title)
    return title

def create_article_file_name(title, url, date):
    """Create article file name"""
    file_name = '_'.join((clean_date(date), get_publisher(url), clean_title(title)))
    file_name = f'{file_name}.json'
    return file_name

def write_output_file(file_name, file_directory, file_content):
    """Write JSON file"""
    with open(os.path.join(file_directory, file_name), 'w') as file:
        json.dump(file_content, file)

# TODO(DLB): port this to function
def __main__():
    """Function string to rewrite after refactor"""
    for line in GDELT_MOST_RECENT_FILE_LIST.text.splitlines():
        *_, newest_gdelt_story_list_url = line.split()
        df_gdelt = pd.read_csv(
            newest_gdelt_story_list_url,
            names=GDELT_COLUMN_NAMES,
            delimiter='\t'
        )
        for i, (url, date) in enumerate(set(zip(df_gdelt['SOURCEURL'], df_gdelt['DATEADDED']))):
            if any(url.startswith(banned_url) for banned_url in BANNED_URLS):
                continue
            print(f"Gathering content from {url}")
            try:
                article = Article(url)
                article.download()
                article.parse()
                file_name = create_article_file_name(article.title, url, date)
                write_output_file(
                    file_name,
                    'data/news_articles/',
                    {'url': url, 'date': date, 'title': article.title, 'text': article.text}
                )
                ### handle file writing
            except Exception as exception:
                print(repr(exception))
            if i > 5:
                break
        break
