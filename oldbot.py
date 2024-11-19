import discord
from discord import SyncWebhook, app_commands, interactions
from discord.ext import commands, tasks
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import logging
import datetime as dt
import time
import threading
import datetime
import schedule 
from pytz import timezone
import asyncio
from functions.birthday import Birthday
import asyncio

birthday = False

GUILD_ID = 992966611797545030
BOT_TOKEN = os.getenv("DEV_BOT_TOKEN")
CHANNEL_ID = 1041141310914039829

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
print(datetime.datetime.now())
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

birthday_function = Birthday()

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


schedule.every().day.at("14:46").do(birthday_function.today_activities)
schedule.every().day.at("13:54").do(birthday_function.birthday_celebration)
# schedule.every().day.at("12:27").do(test2)

stop_run_continuously = run_continuously()

#############################################################

# birthday_function.today_activities()
# birthday_function.birthday_celebration()

# async def load():
#     for filename in os.listdir("./cogs"):
#         if filename.endswith(".py"):
#             #loads cogs and removes the .py from filename
#             await bot.load_extension(f"cogs.{filename[:-3]}")


async def periodic_broadcast():
    await bot.wait_until_ready()
    while True:
        print(birthday_function.birthday)
        if True:
            await birthday_function.broadcast_message(bot)
            birthday_function.birthday = False
        await asyncio.sleep(30)

async def main():
    await bot.start(BOT_TOKEN)

@bot.event
async def on_ready():
    print("bot up and running...")
    asyncio.create_task(periodic_broadcast())


@bot.tree.command(name='message', guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.user.send("Hello")
    await interaction.response.send_message('Message sent')

@bot.tree.command(name = "helloguild2", guild=discord.Object(id=GUILD_ID))
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}! SlashGUILD", ephemeral=True)

@bot.tree.command(name = 'addactivity', description="Add an activity for Lolo to remember", guild=discord.Object(id=GUILD_ID))
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

if __name__ == "__main__":
    asyncio.run(main())