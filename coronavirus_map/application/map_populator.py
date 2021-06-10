"""Populates a map with last 15 minutes of GDELT data."""

import coronavirus_map.domain.classifier as classifier
import coronavirus_map.domain.mapper as mapper
import training_scripts.domain.retriever as retriever


def populate_map(balance_data: bool, sample_size: float, n_datasets: int):
    if n_datasets == 1:
        news = retriever.scrape_latest_gdelt_dataset(balance_data, sample_size)
    else:
        news = retriever.scrape_latest_gdelt_datasets(n_datasets, balance_data, sample_size)
    covid_news = classifier.find_coronavirus_stories(news)
    plotly_map = mapper.generate_map(covid_news)
    return plotly_map
