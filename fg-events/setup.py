# coding: utf-8

from os import path
from setuptools import setup, find_packages


NAME = "fg-events"
VERSION = "1.0.0"
AUTHOR = "T Cloud Public Community"
AUTHOR_EMAIL = "otc_ecosystem_squad@t-systems.com"
URL = "https://github.com/opentelekomcloud-community/otc-functiongraph-python-runtime"

DESCRIPTION = "fg-events"
LICENSE = "Apache License 2.0"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

REQUIRES = []


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    keywords=["T Cloud Public", "sdk", "fg-events", "functiongraph"],
    package_dir={
      "fg_apig_event": "fg-apig-event/src/fg_apig_event",
      "fg_cts_event": "fg-cts-event/src/fg_cts_event",
      "fg_dds_event": "fg-dds-event/src/fg_dds_event",
      "fg_dms4kafka_event": "fg-dms4kafka-event/src/fg_dms4kafka_event",      
      "fg_dms4rocketmq_event": "fg-dms4rocketmq-event/src/fg_dms4rocketmq_event",
      "fg_kafkaopensource_event": "fg-kafkaopensource-event/src/fg_kafkaopensource_event",
      "fg_lts_event": "fg-lts-event/src/fg_lts_event",
      "fg_obss3_event": "fg-obss3-event/src/fg_obss3_event",
      "fg_smn_event": "fg-smn-event/src/fg_smn_event",
      "fg_timer_event": "fg-timer-event/src/fg_timer_event"
    },
    
    # package_dir={"": "src"},
    install_requires=REQUIRES,
    
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
