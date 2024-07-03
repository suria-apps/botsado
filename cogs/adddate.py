import discord
from discord import app_commands
from discord.ext import commands

class Activity(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print("cog loaded")

    # @app_commands.command(name='chooseactivity', description='Choose an activity')
    # @app_commands.describe(person='Choose the person')
    # @app_commands.choices(person=[])


    async def fruit_autocomplete(interaction: discord.Interaction, current: str,) -> List[app_commands.Choice[str]]:
        fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        return [
            app_commands.Choice(name=fruit, value=fruit)
            for fruit in fruits if current.lower() in fruit.lower()
        ]