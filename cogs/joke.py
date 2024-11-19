import discord
from discord.ext import commands

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="joke", description="Tells a joke")
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello from the cog!")
    
async def setup(bot):
    await bot.add_cog(Joke(bot))