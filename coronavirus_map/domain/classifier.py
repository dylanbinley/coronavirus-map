"""Identifies news articles related to the novel coronavirus."""

from typing import List


def _string_contains_covid(string: str) -> bool:
    string = string.lower()
    contains_covid = 'coronavirus' in string or 'covid' in string
    return contains_covid


def find_coronavirus_stories(data_dicts: List[dict]) -> List[dict]:
    coronavirus_data_dicts = []
    for data_dict in data_dicts:
        title = data_dict.get('ARTICLE', {}).get('TITLE', '')
        if _string_contains_covid(title):
            coronavirus_data_dicts.append(data_dict)
    return coronavirus_data_dicts
