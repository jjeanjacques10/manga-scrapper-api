
from time import sleep
import boto3
import logging
import json

from src.app import process_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.resource('sqs')


queue = sqs.get_queue_by_name(QueueName='manga-queue')

while True:
    for message in queue.receive_messages():
        try:
            logger.info(message.body)
            process_message(json.loads(message.body))
        except Exception as e:
            logger.error(e)
        message.delete()
    logger.info("Waiting for messages...")
    sleep(5)
