import discord
from discord import app_commands
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name="introduce",
        description= "Introduce Yourself!"
        )

    async def introduce(self, interation: discord.Interaction, name: str, age: int) -> None:
        await interation.response.send_message(
            f"My name is: {name} and my age is: {age}"
        )
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        test(bot),  
        guild=discord.Object(id=992966611797545030)
    )