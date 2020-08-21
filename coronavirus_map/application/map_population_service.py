"""Service to populate a map with last 15 minutes of GDELT data."""

import training_scripts.domain.dataframe_sampling_service as dataframe_sampling_service
import training_scripts.domain.news_retrieval_service as news_retrieval_service
import coronavirus_map.domain.news_classification_service as news_classification_service
import coronavirus_map.domain.map_generation_service as map_generation_service

class MapPopulationService:
    """
    Class that populates a map with last 15 minutes of GDELT data.
    Args:
        retriever: news_retrieval_service.NewsRetrievalService
         classifier: news_classification_service.NewsClassificationService
        mapper: map_generation_service.MapGenerationService
    Methods:
        populate_map: populates map
    """

    def __init__(self,
                 retriever: news_retrieval_service.NewsRetrievalService,
                 classifier: news_classification_service.NewsClassificationService,
                 mapper: map_generation_service.MapGenerationService):
        self.retriever = retriever
        self.classifier = classifier
        self.mapper = mapper

    def populate_map(self):
        """Function to populate map with last 15 minutes of GDELT data."""
        news = self.retriever.scrape_latest_gdelt_dataset()
        covid_news = self.classifier.find_coronavirus_stories(news)
        plotly_map = self.mapper.generate_map(covid_news)
        return plotly_map
