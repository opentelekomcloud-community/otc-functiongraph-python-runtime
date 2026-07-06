.. _event-sdk-obs:

event-sdk-obs
-------------------

Example on how to use OBS in FunctionGraph.

Source code for this sample can be found on :github_repo_master:`GitHub <samples-doc/event-sdk-obs>`.

For reference see:

- `Object Storage Service 3rd Party - Python SDK <https://docs.otc.t-systems.com/object-storage-service-3rd-party/python-sdk/>`_

Deploy to T Cloud Public FunctionGraph
======================================

Create following FunctionGraph function using FunctionGraph console:

Create function:
""""""""""""""""""

- Create with: **Create from scratch**
- Function Type: **Event Function**
- Region: **your region** (e.g. eu-de)
- FunctionName: **py_obs_sample**
- Enterprise Project: **default**
- Runtime: **Python 3.10**
- Agency: **specify an agency with OBS permissions**  
  (e.g. Permission `OBS Administrator`)


In **Code** tab, copy code following code snippet into the code window. 


.. literalinclude:: ../../../../samples-doc/event-sdk-obs/src/index.py
   :caption: index.py
   :language: python
   :tab-width: 2


and click **Deploy**.

Configure function:
""""""""""""""""""""

- `Basic Settings`

   - Handler: **index.handler**

- `Environment variables`

   - **ECS_ENDPOINT** = **https://ecs.eu-de.otc.t-systems.com**
  


Test the Function
""""""""""""""""""""

- Create any Test events.

- Click **Test**

