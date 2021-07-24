"""Identifies news articles related to the novel coronavirus."""

import pandas as pd
import joblib
import pickle

CLASSIFIER = 'models/logistic_regression_tfidf.pkl'
TFIDF_VECTORIZER = 'models/tfidf.pkl'

TEXT_COL = 'ARTICLE.TEXT'

THRESHOLD = .55 #Used in ml model prediction to help limit false positives

def _predict(classifier, X,  threshold):
    return classifier.predict_proba(X)[:,1] > threshold

def _load_pickle_file(file_name):
    with open(file_name, 'rb') as file:
        return pickle.load(file)

def find_coronavirus_stories(dataframe: pd.DataFrame) -> pd.DataFrame:
    #load classifiers
    classifier = joblib.load(CLASSIFIER)
    tfidf_vectorizer = _load_pickle_file(TFIDF_VECTORIZER)

    #create tfidf matrix
    tfidf_matrix = tfidf_vectorizer.transform(dataframe[TEXT_COL])

    #predict using a threshold
    predicted = _predict(classifier,tfidf_matrix,THRESHOLD)

    return dataframe[predicted]
