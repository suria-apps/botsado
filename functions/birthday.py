import boto3
from boto3.dynamodb.conditions import Key
import os
import datetime
import logging
from discord import SyncWebhook
from dotenv import load_dotenv
# from functions.botcommands import MyCommands

load_dotenv()

class Birthday:
    def __init__(self):
        self.dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamoDB.Table(os.getenv("DYNAMO_TABLE"))
        self.partitionKey = 'Date'
        self.birthday = False

    async def broadcast_message(self, bot):
        today = datetime.date.today().strftime('%m/%d')
        filtering_exp = Key(self.partitionKey).eq(today)
        response = self.table.query(KeyConditionExpression=filtering_exp)['Items']
        target_guild = response[0]['Guild']
        target_channel = response[0]['Channel']
        
        for guild in bot.guilds:
            if str(guild.id) == target_guild:
                for channel in guild.text_channels:
                    if str(channel.id) == target_channel:
                    # if channel.permissions_for(guild.me).send_messages:
                        try:
                            await channel.send(f"Today is {response[0]['Date']} and it's {response[0]['Name']}'s Birthday!")
                        except Exception as e:
                            print(f"Failed to send message to {channel.name} in {guild.name}: {e}")
        print("Broadcast complete!")

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