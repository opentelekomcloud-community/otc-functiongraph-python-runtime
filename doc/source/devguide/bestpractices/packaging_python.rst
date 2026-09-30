.. _devguide_bestpractices_packaging_python:

Packaging Python functions created from scratch
===============================================================

.. toctree::
   :hidden:


FunctionGraph supports packaging Python functions as zip files.

This packaging method is suitable for both event and HTTP functions created from scratch.

To package your Python function as a zip file, you can use the provided `createZip.py` script and run it from the root of the project you want to package. The script will create a zip file in the `dist` folder including the function code and all dependencies:

.. literalinclude:: /../../utils/createZip.py
   :caption: :github_repo_master:`createZip.py <utils/createZip.py>`

