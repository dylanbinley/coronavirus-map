from setuptools import setup

setup(
    name='coronavirus-map',
    entry_points={
        'console_scripts': [
            'generate_data = training_scripts.cli:generate_data',
            'select_balanced_dataset = training_scripts.cli:select_balanced_dataset',
        ],
    },
    install_requires=[
        'click',
        'newspaper3k',
        'pandas',
        'requests',
    ]
)
