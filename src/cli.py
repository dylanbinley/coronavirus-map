import click

import src.news_retrieval_service as news_retrieval_service

@click.command()
@click.option('--output_directory', required=True, type=click.STRING)
@click.option('--sample_size', required=True, type=click.FLOAT)
@click.option('--n_hours', required=False, type=click.INT)
@click.option('--n_days', required=False, type=click.INT)
def retrieve_latest_news(output_directory, sample_size, n_hours=None, n_days=None):
    retriever = news_retrieval_service.NewsRetrievalService(sample_size=sample_size)
    if not n_hours and not n_days:
        retriever.scrape_latest_gdelt_dataset(output_directory)
    elif n_hours:
        retriever = news_retrieval_service.NewsRetrievalService()
        retriever.scrape_latest_gdelt_datasets(4*n_hours, output_directory)
    else:
        retriever = news_retrieval_service.NewsRetrievalService()
        retriever.scrape_latest_gdelt_datasets(4*24*n_days, output_directory)
