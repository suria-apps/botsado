import discord
from discord import SyncWebhook, app_commands, interactions
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

GUILD_ID = 992966611797545030
BOT_TOKEN = 'MTI1NDY1MjY2ODYzNTI1NDc4NA.Gb3htq.-TsbiJKWyj_xXWal83pAJA9g0EEI1DCtAf3UsI'
CHANNEL_ID = 1041141310914039829

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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

schedule.every().day.at("03:38").do(today_activities)
schedule.every().day.at("03:38").do(birthday_celebration)

stop_run_continuously = run_continuously()

#############################################################

# today_activities()
# birthday_celebration()

@bot.event
async def on_ready():
    print("bot up and running...")

@bot.tree.command(name = "helloguild2", guild=discord.Object(id=GUILD_ID))
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}! SlashGUILD", ephemeral=True)

@bot.tree.command(name = 'addactivity', description="Add an activity for Lolo to rememberwhat?", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(the_date = "What is the date of the event")
async def speak(interaction: discord.Interaction, the_date: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{the_date}'")
    print(the_date)

@bot.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 200802844075491328:
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print('Command tree synced.')
        await interaction.response.send_message('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')


bot.run(BOT_TOKEN)