
import os
from time import sleep
import boto3
import json

from src.app import process_message

sqs = boto3.resource('sqs', endpoint_url=os.environ.get("SQS_ENDPOINT"))
#sqs = boto3.resource('sqs', endpoint_url='http://localhost:4576', region_name='us-east-1', aws_access_key_id='admin', aws_secret_access_key='admin')

queue = sqs.get_queue_by_name(QueueName='manga-queue')

while True:
    for message in queue.receive_messages():
        try:
            print(message.body)
            process_message(json.loads(message.body))
        except Exception as e:
            print(e)
        message.delete()
    print("Waiting for messages...")
    sleep(5)
