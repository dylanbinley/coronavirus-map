"""Identifies news articles related to the novel coronavirus."""

from typing import List
import pandas as pd
import json

def predict(df, title_col, content_col):
    keywords =  'covid|corona|pandem|epidem|mask|quarant|vaccine|lockdown'
    return df[title_col].str.contains(pat=keywords, case=False,regex = True) & (df[content_col].str.lower().str.count(keywords) > 5)

def build_dataframe(data_dicts):
    return pd.json_normalize(data_dicts)

def find_coronavirus_stories(data_dicts: List[dict]) -> List[dict]:
    df = build_dataframe(data_dicts)
    df = df.dropna(subset=['ARTICLE.TITLE','ARTICLE.TEXT'])
    predicted = predict(df, title_col='ARTICLE.TITLE', content_col='ARTICLE.TEXT') 
    return df[predicted == True].to_dict('records')
