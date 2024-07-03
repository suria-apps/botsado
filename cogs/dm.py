import discord
from discord import app_commands
from discord.ext import commands

class dm(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="message",
        description= "Send a DM"
        )  
    
    async def message(self, interaction: discord.Interaction) -> None:
        await interaction.user.send("Hello")
        await interaction.response.send_message('Message sent')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        dm(bot),  
        guild=discord.Object(id=992966611797545030)
    )

# @commands.Cog.listener()
# async def on_ready(self):
#     print(f"{__name__} is ready")