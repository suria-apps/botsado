import boto3
from boto3.dynamodb.conditions import Key
import os
import datetime
import logging
from discord import SyncWebhook
from dotenv import load_dotenv

load_dotenv()

class Birthday:
    def __init__(self):
        self.dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamoDB.Table(os.getenv("DYNAMO_TABLE"))
        self.partitionKey = 'Date'
        self.birthday = False

    def today_activities(self):
        try:
            print("Getting todays activities...")
            today = datetime.date.today().strftime('%m/%d')
            filtering_exp = Key(self.partitionKey).eq(today)
            response = self.table.query(KeyConditionExpression=filtering_exp)['Items']
            if not response:
                logging.info("No Activity today...")
            else:
                logging.info("Brithday Alert...")
                global birthday
                self.birthday = True

        except Exception as error:
            logging.error(error)

    def birthday_celebration(self):
        if self.birthday == True:
            print("Celebrating...")
            webhook = SyncWebhook.from_url('https://discord.com/api/webhooks/1237097560922128415/FKYE6gWAErA-2CPeMlpIiN7hNmqz138ma2Pw3-wTtERTwRGYEzXZr3wYS39BTRTJP5TM')
            webhook.send(content='@everyone Birthday')
        else:
            print("No Birthday...")