from setuptools import setup

setup(
    name='coronavirus_map',
    entry_points={
        'console_scripts': [
            'retrieve_latest_news = src.cli:retrieve_latest_news',
        ],
    },
    install_requires=[
        'pandas',
        'newspaper3k',
    ]
)
