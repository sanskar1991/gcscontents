import os

from setuptools import setup, find_packages

setup_dir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    filepath = os.path.join(setup_dir, filename)
    with open(filepath) as file:
        return file.read()

VERSION = '0.0.1'
DESCRIPTION = 'A ContentsManager for managing Google Cloud APIs.'
LONG_DESCRIPTION = 'A package that allows to build a contents manager for jupyter applications.'

# Setting up
setup(
    name="gcscontents",
    version=VERSION,
    author="Sanskar Jain",
    author_email="<email@root.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url="https://github.com/sanskar1991/gcscontents",
    # package_dir = {'':'gcscontents'},
    python_requires=">=3.7",
    extras_require={
        "test": ["pytest", "pytest-cov", "toml"],
        "dev": read_file("requirements.txt").splitlines(),
    },
    install_requires=[
        "notebook>=5.6", 
        "nbformat>=5.0.0",
        "tornado>=6", 
        "traitlets>=5.0.0",
        "requests",
        "gcsfs>=0.2.1",
        "nose"
        ],
    keywords=['python', 'jupyter', 'contents manager'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ]
)
