import click

import src.application.news_retrieval_service as news_retrieval_service

@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--n_hours', required=False, type=click.INT)
@click.option('--n_days', required=False, type=click.INT)
def retrieve_latest_news(output_directory, sample_size, n_hours=None, n_days=None):
    retriever = news_retrieval_service.NewsRetrievalService()
    retriever.retrieve_latest_news(output_directory, sample_size, n_hours, n_days)
