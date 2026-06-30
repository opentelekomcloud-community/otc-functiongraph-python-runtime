"""
Setup configuration for fg-timer-event package.
"""

from setuptools import find_packages, setup

setup(
    name="fg-timer-event",
    version="1.0.0",
    description="Timer event class for FunctionGraph",
    author="T Cloud Public Community",
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
)
