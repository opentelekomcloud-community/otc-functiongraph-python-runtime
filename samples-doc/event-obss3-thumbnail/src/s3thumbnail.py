import json
from io import BytesIO

from PIL import Image
from fg_obss3_event import OBSS3Event


from obs import ObsClient
from obs import GetObjectRequest

def handler(event, context):
    if ObsClient is None:
        raise RuntimeError("Missing dependency: obs (esdk-obs-python)")

    logger = context.getLogger()

    logger.info("Function name: %s", context.getFunctionName())
    logger.info("Event received: %s", event)

    obs_event = OBSS3Event(event)
    records = obs_event.get_records()
    if not records:
        logger.info("No OBS records found in event.")
        return None

    src_bucket = records[0].get_s3().get_bucket().get_name()
    src_key = records[0].get_s3().get_object().get_key()

    obs_endpoint = context.getUserData("OBS_ENDPOINT")
    dest_bucket = context.getUserData("OUTPUT_BUCKET")
    dest_key = f"thumb-{src_key}"

    logger.info("Source bucket: %s", src_bucket)
    logger.info("Source key: %s", src_key)
    logger.info("Destination bucket: %s", dest_bucket)
    logger.info("Destination key: %s", dest_key)
    logger.info("OBS Endpoint: %s", obs_endpoint)

    if "." not in src_key:
        logger.info("Could not determine the image type.")
        return None

    image_type = src_key.rsplit(".", 1)[1].lower()
    if image_type not in ("jpg", "png"):
        logger.info("Unsupported image type: %s", image_type)
        return None

    obs_client = ObsClient(
        access_key_id=context.getSecurityAccessKey(),
        secret_access_key=context.getSecuritySecretKey(),
        security_token=context.getSecurityToken(),
        server=obs_endpoint,
    )

    try:
        shrink(obs_client, logger, src_bucket, src_key, dest_bucket, dest_key)
    except Exception as err:
        logger.info("Error in shrink: %s", err)
        raise
    finally:
        obs_client.close()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "isBase64Encoded": False,
        "body": json.dumps(event),
    }


def shrink(obs_client, logger, src_bucket, src_key, dest_bucket, dest_key):

    getObjectRequest = GetObjectRequest()
    getObjectRequest.content_type = "application/octet-stream"

    resp = obs_client.getObject(
        bucketName=src_bucket,
        objectKey=src_key,
        getObjectRequest=getObjectRequest,
        loadStreamInMemory=True,
    )

    if resp.status >= 300:
        logger.info("Failed to retrieve the object. Status code: %s", resp.status)
        return

    logger.info("Object retrieved successfully.")

    resized_image_buffer = _resize_image(resp.body.buffer)

    put_result = obs_client.putObject(
        bucketName=dest_bucket, objectKey=dest_key, content=resized_image_buffer
    )

    if put_result.status < 300:
        logger.info("Thumbnail created and uploaded successfully.")
    else:
        logger.info(
            "Failed to upload the thumbnail. Status code: %s", put_result.status
        )


def _resize_image(content_buffer):
    with Image.open(BytesIO(content_buffer)) as image:
        image = image.resize((100, 100))
        output = BytesIO()
        save_format = image.format or "JPEG"
        image.save(output, format=save_format)
        return output.getvalue()
