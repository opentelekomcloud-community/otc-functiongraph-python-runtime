Invoke FunctionGraph Function from FunctionGraph using Temporary Credentials
=============================================================================

.. toctree::
   :maxdepth: 1
   :hidden:


This page demonstrates how to call a FunctionGraph implemented
in Python from another FunctionGraph function using API calls and
**temporary security credentials** (SecurityAccessKey/SecurityKey/SecurityToken)
provided by an agency of `Agency Type` **Cloud Service** 
for `Cloud Service` **FunctionGraph Service** with permission to invoke FunctionGraph.
for authentication.

Using temporary credentials the request has to be signed using the
`otc-api-sign-sdk-python <https://github.com/opentelekomcloud-community/otc-api-sign-sdk-python>`_. 

See: :ref:`invoke_functiongraph_function_api` for more details on
how to use the REST API.


Prerequisites
-----------------

1. URN of Function to be called.
   In this example the code of the function to be called is:

   .. literalinclude:: ../../../../samples-doc/invoke-fg2fg/src-fg/index.py
      :language: python
      :caption: :github_repo_master:`samples-doc/invoke-fg2fg/src-fg/index.py <samples-doc/invoke-fg2fg/src-fg/index.py>`

   .. note::
      Ensure that the function and the subfunction are created in the same region.   

2. An agency of `Agency Type` **Cloud Service** for `Cloud Service` **FunctionGraph Service**
   with permission to invoke FunctionGraph.

   The permission policy should contain following policy statement:

   .. code-block:: json

      {
        "Version": "1.1",
        "Statement": [
          {
            "Action": [
              "functiongraph:function:invokeAsync*",
              "functiongraph:function:invoke"
              ],
            "Effect": "Allow"
          }
        ]
      }

   or use an agency with default permission **FunctionGraph CommonOperations**.

   .. note::
      The permissions shown above are for demonstration purpose.
      Please follow the principle of least privilege when creating 
      the permission policy for the agency.

      e.g. to grant permission to invoke only specific functions,
      the policy statement should be like:

      .. code-block:: json

         {
           "Version": "1.1",
           "Statement": [
             {
               "Action": [
                 "functiongraph:function:invokeAsync*",
                 "functiongraph:function:invoke"
                 ],
               "Effect": "Allow",
               "Resource": [
                 "RESOURCE_PATH"           
               ]
             }
           ]
         }

      where **"RESOURCE_PATH"** is in format

      .. code-block:: text

          FunctionGraph:::function:group/function name

      By adding Function name to the end of the generated prefix,
      you can define a specific path.
      
      An asterisk * is allowed to indicate any function.
      
      For example, **FunctionGraph:*:*:function:default/*** indicates
      any function in the **default** group.

      For more details, see :docs_otc:`Policy Syntax<identity-access-management/umn/user_guide/permissions/policy_syntax.html>` in Identity and Access Management User Guide.

      (Remark: changing the permission policy may take some time to take effect.)


Coding
---------------------

index.py
^^^^^^^^^^^^^^^^^^^^^^

Create a function with following content to call another FunctionGraph function:

.. literalinclude:: ../../../../samples-doc/invoke-fg2fg/src/index.py
   :language: python
   :caption: :github_repo_master:`samples-doc/invoke-fg2fg/src/index.py <samples-doc/invoke-fg2fg/src/index.py>`

Deployment
---------------------

Create a deployment package using **make create-package** command
and deploy the package to FunctionGraph using the console as 
event function from scratch using Python 3.10.


Configure the function:

- set the handler name as **index.handler**.
- specify an agency with permission to **invoke** FunctionGraph
- and set the URN of the function to be called as Environment variable
  with key **CALL_FG_URN**.

Testing
----------

Create a test event based on Blank Template and click **Test**. 

Execution Result on the right should show a successful execution and the function set in the **CALL_FG_URN** environment variable should have a new invoke request in its Monitoring.

