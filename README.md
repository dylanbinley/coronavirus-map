# Coronavirus Map

This is an in-progress application to find and map the lastest local news on COVID-19 from around the globe.

## Data Generation

To generate training and testing data, use the command line utility:
```
generate_data --output_directory=OUTPUT_DIR --sample_size=SAMPLE_SIZE --n_days=N_DAYS
```

## To-Do List
1. Convert development from package to application (requirements.txt, flask app, etc.)
2. Rethink config file usage and location