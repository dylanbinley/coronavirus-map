import os
import json

class NewsFilteringService:

    def __init__(self):
        pass

    def find_coronavirus_stories(self, data_dicts):
        coronavirus_data_dicts = []
        for article in data_dicts:
            title = article.get('ARTICLE', {}).get('TITLE', '')
            if self._story_is_covid(title):
                coronavirus_data_dicts.append(article)
        return coronavirus_data_dicts

    def _story_is_covid(self, title):
        title = title.lower()
        return 'coronavirus' in title or 'covid' in title
