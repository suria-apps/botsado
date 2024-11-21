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
        self.table = self.dynamoDB.Table(os.getenv("DYNAMO_EVENT_TABLE"))
        self.partitionKey = 'date'
        self.birthday = False

    async def broadcast_message(self, bot):
        try:
            today = datetime.date.today().strftime('%m/%d')
            filtering_exp = Key(self.partitionKey).eq(today)
            response = self.table.query(KeyConditionExpression=filtering_exp)['Items']
            target_guild = response[0]['guildID']
            target_channel = response[0]['channelID']

            user = await bot.fetch_user(response[0]['userID'])
            
            for guild in bot.guilds:
                if str(guild.id) == target_guild:
                    for channel in guild.text_channels:
                        if str(channel.id) == target_channel:
                            try:
                                await channel.send(f"Today is {response[0]['date']} and it's {user.mention}'s Birthday!")
                            except Exception as e:
                                print(f"Failed to send message to {channel.name} in {guild.name}: {e}")
            self.birthday = False
            print("Broadcast complete!")
        except Exception as e:
            print(e)

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