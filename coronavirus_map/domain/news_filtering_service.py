import os
import json

class NewsFilteringService:

    def __init__(self):
        pass

    def find_coronavirus_stories(self, directory):
        files_in_directory = os.listdir(directory)
        coronavirus_stories = []
        for file_path in files_in_directory:
            file_path = os.path.join(directory, file_path)
            with open(file_path, 'r') as file:
                article = json.load(file)
            title = article.get('ARTICLE', {}).get('TITLE', '')
            if self._story_is_covid(title):
                coronavirus_stories.append(file_path)
        return coronavirus_stories

    def _story_is_covid(self, title):
        title = title.lower()
        return 'coronavirus' in title or 'covid' in title
