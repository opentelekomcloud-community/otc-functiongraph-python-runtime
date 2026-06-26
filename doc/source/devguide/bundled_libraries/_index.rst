.. _bundled_libraries:

Bundled Libraries
========================

Bundled libraries can be used for **event** and **http** functions **build from scratch**.

If you want to use a different version of a runtime-included library,you can do this by bundling it with your function in your deployment package or by adding it as a dependency.

Following table lists the non-standard libraries integrated with Python, which can be directly declared and used in Python function code.

.. list-table:: Bundled libraries with **Python**
    :header-rows: 1

    * - Name
      - Usage
      - Version

    * - dateutil
      - Date and time processing
      - 2.6.0

    * - requests
      - HTTP library
      - 2.7.0

    * - httplib2
      - httpclient
      - 0.10.3

    * - numpy
      - Mathematical computation
      - 1.13.1

    * - redis
      - Redis client
      - 2.10.5

    * - obsclient
      - OBS client
      - \-

    * - smnsdk
      - SMN access
      - 1.0.1
