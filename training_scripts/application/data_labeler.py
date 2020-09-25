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
You will then be asked to enter values for 'WANT_ON_MAP' (y/n, to be converted to boolean) and
'NOTES' (comma separated notes, to be converted to list). These values will be added to the JSON
object saved to the original file.
"""

import json
import os
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


def _print(data: dict, max_paragraphs: int = 10):
    headline = data['ARTICLE']['TITLE']
    paragraphs = [
        p.strip() for p in data['ARTICLE']['TEXT'].splitlines() if p.strip()
    ]
    if len(paragraphs) > max_paragraphs:
        paragraphs = paragraphs[:max_paragraphs] + ['...']
    text = '\n'.join(paragraphs)
    print('\nHEADLINE:\t', headline)
    print('TEXT:\t\t', repr(text))


def _parse_response(prompt: str):
    response = input(prompt)
    if response in RESPONSE_MAP:
        return RESPONSE_MAP[response]
    if not response:
        return []
    return re.split(r'\s*,\s*', response.title())


def _covid_in_string(string: str):
    return any(w in string.lower() for w in COVID_KEYWORDS)


def _covid_in_data(data: dict):
    return _covid_in_string(data['ARTICLE']['TITLE']) or \
        _covid_in_string(data['ARTICLE']['TEXT'])


def _auto_label(data: dict, file_path: str):
    data['LABEL'] = {'WANT_ON_MAP': False, 'NOTES': ['No Coronavirus Keywords']}
    with open(file_path, 'w') as file:
        json.dump(data, file)


def _manually_label(data: dict, file_path: str):
    _print(data)
    want_on_map = _parse_response('WANT ON MAP (y/n):\t')
    notes = _parse_response('NOTES (csv):\t\t')
    save = _parse_response('SAVE RESPONSE (y/n):\t')
    if save is not True:
        return
    data['LABEL'] = {'WANT_ON_MAP': want_on_map, 'NOTES': notes}
    with open(file_path, 'w') as file:
        json.dump(data, file)


def label_file(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    if data.get('LABEL'):
        return
    if _covid_in_data(data):
        _manually_label(data, file_path)
    else:
        _auto_label(data, file_path)


def label_directory(directory: str):
    for i, file_name in enumerate(os.listdir(directory)):
        if (i + 1) % 10 == 0:
            print(f'\nLabeling story no. {i+1}')
        try:
            file_path = os.path.join(directory, file_name)
            label_file(file_path)
        except Exception as e:
            print(f'\nEncountered exception labeling {file_path}:', repr(e))
