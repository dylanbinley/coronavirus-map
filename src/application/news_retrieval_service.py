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

import src.domain.news_retrieval_service as news_retrieval_service

def write_output_file(file_path, file_content):
    """Write JSON file"""
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as file:
        json.dump(file_content, file)

class NewsRetrievalService:
    
    def __init__(self):
        pass
    
    def retrieve_latest_news(self, output_directory, sample_size, n_hours, n_days):
        retriever = news_retrieval_service.NewsRetrievalService(sample_size=sample_size)
        if not n_hours and not n_days:
            latest_news = retriever.scrape_latest_gdelt_dataset()
        elif n_hours:
            retriever = news_retrieval_service.NewsRetrievalService()
            latest_news = retriever.scrape_latest_gdelt_datasets(4*n_hours)
        else:
            retriever = news_retrieval_service.NewsRetrievalService()
            latest_news = retriever.scrape_latest_gdelt_datasets(4*24*n_days)
        for article in latest_news:
            file_path = os.path.join(output_directory, f"{article['GlobalEventID']}.json")
            write_output_file(file_path, article)
