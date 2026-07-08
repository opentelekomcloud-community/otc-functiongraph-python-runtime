# coding: utf-8

from os import path
from setuptools import setup, find_packages


NAME = "scratch-event-apig"
VERSION = "1.0.0"
AUTHOR = "T Cloud Public Community"
AUTHOR_EMAIL = "otc_ecosystem_squad@t-systems.com"
URL = "https://github.com/opentelekomcloud-community/otc-functiongraph-python-runtime"

DESCRIPTION = "OTC FunctionGraph Python sample - APIG event handler"
LICENSE = "Apache License 2.0"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords=["T Cloud Public", "apig", "functiongraph", "sample"],
    packages=find_packages(where="src", exclude=["tests*"]),
    package_dir={"": "src"},
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
    ],    
)
