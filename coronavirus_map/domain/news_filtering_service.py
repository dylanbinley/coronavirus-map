"""Service to locate news articles related to the novel coronavirus."""

# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods

class NewsFilteringService:
    """
    Class to locate news articles related to the novel coronavirus.
    Methods:
        find_coronavirus_stories: identifies news stories that mention the coronavirus
    """

    def __init__(self):
        pass

    def find_coronavirus_stories(self, data_dicts):
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
            if self._string_contains_covid(title):
                coronavirus_data_dicts.append(data_dict)
        return coronavirus_data_dicts

    def _string_contains_covid(self, string):
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
