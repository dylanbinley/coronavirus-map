import os
import json

def find_coronavirus_stories(directory):
    files_in_directory = os.listdir(directory)
    coronavirus_stories = []
    for file_path in files_in_directory:
        file_path = os.path.join(directory, file_path)
        with open(file_path, 'r') as file:
            article = json.load(file)
        title = article.get('ARTICLE', {}).get('TITLE', '')
        if story_is_covid(title):
            coronavirus_stories.append(file_path)
    return coronavirus_stories

def story_is_covid(title):
    title = title.lower()
    return ('coronavirus' in title or
            'covid' in title)
