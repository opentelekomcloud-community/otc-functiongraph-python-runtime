# -*- coding:utf-8 -*-
import json
import pkg_resources

def handler (event, context):

    installed_packages = pkg_resources.working_set
    packages = []
    
    for package in installed_packages:
        packages.append({"package": package.key, "version": package.version})
        
    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps({"packages": packages}),
        "headers": {
            "Content-Type": "application/json"
        }
    }