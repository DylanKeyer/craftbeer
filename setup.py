from setuptools import setup, find_packages

setup(
    name='beer',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = beer.settings']},
)