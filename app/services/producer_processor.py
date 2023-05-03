import logging
import os
import boto3
import json

sqs = boto3.resource('sqs', region_name='us-east-1',
                     endpoint_url=os.environ.get("SQS_ENDPOINT"))

logging.basicConfig(level=logging.DEBUG)


def send_message(message):
    try:
        # Retrieving a queue by its name
        queue = sqs.get_queue_by_name(QueueName='manga-queue')

        # Create a new message
        response = queue.send_message(MessageBody=json.dumps(message))

        # The response is not a resource, but gives you a message ID and MD5
        logging.info("MessageId created: {0}".format(
            response.get('MessageId')))
    except Exception as e:
        logging.error(e)
