Dependencies for Python functions
====================================

This section describes how to create dependencies for Python functions in FunctionGraph.

Example
--------

Before creating a dependency, ensure that Python matching the function runtime
has been installed in the environment.

The following uses **Python 3.10** as an example to describe how to create a **fg_events** dependency package.

1. Create a directory for your function and navigate to it.
 
  .. code-block:: bash

        # Create a directory for your function
        mkdir dependency-fg-events
        cd dependency-fg-events

2. Create a **requirements.txt** file and add dependencies.

    .. literalinclude:: ../../../../../samples-doc/dependency-fg-events/requirements.txt
       :language: text
       :caption: :github_repo_master:`requirements.txt <samples-doc/dependency-fg-events/requirements.txt>`
       :tab-width: 2

3. Create zip file using :github_repo_master:`createZip.py <utils/createZip.py>`.

    .. code-block:: bash

        python3 createZip.py 

4. Deploy the dependency package to FunctionGraph as described in :otc_fg_umn:`Configuring Dependency Packages <configuring_dependencies/configuring_dependency_packages.html>`


Full example for fg-events dependency package
------------------------------------------------

This example deploys :github_repo_master:`fg_events <fg-events>` dependency packages for Python all runtime versions using Terraform.

Additionally, a simple timer event function using the dependency is deployed.

For code, see :github_repo_master:`samples-doc/dependency-fg-events <samples-doc/dependency-fg-events>` directory.
