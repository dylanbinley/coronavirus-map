# Coronavirus Map

This is an in-progress application to find and map the lastest local news on COVID-19 from around the globe.

## Installation

Right now, this repository is set up as a Python package. Inside the repository:
```
pip install -e .
```
to install the requirements and command line utilities.

## Data Generation

To generate training and testing data, use the command line utility:
```
generate_data --output_directory=OUTPUT_DIR --sample_size=SAMPLE_SIZE --days=DAYS --balance_data=BALANCE_DATA
```
To generate a CSV of GDELT GlobalEventIDs to include in a geographically balanced dataset, use the command line utility:
```
select_balanced_dataset --data_directory=DATA_DIRECTORY --output_file=OUTPUT_FILE
```

## Data Processing

To label training and testing data, use the command line utility:
```
label_data --data_directory=DATA_DIR
```

## Map Generation

You can generate a map with the latest coronavirus news:
```
populate_map
```
Alternatively, you can generate a map from data/news_articles:
```
backfill_map
```

## View Sample Map

Open ```maps/backfilled.html``` to see the map with data from data/news_articles.
