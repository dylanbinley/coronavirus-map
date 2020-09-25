"""Service to populate a map with last 15 minutes of GDELT data."""

import training_scripts.domain.news_retrieval_service as news_retrieval_service
import coronavirus_map.domain.classifier as classifier
import coronavirus_map.domain.mapper as mapper


class MapPopulationService:
    """
    Class that populates a map with last 15 minutes of GDELT data.
    Args:
        retriever: news_retrieval_service.NewsRetrievalService
    Methods:
        populate_map: populates map
    """

    def __init__(self,
                 retriever: news_retrieval_service.NewsRetrievalService):
        self.retriever = retriever

    def populate_map(self):
        """Function to populate map with last 15 minutes of GDELT data."""
        news = self.retriever.scrape_latest_gdelt_dataset()
        covid_news = classifier.find_coronavirus_stories(news)
        plotly_map = mapper.generate_map(covid_news)
        return plotly_map
