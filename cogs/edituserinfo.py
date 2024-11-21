import discord
from discord.ext import commands
import os
import boto3
from boto3.dynamodb.conditions import Key

class EditUserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="edituserinfo", description="Edit your info for the bot")
    async def edituserinfo(self, interaction: discord.Interaction):
        pass