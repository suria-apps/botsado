import discord
import os
from discord.ext import commands
from openai import OpenAI
import boto3
from boto3.dynamodb.conditions import Key
import random

client = OpenAI(
    api_key = os.getenv("OPEN_API_KEY"),
)

joke_messages = [
    {"role": "system", "content": "You are a comedian. Very casual and raw"},
    ]


class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamoDB.Table(os.getenv("DYNAMO_USER_TABLE"))
        self.partitionKey = 'userID'

    @discord.app_commands.command(name="joke", description="Tells a joke")
    async def joke(self, interaction: discord.Interaction):
        user = str(interaction.user.id)
        # print(interaction.user.global_name)

        filterQuery = Key(self.partitionKey).eq(user)
        response = self.table.query(KeyConditionExpression=filterQuery)['Items']
        list = response[0]['likes']
        random_preference = random.choice(list)

        joke_messages.append({"role": "user", "content": f"Tell me a unique joke, I like {random_preference}! Don't say 'Sure Thing' just say the joke and leave a space after the question."})
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Specify the model
            messages=joke_messages,
            temperature=0.9,
            max_tokens=150
            )
        joke = (completion.choices[0].message.content.strip())
        joke_messages.append({"role": "assistant", "content": joke})

        await interaction.response.send_message(joke, delete_after=1800)
    
async def setup(bot):
    await bot.add_cog(Joke(bot))