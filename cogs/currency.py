import discord
from discord.ext import commands
import boto3
import os
from boto3.dynamodb.conditions import Key

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamoDB.Table(os.getenv("DYNAMO_USER_TABLE"))
        self.partitionKey = 'userID'

    @discord.app_commands.command(name='currency', description='Check to validate your coin.')
    async def currency(self, interaction: discord.Interaction):
        try:
            validated = Currency.validate(self, interaction.user.id, interaction.user.name, interaction.guild_id)
            await interaction.response.send_message(f"{validated}", ephemeral=True)
        except Exception as e:
            print(f"Error in on_submit: {e}")
            await interaction.response.send_message("An error occurred while processing your input.", ephemeral=True)
    
    
    def validate(self, userID, userGN, currentGuild):
        key = {'userID': str(userID), 'globalName': str(userGN)}
        try:
            response = self.table.get_item(Key=key)
            item = response.get('Item', {})
            if 'currency' not in item:
                new_dict = {
                    str(currentGuild): '100',
                }

                self.table.update_item(
                    Key=key,
                    UpdateExpression="SET currency = :new_dict",
                    ExpressionAttributeValues={
                        ':new_dict': new_dict
                    }
                )
                return 'Created, you start with 100 coin.'
            
        except Exception as e:
            return (f"Error in on_submit: {e}")

        return f" You have {response['Item']['currency'][str(currentGuild)]} coins"
async def setup(bot):
    await bot.add_cog(Currency(bot))

