.. _devguide_http_function_scratch_index:

Building FunctionGraph HTTP Functions with Python from scratch
==========================================================================

.. toctree::
   :hidden:

   Project <project>


Following chapter describes in short how to build FunctionGraph HTTP functions
using Python from scratch.

Introduction
------------

For general details about creating HTTP functions from scratch and
executing an HTTP function,
see :otc_docs:`Creating a Function from Scratch and Executing the Function <function-graph/umn/creating_a_function/creating_a_function_from_scratch/creating_an_http_function.html#functiongraph-01-1442>`
in the user manual.

Function Development Overview
------------------------------

See also :ref:`General Constraints for HTTP Functions <general_constraints_http>`

Step 1: Create a function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In FunctionGraph console, create a function with the following parameters:

- **Create with**: Create from scratch
- **Function Type**: HTTP Function
- **Region**: select the region where you want to create the function 
- **Function Name**: http-function-scratch

leave the other parameters with default values, and click **Create Function** to create the function.

Step 2: Write code for the function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For HTTP functions, the code is expected to listen for HTTP requests and send responses.
You can use any Python web framework or library to implement the function code.

The following is a sample code using Python built-in HTTP module.

In the code editor, replace the default code for file `index.py` with the following
code, and click **Deploy** to save the code.


.. literalinclude:: ../../../../../samples-doc/scratch-http/src/index.py
   :caption: index.py
    

Step 3: Configure the bootstrap file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A file named `bootstrap` is used to start the function runtime and execute the function code.

The following is the code to be added in the `bootstrap` file for Python runtime.
It starts the Python runtime and executes the `index.py` file.


.. code-block:: bash
   :caption: bootstrap

   /opt/function/runtime/[PYTHON_RUNTIME]/rtsp/python/bin/python $RUNTIME_CODE_ROOT/[FUNCTION_FILENAME]

where

* **[PYTHON_RUNTIME]** is the Python runtime to use (see :ref:`Supported Python Runtimes <SupportedPythonRuntimes>`).
* **$RUNTIME_CODE_ROOT** is the environment variable that points to the root directory of your function code
  (/opt/function/code).
* **[FUNCTION_FILENAME]** is the name of the file that contains your function code (e.g., `index.py`).

In the code editor, replace the default code for file `bootstrap` with the following
code, and click **Deploy** to save the code.

.. literalinclude:: ../../../../../samples-doc/scratch-http/bootstrap
   :caption: bootstrap  


Step 4: Create a test event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click on **Test** tab, and click **Configure Test Event** to create test events with the following parameters:

(For HTTP functions only "API Gateway (Dedicated)" event template is supported.)


For POST /

.. literalinclude:: ../../../../../samples-doc/scratch-http/resources/test_post.json
   :caption: test_post

For GET /

.. literalinclude:: ../../../../../samples-doc/scratch-http/resources/test_get.json
   :caption: test_get


Step 5: Test the function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click **Test** to execute the function with the test events created in the previous step,
and you should see the following output in the ``Execution Result`` section


For POST event:

.. code-block:: json
   :caption: Execution Result POST

    {
      "body": "eyJtZXNzYWdlIjogIkhlbGxvLCBXb3JsZCEifQ==",
      "headers": {
          "Date": [
              "Fri, 03 Jul 2026 09:16:00 GMT"
          ],
          "Server": [
              "BaseHTTP/0.6 Python/3.10.0"
          ]
      },
      "statusCode": 200,
      "isBase64Encoded": true
    }

The body in the output is base64 encoded. After decoding, you should see the following content:

.. code-block:: html

    {"message": "Hello, World!"} 


For GET event:

.. code-block:: json
   :caption: Execution Result GET

    {
        "body": "eyJtZXNzYWdlIjogIkhlbGxvLCBKb2huISJ9",
        "headers": {
            "Content-Type": [
                "application/json"
            ],
            "Date": [
                "Fri, 03 Jul 2026 09:17:28 GMT"
            ],
            "Server": [
                "BaseHTTP/0.6 Python/3.10.0"
            ]
        },
        "statusCode": 200,
        "isBase64Encoded": true
    }

The body in the output is base64 encoded. After decoding, you should see the following content:

.. code-block:: html

    {"message": "Hello, John!"} 

