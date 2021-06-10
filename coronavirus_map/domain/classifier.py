"""Identifies news articles related to the novel coronavirus."""

from typing import List

import pandas as pd
import json
import joblib
import pickle

THRESHOLD = .55 #Used in ml model prediction to help limit false positives

def _build_dataframe(data_dicts):
    return pd.json_normalize(data_dicts)

def _predict(classifier, X,  threshold):
    return classifier.predict_proba(X)[:,1] > threshold

def _load_pickle_file(file_name):
    with open(file_name, 'rb') as file:
        return pickle.load(file)

def find_coronavirus_stories(data_dicts: List[dict]) -> List[dict]:
    columns = ['ARTICLE.TITLE','ARTICLE.TEXT']
    df = _build_dataframe(data_dicts)
    df = df.dropna(subset=columns)

    classifier = joblib.load('models/logistic_regression_tfidf.pkl')
    tfidf_vectorizer = _load_pickle_file('models/tfidf.pkl')
    tfidf_matrix = tfidf_vectorizer.transform(df['ARTICLE.TEXT'])

    predicted = _predict(classifier,tfidf_matrix,THRESHOLD)
    return df[predicted].to_dict('records')
