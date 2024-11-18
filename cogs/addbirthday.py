from typing import Any
import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import boto3
load_dotenv()


#AWS INFO
###########################################
table = os.getenv("DYNAMO_TABLE")
dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamoDB.Table(table)
partitionKey = 'Date'
###########################################

discord_members = {}

class dropdownMembers(discord.ui.Select):
    def __init__(self, guild_id, user):

        # self.targetMember = None
        self.guild_id = guild_id
        self.user = user
        self.members = discord_members[self.guild_id]

        options=self.members
        


        super().__init__(placeholder="Choose a person.", options=options, min_values=1, max_values=1)   
    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_message(f'{self.user} chose {self.values[0]}.', delete_after=20)
        # self.targetMember = self.values[0]
        self.children[0].disabled = True
        activity_selection = dropdownActivity()
        self.add_item(activity_selection)


        

#Dropdown needs this viewclass
class dropdownMembersAndActivityView(discord.ui.View):
    def __init__(self, guild_id, user):
        super().__init__()
        self.guild_id = guild_id
        self.user = user
        print(f"HELLO {self.guild_id}")
        print(self.user)
        self.add_item(dropdownMembers(self.guild_id,self.user))
        # self.add_item(dropdownActivity())

class dropdownActivity(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label='Birthday')
        ]

        super().__init__(placeholder="Choose an activity.", options=options, min_values=1, max_values=1)
    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_message(f"A {self.values[0]}", delete_after=20)

# class dropdownActivityView(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.add_item(dropdownActivity())

class addbirthday(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.guildId = None
    
    @commands.command(name="date", description= "Add date")
    async def date(self, interation: discord.Interaction, month: int, day: int) -> None:
        date = f"{month}/{day}"
        await interation.response.send_message(f"Date is: {date}")
        return date

    @app_commands.command(
        name="addbirthday",
        description= "Add the date of someones birthday for Lolo to remember and remind you."
        )
    async def addbirthday(self, interaction: discord.Interaction) -> None:
        dictList = []
        print(dictList)
        guild = interaction.guild
        self.user = interaction.user
        print(self.user)
        self.guildId = interaction.guild.id
        print(self.guildId)
        for guild in self.bot.guilds:
            print(len(guild.members))
            if self.guildId in discord_members and len(guild.members) == len(discord_members[self.guildId]):
                print('guild in dict')
                pass
            else:
                print('guild not in dict')
                for member in guild.members:
                    dictList.append(discord.SelectOption(label=member.name))
                discord_members[self.guildId] = dictList
        print(dictList)
        print(discord_members)
        print(f'here {len(discord_members[self.guildId])}')
        await interaction.channel.send("Pick a member", view=dropdownMembersAndActivityView(self.guildId, self.user), delete_after=20)
        # await interaction.channel.send("Pick an activity", view=dropdownActivityView(), delete_after=20)
        await interaction.response.send_message('Added', silent=True)
        print(self.guildId)

        return self.guildId
    


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err, interaction: discord.Interaction):
        ss = self.get(self.bot.guilds, id=interaction.guild)
        report = self.get(ss.text_channels, id=interaction.guild)
        embed = discord.Embed(title='An Error has occurred', description=f'Error: \n `{err}`', timestamp=ctx.message.created_at, color=242424)
        await report.send(embed=embed)
        print(err)



        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        addbirthday(bot),  
        guild=discord.Object(id=992966611797545030)
    )

# @commands.Cog.listener()
# async def on_ready(self):
#     print(f"{__name__} is ready")

# @commands.Cog.listener()
# async def on_command_error(self, ctx, err):