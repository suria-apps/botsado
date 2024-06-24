import discord
from discord import SyncWebhook
from discord.ext import commands, tasks
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import logging
import datetime as dt
import time
import requests
import threading
import datetime
import schedule 
from pytz import timezone

birthday = False

##LOGGING
##########################################
LOG_FILE = os.getcwd() + "/logs"
if not os.path.exists(LOG_FILE):
    os.makedirs(LOG_FILE)
LOG_FILE = LOG_FILE + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d %H_%M_%S') + ".log"
logFormatter = logging.Formatter("%(levelname)s %(asctime)s %(processName)s %(message)s")
fileHandler = logging.FileHandler("{0}".format(LOG_FILE))
fileHandler.setFormatter(logFormatter)
rootLogger = logging.getLogger()
rootLogger.addHandler(fileHandler)
rootLogger.setLevel(logging.INFO)

logging.info("testing out the logging functionality")
###########################################

#AWS INFO
###########################################
dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamoDB.Table('Lolo-Botsado-BDDate')
partitionKey = 'Date'
###########################################

def today_activities():
    try:
        print("Getting todays activities...")
        today = datetime.date.today().strftime('%m/%d')
        filtering_exp = Key(partitionKey).eq(today)
        response = table.query(KeyConditionExpression=filtering_exp)['Items']
        if not response:
            logging.info("No Activity today...")
        else:
            for activity in response:
                logging.info("Brithday Alert...")
                global birthday
                birthday = True

    except Exception as error:
        logging.error(error)

BOT_TOKEN = 'OTkyOTY1MzA1NTg2NDI1ODk3.GWWz--.3VHxW-PaL8OWBYxbMR0J74z3pLiyDp7A2PGPYE'
CHANNEL_ID = 1041141310914039829

# birthdayList = ['04/22', '04/02', '05/06', '06/16']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

######## DATE
# try:

# except Exception:
#     logging.exception(Exception)

# date = datetime.date.today().strftime('%m/%d')
# print(type(date))

# def today():
#     try:
#         global today_date
#         today_date = datetime.date.today().strftime('%m/%d')
#         print("Today is:", today_date)
#         for i in birthdayList:
#             if i == today_date:
#                 print("Brithday Alert...")
#                 global birthday
#                 birthday = True
#             else: 
#                 pass
#     except Exception as error:
#         logging.error(error)
        
#     print(birthday)
def birthday_celebration():
    if birthday == True:
        print("Celebrating...")
        webhook = SyncWebhook.from_url('https://discord.com/api/webhooks/1237097560922128415/FKYE6gWAErA-2CPeMlpIiN7hNmqz138ma2Pw3-wTtERTwRGYEzXZr3wYS39BTRTJP5TM')
        webhook.send(content='@everyone Birthday')
        stop_run_continuously.set()
    else:
        print("No Birthday...")
        stop_run_continuously.set()


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

# schedule.every().day.at("03:22").do(today_activities)
# schedule.every().day.at("03:22").do(birthday_celebration)

stop_run_continuously = run_continuously()

############# 

today_activities()
birthday_celebration()

@bot.event
async def on_ready():
    print("bot up and running...")

@bot.command()
async def date(ctx):
    await ctx.send(today_date)

bot.run(BOT_TOKEN)