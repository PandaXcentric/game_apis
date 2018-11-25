from setuptools import setup
from setuptools import find_packages

setup(
    name="game_apis",
    version="1.0.0",
    url="https://github.com/PandaXcentric/game_apis",
    packages=find_packages(exclude=['test']),
    package_data={'': ['rest/config.yaml']}
)
