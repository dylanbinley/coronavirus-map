import os
import json

def main(directory):
    directory_file = os.listdir(directory)
    coronavirus_stories = []
    for filepath in directory_file:
        filepath = os.path.join(directory,filepath)
        file = open(filepath, 'r')
        try:
            title = json.load(file)['ARTICLE']['TITLE']
        except:
            continue
        if (story_is_covid(title)):
            coronavirus_stories.append(filepath)
        file.close()
    return coronavirus_stories

def story_is_covid(title):
    title = title.lower()
    return ('coronavirus' in title or
           'covid' in title)
