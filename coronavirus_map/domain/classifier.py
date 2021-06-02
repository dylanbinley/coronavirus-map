"""Identifies news articles related to the novel coronavirus."""

from typing import List

import pandas as pd
import joblib
import json

def _string_contains_covid(string: str) -> bool:
    string = string.lower()
    contains_covid = 'coronavirus' in string or 'covid' in string
    return contains_covid


def find_coronavirus_stories(data_dicts: List[dict]) -> List[dict]:
#    coronavirus_data_dicts = []
#    for data_dict in data_dicts:
#        title = data_dict.get('ARTICLE', {}).get('TITLE', '')
#        if _string_contains_covid(title):
#            coronavirus_data_dicts.append(data_dict)
#    return coronavirus_data_dicts

    df = build_dataframe(data_dicts)

    columns = [
        'ARTICLE.TEXT',
        'ARTICLE.TITLE']

    keywords = [
        'covid',
        'corona',
        'pandem',
        'epidem',
        'mask',
        'quarant']
    df = drop_unlabeled_data(df, 'ARTICLE.TEXT')

    df = count_keywords(df, columns, keywords)

    #model = joblib.load('models/logistic_regression.pkl')
    model = joblib.load('models/random_forest_model.pkl')

    df['predicted'] = model.predict(df[keywords]);

    final_df = df[df['predicted'] == True]
    final_df = final_df.drop(['predicted'], axis = 1)

    return final_df.to_dict('records')

def build_dataframe(data_dicts):
    return pd.json_normalize(data_dicts)

def reformat_dataframe(df, columns_to_keep):
    df = df.rename(columns_to_keep, axis=1)
    df = df[list(columns_to_keep.values())]
    return df

def drop_unlabeled_data(df, column):
    return df.dropna(subset=[column])


def balance_data(df, column):
    df_grouped = df.groupby(column)
    sample_size = df_grouped.size().min()

    def sample(df):
        return df.sample(sample_size).reset_index(drop=True)

    df_grouped_sampled = df_grouped.apply(sample)
    df_sampled = pd.DataFrame(df_grouped_sampled)
    df_sampled = df_sampled.droplevel(level=0)
    return df_sampled

def count_keywords(df, columns, keywords):
    for keyword in keywords:

        def count_keyword(string):
            return sum(
                keyword in word
                for word in string.lower().split())

        df[keyword] = df[columns].applymap(count_keyword).sum(axis=1)
    return df
