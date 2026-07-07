# coding: utf-8

from fg_dds_event import DDSEvent


def handler(event, context):
  logger = context.getLogger()

  logger.info("Function Name: %s", context.getFunctionName())

  dds_event = DDSEvent(event)
  
  
  records = dds_event.get_records()
  logger.info("DDS Event- Number of records: %s", len(records))

  for index, record in enumerate(records):
    logger.info("DDS Event- Record %d: %s", index + 1, record)
  
  output = {
    "record_count": len(records),
  }
	
  return output
