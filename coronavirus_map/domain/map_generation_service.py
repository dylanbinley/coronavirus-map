"""Service to generate a map displaying COVID-19 news around the world."""

# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods

import json

import pandas as pd
import plotly.express as px

class MapGenerationService:
    """
    Class that generates a map displaying COVID-19 news around the world.
    Methods:
        generate_map: generates map
    """

    def __init__(self):
        pass

    def generate_map(self, data_dicts):
        """
        Function to generate map.
        Args:
            data_dict: list, dictionaries containing article data
        """
        dataframe = self._convert_data_dicts_to_dataframe(data_dicts)
        plotly_map = self._generate_map_from_dataframe(dataframe)
        return plotly_map

    def _convert_data_dicts_to_dataframe(self, data_dicts):
        """
        Function to convert data dicts to dataframe.
        Args:
            data_dicts: list, dictionaries of file contents
        Returns:
            dataframe: pd.DataFrame
        """
        dataframe = pd.json_normalize(data_dicts)
        return dataframe

    def _generate_map_from_dataframe(self, dataframe):
        """
        Function to generate map from Pandas dataframe.
        Args:
            dataframe: pd.DataFrame
        Returns:
            plotly_map: plotly.graph_objs._figure.Figure
        """
        plotly_map = px.scatter_mapbox(
            dataframe,
            lat='GDELT.Actor1Geo_Lat',
            lon='GDELT.Actor1Geo_Long',
            hover_name='ARTICLE.TITLE',
            hover_data=['GDELT.SOURCEURL', 'GDELT.Actor1Geo_Fullname'],
            zoom=1,
            height=750,
        )
        plotly_map.update_layout(mapbox_style='open-street-map')
        plotly_map.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        return plotly_map
