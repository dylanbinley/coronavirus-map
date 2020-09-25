"""Service to generate a map displaying COVID-19 news around the world."""

# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods

import json

import pandas as pd
import plotly.express as px

def generate_map(data_dicts):
    """
    Function to generate map.
    Args:
        data_dict: list, dictionaries containing article data
    """
    dataframe = _convert_data_dicts_to_dataframe(data_dicts)
    plotly_map = _generate_map_from_dataframe(dataframe)
    return plotly_map

def _convert_data_dicts_to_dataframe(data_dicts):
    """
    Function to convert data dicts to dataframe.
    Args:
        data_dicts: list, dictionaries of file contents
    Returns:
        dataframe: pd.DataFrame
    """
    dataframe = pd.json_normalize(data_dicts)
    return dataframe

def _generate_map_from_dataframe(dataframe):
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
        hover_data={
            'GDELT.Day': True,
            'GDELT.Actor1Geo_Fullname': True,
            'GDELT.SOURCEURL': True,
            'GDELT.Actor1Geo_Lat': False,
            'GDELT.Actor1Geo_Long': False,
        },
        labels={
            'GDELT.Day': 'Date',
            'GDELT.Actor1Geo_Fullname': 'Location',
            'GDELT.SOURCEURL': 'URL',
        },
        color_discrete_sequence=px.colors.sequential.Peach_r,
        zoom=1,
        height=750,
    )
    plotly_map.update_layout(mapbox_style='stamen-toner')
    plotly_map.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return plotly_map
