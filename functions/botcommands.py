# import boto3
# import os
# from boto3.dynamodb.conditions import Key
# import datetime
# from dotenv import load_dotenv

# load_dotenv()

# class MyCommands:
#     def __init__(self):
#         self.dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
#         self.table = self.dynamoDB.Table(os.getenv("DYNAMO_TABLE"))
#         self.partitionKey = 'Date'
#         self.birthday = False

#     def broadcast_message(self, message: str):
#         from oldbot import bot
#         today = datetime.date.today().strftime('%m/%d')
#         filtering_exp = Key(self.partitionKey).eq(today)
#         response = self.table.query(KeyConditionExpression=filtering_exp)['Items']
#         print(response)
#         for guild in bot.guilds:
#             for channel in guild.text_channels:
#                 if channel.permissions_for(guild.me).send_messages:
#                     try:
#                         channel.send(message)
#                     except Exception as e:
#                         print(f"Failed to send message to {channel.name} in {guild.name}: {e}")
#         print("Broadcast complete!")