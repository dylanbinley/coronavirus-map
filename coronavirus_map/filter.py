import os
import json

def find_coronavirus_stories(directory):
    files_in_directory = os.listdir(directory)
    coronavirus_stories = []
    for filepath in files_in_directory:
        filepath = os.path.join(directory,filepath)
        with open(file_path, 'r') as file:
            article = json.load(file)
        article_title = article.get('ARTICLE', {}).get('TITLE', '')
        if story_is_covid(title):
            coronavirus_stories.append(filepath)
    return coronavirus_stories

def story_is_covid(title):
    title = title.lower()
    return ('coronavirus' in title or
            'covid' in title)
