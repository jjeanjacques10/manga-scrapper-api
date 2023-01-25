
import os
from time import sleep
import boto3
import json

from src.gateway.consumer.consumer_processor import process_message

sqs = boto3.resource('sqs', endpoint_url=os.environ.get("SQS_ENDPOINT"))

queue = sqs.get_queue_by_name(QueueName='manga-queue')

print("Checking for messages...")
while True:
    for message in queue.receive_messages():
        try:
            print(message.body)
            process_message(json.loads(message.body))
        except Exception as e:
            print(e)
        message.delete()
    #print("Waiting for messages...")
    sleep(5)
