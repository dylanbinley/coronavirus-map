"""
Service to label coronavirus-related news data.
Expects file path to JSON object or directory of JSON objects. JSON objects must contain the key
'ARTICLE' with subkeys 'TITLE' and 'TEXT'.
Data is labeled by adding a 'LABEL' key to a JSON object with subkeys 'WANT_ON_MAP' and 'NOTES',
then re-saving the object. You shouldn't use this service if you don't want to modify the original
data files.
You will be promoted to add values for 'WANT_ON_MAP' and 'NOTES' through the command line.
To call the command line prompts:
$ label_data --data_directory=DATA_DIR
The service will print the article title and a portion of the text.
You will then be asked to enter values for 'WANT_ON_MAP' (y/n, to be converted to boolean) and 'NOTES'
(comma separated notes, to be converted to list). These values will be added to the JSON object
saved to the original file.
"""

# pylint: disable=no-self-use

import os
import json
import re

COVID_KEYWORDS = [
    'covid',
    'corona',
    'pandem',
    'epidem',
    'mask',
    'quarant'
]

RESPONSE_MAP = {
    'f': False,
    'false': False,
    'n': False,
    't': True,
    'true': True,
    'y': True,
}

class DataLabelingService:
    """
    Class to handle data labeling.
    Methods:
        label_file: prompts users to add labels to one file
        label_directory: prompts users to add labels to all files in directory
    """

    def __init__(self):
        pass

    def _print(self, data, max_paragraphs=10):
        """Prints data headline and up to ten paragraphs of text."""
        headline = data['ARTICLE']['TITLE']
        paragraphs = [
            p.strip()
            for p in data['ARTICLE']['TEXT'].splitlines()
            if p.strip()
        ]
        if len(paragraphs) > max_paragraphs:
            paragraphs = paragraphs[:max_paragraphs] + ['...']
        text = '\n'.join(paragraphs)
        print('\nHEADLINE:\t', headline)
        print('TEXT:\t\t', repr(text))

    def _parse_response(self, prompt):
        """Accepts user input and converts response to bool or list."""
        response = input(prompt)
        if response in RESPONSE_MAP:
            return RESPONSE_MAP[response]
        if not response:
            return []
        return re.split(r'\s*,\s*', response.title())

    def _covid_in_string(self, string):
        """Returns bool: string contains coronavirus keywords."""
        return any(w in string.lower() for w in COVID_KEYWORDS)

    def _covid_in_data(self, data):
        """Returns bool: data headline or text contain coronavirus keywords."""
        return self._covid_in_string(data['ARTICLE']['TITLE']) or \
            self._covid_in_string(data['ARTICLE']['TEXT'])

    def _auto_label(self, data, file_path):
        """Automatically labels data that does not contain coronavirus keywords."""
        data['LABEL'] = {
            'WANT_ON_MAP': False,
            'NOTES': ['No Coronavirus Keywords']
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def _manually_label(self, data, file_path):
        """Prints article information, asks for user input, and saves labels."""
        self._print(data)
        want_on_map = self._parse_response('WANT ON MAP (y/n):\t')
        notes = self._parse_response('NOTES (csv):\t\t')
        save = self._parse_response('SAVE RESPONSE (y/n):\t')
        if save is not True:
            return
        data['LABEL'] = {
            'WANT_ON_MAP': want_on_map,
            'NOTES': notes
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def label_file(self, file_path):
        """Labels file at file_path"""
        with open(file_path, 'r') as file:
            data = json.load(file)
        if data.get('LABEL'):
            return
        if self._covid_in_data(data):
            self._manually_label(data, file_path)
        else:
            self._auto_label(data, file_path)

    def label_directory(self, directory):
        """Labels all files in directory"""
        for i, file_name in enumerate(os.listdir(directory)):
            if (i+1) % 10 == 0:
                print(f'\nLabeling story no. {i+1}')
            try:
                file_path = os.path.join(directory, file_name)
                self.label_file(file_path)
            except Exception as e:
                print(f'\nEncountered exception labeling {file_path}:', repr(e))
