"""Service to generate and save training / testing data."""

import json
import os

import training_scripts.domain.retriever as retriever


def write_output_file(file_path: str, file_content: dict):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as file:
        json.dump(file_content, file)


def generate_data(output_directory: str, hours: int, days: int):
    if not hours and not days:
        news = retriever.scrape_latest_gdelt_dataset()
    elif hours:
        news = retriever.scrape_latest_gdelt_datasets(4*hours)
    else:
        news = retriever.scrape_latest_gdelt_datasets(4*24*days)
    for article in news:
        file_path = os.path.join(output_directory, f"{article['GDELT']['GlobalEventID']}.json")
        write_output_file(file_path, article)
