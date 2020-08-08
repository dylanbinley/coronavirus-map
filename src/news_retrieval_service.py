import os
import json
import re

import requests
import pandas as pd
from newspaper import Article

#TODO(CBB): move gdelt dataframe creation to function
#TODO(CBB): move article parsing and writing to function
#TODO(CBB): move __main__ to function
#TODO(CBB): add click cli

BANNED_URLS = [
    'https://www.newsweek.com/'
]

COLUMN_NAMES = list(range(61))
COLUMN_NAMES[1] = 'DATE'
COLUMN_NAMES[60] = 'URL'

# GDELT_MASTER_FILE_LIST_URL = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'

GDELT_MOST_RECENT_FILE_LIST_URL = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'

GDELT_MOST_RECENT_FILE_LIST  = requests.get(GDELT_MOST_RECENT_FILE_LIST_URL)

NEWS_ARTICLES = []

def clean_date(date):
    date = str(date)
    return date

def get_publisher(url):
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
    title = title.lower()
    title = re.sub(r'\W', '-', title)
    title = re.sub(r'-+', '-', title)
    return title

def create_article_file_name(title, url, date):
    file_name = '_'.join((clean_date(date), get_publisher(url), clean_title(title)))
    file_name = f'{file_name}.txt'
    return file_name

def write_output_file(file_name, file_directory, file_content):
    with open(os.path.join(file_directory, file_name), 'w') as file:
        json.dump(file_content, file)

for line in GDELT_MOST_RECENT_FILE_LIST.text.splitlines():
    *_, NEWEST_GDELT_STORY_LIST_URL = line.split()
    df = pd.read_csv(NEWEST_GDELT_STORY_LIST_URL, names=COLUMN_NAMES, delimiter='\t')
    for i, (url, date) in enumerate(set(zip(df['URL'], df['DATE']))):
        if any(url.startswith(banned_url) for banned_url in BANNED_URLS):
            continue
        print(f"Gathering content from {url}")
        try:
            article = Article(url)
            article.download()
            article.parse()
            file_name = create_article_file_name(article.title, url, date)
            write_output_file(file_name, 'data/news_articles/', {'url': url, 'date': date, 'title': article.title, 'text': article.text})
            ### handle file writing
        except Exception as e:
            print(repr(e))
        if i > 5:
            break
    break

