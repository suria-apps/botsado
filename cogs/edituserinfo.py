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
                discord.SelectOption(label="Likes", description="Add things you like."),
                discord.SelectOption(label="Delete Likes", description="Remove things you like."),
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

            selected_value = self.dropdown.values[0]  # Access the selected value

            if selected_value == "Likes":
                modal = TextInputModal(selected_value)
                await interaction.response.send_modal(modal)
            elif selected_value == "Delete Likes":
                # Fetch the user's likes
                user_id = interaction.user.id
                global_name = interaction.user.name
                key = {'userID': f"{user_id}", 'globalName': f"{global_name}"}
                dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
                table = dynamoDB.Table(os.getenv("DYNAMO_USER_TABLE"))
                response = table.get_item(Key=key)
                item = response.get('Item', {})
                likes = item.get('likes', [])

                if not likes:
                    await interaction.response.send_message(
                        "You have no likes to delete.", ephemeral=True
                    )
                else:
                    view = DeleteLikesView(interaction, user_id, global_name, likes)
                    await interaction.response.send_message(
                        "Select a like to delete:", view=view, ephemeral=True
                    )
        except Exception as e:
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
                   'globalName': f"{str(interaction.user.name)}"}
            if ',' in new_items:
                new_item = new_items.split(',')
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
                f"You added **{self.text_input.value}** to the things you like.", ephemeral=True
            )
        except Exception as e:
            print(f"Error in on_submit: {e}")
            await interaction.response.send_message("An error occurred while processing your input.", ephemeral=True)

class DeleteLikesView(discord.ui.View):
    def __init__(self, interaction, user_id, global_name, likes):
        super().__init__(timeout=60)
        self.interaction = interaction
        self.user_id = user_id
        self.global_name = global_name
        self.likes = likes

        # Define the dropdown menu for selecting likes to delete
        self.dropdown = discord.ui.Select(
            placeholder="Choose an item to delete...",
            options=[discord.SelectOption(label=like) for like in likes],
        )
        self.dropdown.callback = self.on_dropdown_select
        self.add_item(self.dropdown)

    async def on_dropdown_select(self, interaction: discord.Interaction):
        try:
            selected_like = self.dropdown.values[0]
            print(f"User selected: {selected_like}")

            # Remove the selected like from the user's likes list in DynamoDB
            key = {
                'userID': f"{self.user_id}",
                'globalName': f"{self.global_name}"
            }
            likes = self.likes
            if selected_like in likes:
                index = likes.index(selected_like)
                dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
                table = dynamoDB.Table(os.getenv("DYNAMO_USER_TABLE"))
                table.update_item(
                    Key=key,
                    UpdateExpression=f"REMOVE likes[{index}]",
                    ReturnValues='UPDATED_NEW'
                )
                await interaction.response.send_message(
                    f"Removed: **{selected_like}** from your likes.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Selected item was not found in your likes.", ephemeral=True
                )
        except Exception as e:
            print(f"Error removing like: {e}")
            await interaction.response.send_message(
                "An error occurred while processing your request.", ephemeral=True
            )



async def setup(bot):
    await bot.add_cog(editUserInfoDropdown(bot))