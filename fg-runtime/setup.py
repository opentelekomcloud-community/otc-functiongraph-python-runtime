"""
Setup configuration for fg-runtime package.
"""

from setuptools import find_packages, setup

setup(
    name="fg-runtime",
    version="1.0.0",
    description="Runtime utilities for FunctionGraph",
    author="T Cloud Public Community",
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
)
