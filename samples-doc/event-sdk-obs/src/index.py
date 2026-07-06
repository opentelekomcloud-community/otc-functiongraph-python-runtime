from obs import ObsClient

def handler(event, context):
    if ObsClient is None:
        raise RuntimeError("Missing dependency: obs (esdk-obs-python)")

    logger = context.getLogger()
    logger.info("Function name: %s", context.getFunctionName())
    
    ret = listBuckets(context)  # Call the listBuckets function to log available buckets
    
    return {
        "statusCode": ret.get("status"),
        "body": {            
            "buckets": ret.get("buckets", [])
        }
    }
        
    
    
def listBuckets(context):
    logger = context.getLogger()
    obs_endpoint = context.getUserData("OBS_ENDPOINT") or "https://obs.eu-de.otc.t-systems.com"  # Default endpoint if not provided
    obs_client = ObsClient(
        access_key_id=context.getSecurityAccessKey(),
        secret_access_key=context.getSecuritySecretKey(),
        security_token=context.getSecurityToken(),
        server=obs_endpoint,
    )

    try:
        response = obs_client.listBuckets()
        if response.status < 300:
            buckets = [bucket.name for bucket in response.body.buckets]
            logger.info("Buckets: %s", buckets)
            return {"buckets": buckets, "status": response.status}
        else:
            logger.error("Failed to list buckets: %s", response.errorMessage)
            return {"buckets": [], "status": response.status}
    except Exception as err:
        logger.error("Error in listBuckets: %s", err)
        return {"buckets": [], "status": 500}        
    finally:
        obs_client.close()    