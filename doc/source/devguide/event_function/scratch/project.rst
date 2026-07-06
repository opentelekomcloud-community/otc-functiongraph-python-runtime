Setting up the Python project for event functions
==========================================================

The following examples assumes that you have Python 3.10 installed
you are using pip as the package manager and linux.


Creating a Python project
---------------------------------

Project structure
^^^^^^^^^^^^^^^^^^^^^^^^

A minimal Python FunctionGraph project is typically structured as follows:

.. code-block:: console
  :caption: Project structure

  /project-root
   ├─ src
   |  └─ index.py
   ├─ requirements.txt
   └─ Makefile


Sample code
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
  :caption: src/index.py

  # -*- coding:utf-8 -*-
  import json

  def initializer(context):
      logger = context.getLogger()
      logger.info(f"Function name: {context.getFunctionName()}")
      

  def handler (event, context):
      logger = context.getLogger()
      logger.info(f"Function name: {context.getFunctionName()}")
      return {
          "statusCode": 200,
          "isBase64Encoded": False,
          "body": json.dumps(event),
          "headers": {
              "Content-Type": "application/json"
          }
      }


requirements.txt
^^^^^^^^^^^^^^^^^^^^^^^^

The **requirements.txt** file is used to manage the dependencies of a Python
project. The following is a sample **requirements.txt** file:

.. code-block:: text
  :caption: requirements.txt

  requests==2.26.0


Makefile
^^^^^^^^^^^^^^^^^^^^^^^^

The **Makefile** is used to automate the build and deployment process of a
Python project. The following is a sample **Makefile**:


.. code-block:: make
  :caption: Makefile

  .PHONY: create_package
  create_package:
	  python3 ../../utils/createZip.py

(Adapt the above Makefile to your project structure and requirements.)


Deploying to FunctionGraph
---------------------------------

Create Zip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To upload the function code to FunctionGraph, you need to create package
of the project.

The directory structure of the zip package should be as follows:

.. code-block:: console
  :caption: Zip package structure

  /code.zip
   ├─ dependency_1           Python third-party dependencies (optional)
   |  └─ ...
   ├─ dependency_2           Python third-party dependencies (optional)
   |  └─ ...
   ├─ src
   |  └─ index.py            .py handler file (mandatory)
   └─ requirements.txt       Python project management file (mandatory)

You can use the following pip command to install the dependencies listed in
the **requirements.txt** file:

.. code-block:: console

  make create_package



Create FunctionGraph function in console
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Log in to the FunctionGraph console.
2. Click **Create Function** and select **Create from scratch**.
3. In **Basic Information**:
   "FunctionType": **Event Function**.
   "Region": select the region where you want to create the function.
   "Function Name**: enter a **python_sample** as name for the function.
   "Enterprise Project**: select **default**.
   "Runtime**: select the Python runtime version **Python 3.10**.
   "Agency": select **Use no agency**
4. Click **Create Function**.
5. Upload the created **code.zip** file to the function by
   clicking **Upload** > **Local ZIP**.

   The uploaded code will be automatically deployed on the
   FunctionGraph console.
   If you have modified the code, click **Deploy** again.

6. Modify the function handler:

   1. Click **Configuration** > **Basic Settings**.
   2. In the **Handler** field, enter the handler **src/index.handler**.
   3. Click **Save**.

7. Modify the initializer (if needed):

   1. Click **Configuration** > **Lifecycle**.
   2. enable **Initialization**
   3. In the **Function Initializer** field, enter the
      initializer **src/index.initializer**.
   4. Click **Save**.

Testing the function
^^^^^^^^^^^^^^^^^^^^^^^^

1. On the Code tab, click **Test**.
   In the Configure Test Event dialog box, create from **Blank Template** and set as:

    .. code-block:: json

       {
          "key": "value"
       }

2. Click **Create** to save the test event.
3. Click **Test** to test the function.
4. the Execution Result window is displayed on the right.
   You can check whether the function is executed successfully.

    .. image:: ./scratch_event_function_test.png
      :alt: Test Event Function

Function Execution Result Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The execution result consists of the function output, summary, and log output.

.. list-table::  Function execution result description
    :widths: 20 50 50
    :header-rows: 1

    * - Parameter
      - Successful Execution
      - Failed Execution

    * - Function output
      - The defined function output information is returned.
      - A JSON file that contains **errorMessage** and **errorType** is returned.
        The format is as follows:


        .. code-block:: json

          {
            "errorMessage": "error message",
            "errorType": "error type"
          }

        **errorMessage**: Error message returned by the runtime.
        **errorType**: Error type.

    * - Summary
      - **Request ID**, **Memory Configured**, **Execution Duration**,
        **Memory Used**, and **Billed Duration** are displayed.
      - **Request ID**, **Memory Configured**, **Execution Duration**,
        **Memory Used**, and **Billed Duration** are displayed.

    * - Log output
      - Function logs are printed. A maximum of 4 KB logs can be displayed.
      - Error information is printed. A maximum of 4 KB logs can be displayed.
