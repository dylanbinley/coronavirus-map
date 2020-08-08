"""
Service to retrieve news articles from GDELT news tracker.
Usage:
    # write how to use service
"""

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
BANNED_URLS = read_input_file('data/preprocessing/known_banned_urls.json')
GDELT_COLUMN_NAMES = read_input_file('data/preprocessing/gdelt_column_names.json')

def find_latest_gdelt_dataset(url='http://data.gdeltproject.org/gdeltv2/lastupdate.txt'):
    information_on_latest_dataset = requests.get(url).text
    line_with_latest_dataset, *_ = information_on_latest_dataset.splitlines()
    *_, latest_dataset_url = line_with_latest_dataset.split()
    return latest_dataset_url

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

def read_input_file(file_name):
    """Read JSON file"""
    with open(file_name, 'r') as file:
        return json.load(file)

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
