# doc-utils

## Create files for bundled libraries

Used to generate documentation files based on installed libraries
in backend.

Following files will be created in folder ``/doc/source/devguide/bundled_libraries``:

- _index.rst
- bundled_libraries_Python[VERSION].rst


To run, following environment variables must be set on client side:

- OTC_SDK_PROJECTID
- OTC_DOMAIN_NAME
- OTC_USER_NAME
- OTC_USER_PASSWORD

To create files use: 

```bash
cd doc-utils/src
python3 createLibraryDocs.py
```


This will 
- deploy for each python version a FunctionGraph function,
- calls this function to get the libraries
- creates the files for sphinx documentation
