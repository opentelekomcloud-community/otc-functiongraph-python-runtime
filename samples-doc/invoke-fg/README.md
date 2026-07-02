# Samples on how to invoke FunctionGraph functions

## Prerequisites

### Environment variables

| Environment variable   | Value                    |
| --------------------   | ------------------------ |
| ``OTC_SDK_PROJECTID`` | Project ID
| ``OTC_SDK_REGION``     | Region, default: "eu-de"
| ``OTC_SDK_AK``         | Access Key (*)
| ``OTC_SDK_SK``         | Secret Key

(*) with permission to invoke FunctionGraph.

### Deployed FunctionGraph

Deploy following FunctionGraph function using console:

* **Project** : ``OTC_SDK_PROJECTID`` (see above)
* **Region**: ``OTC_SDK_REGION`` (see above)
* **Name**: ``python-sample-invoke-function``
* **Runtime**: ``Python 3.10``
* **Version**: ``latest``
* **Application**: ``default``
* **Code:** see: [src-fg/index.py](./src-fg/index.py)

## Synchronous invocation

### Using Python urllib

**code:** [src/invokeSync_AKSK.py](./src/invokeSync_AKSK.py)

```bash
python3 invokeSync_AKSK.py
```

### Using Python requests

**code:** [src/invokeSync_AKSK_requests.py](./src/invokeSync_AKSK_requests.py)

```bash
python3 invokeSync_AKSK_requests.py
```

## ASynchronous invocation

### Using Python urllib

**code:** [src/invokeASync_AKSK.py](./src/invokeASync_AKSK.py)

```bash
python3 invokeASync_AKSK.py
```

### Using Python requests

**code:** [src/invokeASync_AKSK_requests.py](./src/invokeASync_AKSK_requests.py)

```bash
python3 invokeASync_AKSK_requests.py
```
