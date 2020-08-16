import json

import pandas as pd
import plotly.express as px

import coronavirus_map.filter as article_filtering_service

# TODO: return actual articles in coronavirus_filtering_service?

class MapGenerationService:

    def __init__(self):
        pass

    def generate_map(self, data_directory, output_file_path):
        data_dicts = self._load_data_from_directory(data_directory)
        dataframe = self._convert_data_dicts_to_dataframe(data_dicts)
        plotly_map = self._generate_map_from_dataframe(dataframe)
        plotly_map.write_html(output_file_path)

    def _load_data_from_directory(self, directory):
        coronavirus_file_paths = article_filtering_service.main(directory)
        def load_json(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return [load_json(file_path) for file_path in coronavirus_file_paths]

    def _convert_data_dicts_to_dataframe(self, data_dicts):
        return pd.json_normalize(data_dicts)

    def _generate_map_from_dataframe(self, dataframe):
        plotly_map = px.scatter_mapbox(
            dataframe,
            lat='GDELT.Actor1Geo_Lat',
            lon='GDELT.Actor1Geo_Long',
            hover_name='ARTICLE.TITLE',
            hover_data=['GDELT.SOURCEURL', 'GDELT.Actor1Geo_Fullname'],
            zoom=1,
            height=1500
        )
        plotly_map.update_layout(mapbox_style="open-street-map")
        plotly_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return plotly_map