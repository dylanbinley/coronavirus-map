"""Identifies news articles related to the novel coronavirus."""

from typing import List
import pandas as pd
import json
import joblib

def predict(df, title_col, content_col):
    keywords =  'covid|corona|pandem|epidem|mask|quarant|vaccine|lockdown'
    return df[title_col].str.contains(pat=keywords, case=False,regex = True) & (df[content_col].str.lower().str.count(keywords) > 5)
def title_contains_keyword(df, keywords, title_col, content_col):
    return df[title_col].str.contains(pat=keywords, case=False,regex = True)

def build_dataframe(data_dicts):
    return pd.json_normalize(data_dicts)

def count_keywords(df, columns, keywords):
    for keyword in keywords:

        def count_keyword(string):
            return sum(
                keyword in word
                for word in string.lower().split())

        df[keyword] = df[columns].applymap(count_keyword).sum(axis=1)
    return df

def find_coronavirus_stories(data_dicts: List[dict]) -> List[dict]:
    #df = build_dataframe(data_dicts)
    #df = df.dropna(subset=['article.title','article.text'])
    #predicted = predict(df, title_col='ARTICLE.TITLE', content_col='ARTICLE.TEXT') 
    #return df[predicted == True].to_dict('records')
    keywords = [
            'covid',
            'corona',
            'pandem',
            'epidem',
            'mask',
            'quarant',
            'vaccine',
            ]
    pattern =  'covid|corona|pandem|epidem|mask|quarant|vaccine|lockdown'
    columns = ['ARTICLE.TITLE','ARTICLE.TEXT']
    df = build_dataframe(data_dicts)
    df = df.dropna(subset=columns)
    model = joblib.load('models/decision_tree_specific_training.pkl')
    df = count_keywords(df, columns, keywords)
    #predicted = model.predict(df[keywords]) | title_contains_keyword(df, pattern, title_col='ARTICLE.TITLE', content_col='ARTICLE.TEXT') 
    predicted = model.predict(df[keywords]) & (~title_contains_keyword(df, pattern, title_col='ARTICLE.TITLE', content_col='ARTICLE.TEXT'))
    return df[predicted == True].to_dict('records')
