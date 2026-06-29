"""
Setup configuration for fg-kafkaopensource-event package.
"""

from setuptools import find_packages, setup

setup(
    name="fg-kafkaopensource-event",
    version="1.0.0",
    description="Kafka Open Source event class for FunctionGraph",
    author="OpenTelekomCloud Community",
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
)
