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
generate_data --output_directory=OUTPUT_DIR --sample_size=SAMPLE_SIZE --days=DAYS --balance_data=TRUE
```


To generate a CSV of IDs to include in a geographically balanced dataset, use the command line utility:
```
generate_balanced_dataset --data_directory=DATA_DIRECTORY --output_file=OUTPUT_FILE
```

## To-Do List
1. Convert repository from package to application
2. Remove generate_balanced_dataset command line util in favor of an option to balance data before downloading
