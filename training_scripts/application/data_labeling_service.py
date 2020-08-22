# pylint: disable=no-self-use

import os
import json
import re

COVID_KEYWORDS = ['covid', 'corona', 'pandem', 'epidem', 'mask', 'quarant']

RESPONSE_MAP = {
    'f': False,
    'false': False,
    'n': False,
    't': True,
    'true': True,
    'y': True,
}

class DataLabelingService:

    def __init__(self):
        pass

    def _print(self, data, max_paragraphs=10):
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
        response = input(prompt)
        if response in RESPONSE_MAP:
            return RESPONSE_MAP[response]
        return re.split(r'\s*,\s*', response.title())

    def _covid_in_string(self, string):
        return any(w in string.lower() for w in COVID_KEYWORDS)

    def _covid_in_data(self, data):
        return self._covid_in_string(data['ARTICLE']['TITLE']) or \
            self._covid_in_string(data['ARTICLE']['TEXT'])

    def _auto_label(self, data, file_path):
        data['LABEL'] = {
            'WANT_ON_MAP': False,
            'NOTES': ['No Coronavirus Keywords']
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def _manually_label(self, data, file_path):
        self._print(data)
        want_on_map = self._parse_response('WANT ON MAP (y/n):\t')
        notes = self._parse_response('NOTES (csv):\t')
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
        with open(file_path, 'r') as file:
            data = json.load(file)
        if data.get('LABEL'):
            return
        if self._covid_in_data(data):
            self._manually_label(data, file_path)
        else:
            self._auto_label(data, file_path)

    def label_directory(self, directory):
        for i, file_name in enumerate(os.listdir(directory)):
            if (i+1) % 15 == 0:
                print(f'\nLabeling story no. {i+1}')
            try:
                file_path = os.path.join(directory, file_name)
                self.label_file(file_path)
            except Exception as e:
                print(f'\nEncountered exception labeling {file_path}:', repr(e))
