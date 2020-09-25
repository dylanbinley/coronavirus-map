"""Service to populate a map with last 15 minutes of GDELT data."""

import training_scripts.domain.retriever as retriever

import coronavirus_map.domain.classifier as classifier
import coronavirus_map.domain.mapper as mapper


class MapPopulationService:
    """
    Class that populates a map with last 15 minutes of GDELT data.
    Methods:
        populate_map: populates map
    """

    def __init__(self):
        pass

    def populate_map(self, balance_data, sample_size):
        """Function to populate map with last 15 minutes of GDELT data."""
        news = retriever.scrape_latest_gdelt_dataset(balance_data, sample_size)
        covid_news = classifier.find_coronavirus_stories(news)
        plotly_map = mapper.generate_map(covid_news)
        return plotly_map
