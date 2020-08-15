import os
import json

import pandas as pd

def load_files_from_directory(directory):
    file_contents = []
    for file_path in os.listdir(directory):
        full_file_path = os.path.join(directory, file_path)
        if os.path.isdir(full_file_path):
            continue
        with open(full_file_path, 'r') as file:
            file_content = json.load(file)
        file_contents.append(file_content)
    return file_contents

def file_contents_to_dataframe(file_contents, must_exist=['ARTICLE.TEXT']):
    df = pd.json_normalize(file_contents)
    df = df.dropna(subset=must_exist)
    return df

def sample_dataframe(df, column, n_means=5):
    df_grouped = df.groupby(column)
    sample_size = n_means*int(df_grouped.size().mean())

    def sample(df_group, sample_size):
        if sample_size > df_group.shape[0]:
            sample_size = df_group.shape[0]
        df_group_sampled = df_group.sample(sample_size).reset_index(drop=True)
        return df_group_sampled

    df_grouped_sampled = df_grouped.apply(lambda df_group: sample(df_group, sample_size))
    df_sampled = pd.DataFrame(df_grouped_sampled)
    return df_sampled

def create_balanced_dataset(directory, balanced_column):
    file_contents = load_files_from_directory(directory)
    file_contents = remove_metadata_from_file_contents(file_contents)
    df_file_contents = file_contents_to_dataframe(file_contents)
    df_file_contents_sampled = sample_dataframe(df_file_contents, balanced_column)