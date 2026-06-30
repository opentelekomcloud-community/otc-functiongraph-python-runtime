"""
Setup configuration for fg-lts-event package.
"""

from setuptools import find_packages, setup

setup(
    name="fg-lts-event",
    version="1.0.0",
    description="LTS event class for FunctionGraph",
    author="T Cloud Public Community",
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
)
