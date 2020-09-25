"""Module to identify news articles related to the novel coronavirus."""

def _string_contains_covid(string):
    """
    Function to determine whether or not a string contains coronavirus-related words.
    Args:
        string: str
    Returns:
        contains_covid: bool
    """
    string = string.lower()
    contains_covid = 'coronavirus' in string or 'covid' in string
    return contains_covid

def find_coronavirus_stories(data_dicts):
    """
    Function to find coronavirus stories.
    Args:
        data_dicts: list, dictionaries containing article data
    Returns:
        coronavirus_data_dicts: list, dicionaries containing coronavirus article data
    """
    coronavirus_data_dicts = []
    for data_dict in data_dicts:
        title = data_dict.get('ARTICLE', {}).get('TITLE', '')
        if _string_contains_covid(title):
            coronavirus_data_dicts.append(data_dict)
    return coronavirus_data_dicts


