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
generate_data --output_directory=OUTPUT_DIR --sample_size=SAMPLE_SIZE --days=DAYS
```

## To-Do List
1. Convert repository from package to application
2. Rethink config file usage and location