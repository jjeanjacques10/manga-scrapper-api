import os
from time import sleep
import boto3
import json

from services.consumer_processor import process_message


class Consumer:

    def __init__(self) -> None:
        self.sqs = boto3.resource('sqs', region_name='us-east-1',
                                  endpoint_url=os.environ.get("SQS_ENDPOINT"))

    def start(self):

        queue = self.sqs.get_queue_by_name(QueueName='manga-queue')

        print("Checking for messages...")
        while True:
            for message in queue.receive_messages():
                try:
                    print(message.body)
                    process_message(json.loads(message.body))
                except Exception as e:
                    print(e)
                message.delete()
            # print("Waiting for messages...")
            sleep(5)
