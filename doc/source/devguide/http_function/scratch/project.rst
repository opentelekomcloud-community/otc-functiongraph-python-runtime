Setting up the Python project for HTTP functions
==========================================================

.. toctree::
   :hidden:

The following examples assumes that you have Python 3.10 installed
you are using linux as operating system.

Project structure
^^^^^^^^^^^^^^^^^^^^^^^^

A minimal Python FunctionGraph project is typically structured as follows:

.. code-block:: bash
  :caption: Project structure

  /project-root
   ├─ src
   |  └─ index.py
   └─ requirements.txt

Step 1: Initialize the project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This project will use Flask, a popular Python web framework, 
to implement the HTTP function.

1. Run the following commands to create a project folder.

   .. code-block:: bash

      mkdir -p scratch-http-simple/src
      cd scratch-http-simple

2. Run the following command to create a virtual environment for the project.

    .. code-block:: bash
  
       # create a virtual environment named .venv in the project root directory
       python3 -m venv .venv

       # activate the virtual environment with the following command:
       source .venv/bin/activate


3. create a file named **requirements.txt** in the project root directory and add the following line to specify Flask as a dependency.

   .. literalinclude:: ../../../../../samples-doc/scratch-http-flask/requirements.txt
      :caption: requirements.txt

4. Run the following command to install the dependencies specified in **requirements.txt**.

   .. code-block:: bash

      pip install -r requirements.txt
      

Step 2: Sample code
^^^^^^^^^^^^^^^^^^^^^^^^

in the src folder, create a file named **index.py** and add the following code.
For details about how to use this framework, see `Flask's guide <https://flask.palletsprojects.com/en/2.0.x/>`_ .

Sample code:

.. literalinclude:: ../../../../../samples-doc/scratch-http-flask/src/index.py
    :language: python
    :caption: src/index.py
    :tab-width: 2

Step 2a: Test the function locally

To test the function locally, run the following command in the project root directory:

.. code-block:: bash

   python3 src/index.py

Then send a HTTP request to the function with the following command:

.. code-block:: bash
  :caption: GET request

   curl -X GET localhost:8000/index

.. code-block:: json
   :caption: Result


   {"message":"Hello from scratch-http sample!"}

.. code-block:: bash
  :caption: POST request

    curl -X POST localhost:8000/index

.. code-block:: json
   :caption: Result

    {"body":"\"/index success\"","headers":{"Content-Type":"application/json"},"isBase64Encoded":false,"statusCode":200}


Step 3: Create the bootstrap file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a file named **bootstrap** in the project root directory and add the following code.

.. literalinclude:: ../../../../../samples-doc/scratch-http-flask/bootstrap
    :language: bash
    :caption: bootstrap
    :tab-width: 2

Step 4: Create package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To deploy the function to FunctionGraph, you need to create a zip package of the project.
The Zip package should have following structure:

.. code-block:: bash
  :caption: deployment zip file structure

  /code.zip
   ├─ requirement 1           # NPM third-party dependencies (optional)
   |  └─ ...
   ├─ src
   |  └─ index.py            # main function code file (mandatory)
   └─ bootstrap              # bootstrap file to start the function runtime (mandatory)
   

To create the zip package, you use makefile file as 
follows to include the necessary fields for FunctionGraph deployment.

.. literalinclude:: ../../../../../samples-doc/scratch-http-flask/Makefile
    :language: make
    :caption: Makefile
    :tab-width: 2

To create the zip package, run the following command in the project root directory:

.. code-block:: bash

   make create_package

This will create a zip package named **code.zip** in the **dist** directory.

Step 5: Deploy to FunctionGraph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In FunctionGraph console, create a function with the following parameters:

- **Create with**: Create from scratch
- **Function Type**: HTTP Function
- **Region**: select the region where you want to create the function 
- **Function Name**: scratch-http-simple

leave the other parameters with default values, and click **Create Function** to create the function.

In the **Code** tab of the created function, click **Upload** -> **local Zip**
to upload the generated zip package (e.g., `code.zip`) to FunctionGraph.


Step 6: Test the Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 

Test GET /index
!!!!!!!!!!!!!!!!

Create a test event with the following parameters:

- **Event Name**: test-event-get
- **Event Template**: API Gateway (Dedicated)

.. literalinclude:: ../../../../../samples-doc/scratch-http-flask/resources/apig_get_index.json
   :caption: apig_get_index.json 




Test POST /index
!!!!!!!!!!!!!!!!

Create a test event with the following parameters:

- **Event Name**: test-event-post
- **Event Template**: API Gateway (Dedicated)

.. literalinclude:: ../../../../../samples-doc/scratch-http-flask/resources/apig_post_index.json
   :caption: apig_post_index.json 
