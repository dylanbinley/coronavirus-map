from setuptools import setup

setup(
    name='coronavirus-map',
    entry_points={
        'console_scripts': [
            'generate_data = coronavirus_map.cli:generate_data',
        ],
    },
    install_requires=[
        'pandas',
        'newspaper3k',
    ]
)
