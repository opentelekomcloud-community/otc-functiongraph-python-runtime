.. _building_with_python:

Building with Python
========================
.. toctree::
   :hidden:
   :maxdepth: 1

   Setup Development Environment <dev_environment/_index>
   Event Function<event_function/_index>
   HTTP Function<http_function/_index>
   Invoke FunctionGraph <invoke/_index>
   Bundled Libraries <bundled_libraries/_index>

FunctionGraph Types
-------------------

FunctionGraph provides 2 types of functions:

* **Event Functions**

  Event functions can be configured with event triggers and integrate
  a variety of products
  (such as object storage service OBS, distributed messaging service
  DMS, cloud log service LTS, etc.).

  See :doc:`Event Functions <event_function/_index>`

* **HTTP Functions**

  HTTP functions support mainstream Web application frameworks and can
  be accessed through a browser or called directly by a URL.

  See :doc:`HTTP Functions <http_function/_index>`

Both types of functions can be built either from **scratch** or by
using **container images**.


Building from scratch
----------------------


Supported Python Runtimes for building from scratch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

FunctionGraph currently supports the following Python runtimes
for building functions from scratch:

.. _SupportedPythonRuntimes:

.. list-table:: Supported Python runtimes
   :header-rows: 1
  
   * - Runtime
     - Identifier
     - Python compilation environment (http functions)

   * - Python 2.7
     - Python2.7
     - /opt/function/runtime/python2.7/rtsp/python/bin/python

   * - Python 3.6
     - Python3.6
     - /opt/function/runtime/python3.6/rtsp/python/bin/python3
     
   * - Python 3.9
     - Python3.9
     - /opt/function/runtime/python3.9/rtsp/python/bin/python3

   * - Python 3.10
     - Python3.10
     - /opt/function/runtime/python3.10/rtsp/python/bin/python3

   * - Python 3.12
     - Python3.12
     - /opt/function/runtime/python3.12/rtsp/python/bin/python3
   

   

For supported runtimes see also: :otc_fg_umn:`Runtimes <service_overview/product_features.html>` in User Guide.

.. note:: 

   If you need newer Python runtimes, use custom container images
   to build your functions.
   
   For more information, see 

   - :ref:`devguide_event_function_container_index`
   - :ref:`devguide_http_function_container_index`

Bundled third-party components integrated in the Python runtime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For bundled libraries integrated in the Python runtime, 
see :doc:`Bundled Libraries <bundled_libraries/_index>`.


Building using container images
--------------------------------


Supported Python Runtimes for building using container images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For building functions using container images, you can use any
Python version that meets the requirements of your custom container image.
