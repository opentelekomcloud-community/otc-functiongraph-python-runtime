# Event-sdk-obs

Example on how to use OBS in FunctionGraph.



For reference see:

- [Object Storage Service 3rd Party - Python SDK](https://docs.otc.t-systems.com/object-storage-service-3rd-party/python-sdk/)

## Deploy to T Cloud Public FunctionGraph

### Deploy to FunctionGraph

Create following FunctionGraph function using FunctionGraph console:

Create function:
- Create with: **Create from scratch**
 - Function Type: **Event Function**
 - Region: **your region**
 - FunctionName: **py_obs_sample**
 - Enterprise Project: **default**
 - Runtime: **Python 3.10**
 - Agency: **specify an agency with OBS permissions**  
   (e.g. Permission `OBS Administrator`)


In **Code** tab, copy code from [src/index.py](./src/index.py) in code window and **Deploy**.

Configure function:

- `Basic Settings`
    - Handler: **index.handler**

- `Environment variables`
    - **ECS_ENDPOINT** = **https://ecs.eu-de.otc.t-systems.com**
  
Create any Test events.

### Test the Function

Click **Test**

