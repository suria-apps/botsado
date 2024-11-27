import discord
from discord.ext import commands
import os
import boto3
from boto3.dynamodb.conditions import Key

    
class editUserInfoDropdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamoDB.Table(os.getenv("DYNAMO_USER_TABLE"))
        self.partitionKey = 'userID'

    @discord.app_commands.command(name="updateinfo", description="Choose what to update.")
    async def dropdown_and_text(self, interaction: discord.Interaction):
        # Step 1: Show a dropdown menu
        view = DropdownView(interaction.user)
        await interaction.response.send_message("Please select an option from the dropdown:", view=view, ephemeral=True)
    
class DropdownView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.user = user  # Store the user who initiated the command

        # Define the dropdown menu
        self.dropdown = discord.ui.Select(
            placeholder="Choose an option to modify ...",
            options=[
                discord.SelectOption(label="Likes", description="Update things you like."),
            ],
        )
        self.dropdown.callback = self.select_callback  # Attach the callback to the dropdown
        self.add_item(self.dropdown)  # Add dropdown to the view

    async def select_callback(self, interaction: discord.Interaction):
        try:
            # Ensure only the original user can interact
            if interaction.user != self.user:
                await interaction.response.send_message("This menu is not for you!", ephemeral=True)
                return

            # Confirm selection and send modal
            selected_value = self.dropdown.values[0]  # Access the selected value
            modal = TextInputModal(selected_value)
            await interaction.response.send_modal(modal)

        except Exception as e:
            # Log the error to the console for debugging
            print(f"Error in select_callback: {e}")
            await interaction.response.send_message("An error occurred while processing your request.", ephemeral=True)

class TextInputModal(discord.ui.Modal, title="Edit things you like."):
    def __init__(self, dropdown_value):
        self.dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamoDB.Table(os.getenv("DYNAMO_USER_TABLE"))
        self.partitionKey = 'userID'

        super().__init__()
        self.dropdown_value = dropdown_value
        self.text_input = discord.ui.TextInput(
            label="Your input, seperate with comma.",
            placeholder="Type here...",
            style=discord.TextStyle.short,
        )
        self.add_item(self.text_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            print(f"Modal submitted by {interaction.user}. Dropdown Value: {self.dropdown_value}, Input: {self.text_input.value}")
            new_items = str(self.text_input.value)
            key = {'userID': f"{str(interaction.user.id)}",
                   'globalName': f"{str(interaction.user.global_name)}"}
            if ',' in new_items:
                new_item = new_items.split()
                for item in new_item:
                    response = self.table.get_item(Key=key)
                    if 'Item' not in response:
                        # If the item does not exist, create it
                        print("Item not found, creating a new one.")

                    self.table.update_item(
                        Key=key ,
                        UpdateExpression="SET likes = list_append(likes, :item)",
                        ExpressionAttributeValues={
                            ':item': [item],
                        },
                        ReturnValues='UPDATED_NEW'
                    )
            else:
                response = self.table.get_item(Key=key)
                if 'Item' not in response:
                    # If the item does not exist, create it
                    print("Item not found, creating a new one.")

                self.table.update_item(
                    Key=key ,
                    UpdateExpression="SET likes = list_append(likes, :new_items)",
                    ExpressionAttributeValues={
                        ':new_items': [new_items],
                    },
                    ReturnValues='UPDATED_NEW'
                )
            await interaction.response.send_message(
                f"You selected: **{self.dropdown_value}** and entered: **{self.text_input.value}**", ephemeral=True
            )
        except Exception as e:
            print(f"Error in on_submit: {e}")
            await interaction.response.send_message("An error occurred while processing your input.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(editUserInfoDropdown(bot))