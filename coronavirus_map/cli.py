import click

import src.news_retrieval_service as news_retrieval_service

@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
def retrieve_latest_news(output_directory):
    retriever = news_retrieval_service.NewsRetrievalService()
    retriever.scrape_latest_gdelt_dataset(output_directory)
