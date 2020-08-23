from setuptools import setup

setup(
    name='coronavirus-map',
    entry_points={
        'console_scripts': [
            'generate_data = training_scripts.cli:generate_data',
            'generate_random_data = training_scripts.cli:generate_random_data',
            'select_balanced_dataset = training_scripts.cli:select_balanced_dataset',
            'label_data = training_scripts.cli:label_data',
            'populate_map = coronavirus_map.cli:populate_map',
            'backfill_map = coronavirus_map.cli:backfill_map',
        ],
    },
    install_requires=[
        'click',
        'newspaper3k',
        'pandas',
        'plotly',
        'requests',
    ]
)
