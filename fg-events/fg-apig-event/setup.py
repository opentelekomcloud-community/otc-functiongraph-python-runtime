"""
Setup configuration for fg-apig-event module.
"""

from setuptools import setup, find_packages

setup(
    name="fg-apig-event",
    version="1.0.0",
    description="API Gateway event classes for FunctionGraph",
    author="T Cloud Public Community",
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
)
