from typing import Any
import discord
from discord import app_commands
from discord.ext import commands

discord_members = {}

class dropdown(discord.ui.Select):
    def __init__(self):
        a = addactivities(bot=self)

        print(a.guildId)
        options=[]

        super().__init__(placeholder="Choose a person.", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_message(f'You chose {self.values[0]}.', delete_after=20)

#Dropdown needs this viewclass
class dropdownView(discord.ui.View):
    def __init__(self, timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(dropdown())

class addactivities(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.guildId = ''

    @app_commands.command(
        name="addactivity",
        description= "Add an activity for Lolo to remember and remind you."
        )
    async def addactivity(self, interaction: discord.Interaction) -> None:
        # guild = self.bot.get_guild(992966611797545030)
        dictList = []
        print(dictList)
        guild = interaction.guild
        self.guildId = interaction.guild.id
        print(self.guildId)
        for guild in self.bot.guilds:
            for member in guild.members:
                # discord_members[""]
                dictList.append(discord.SelectOption(label=member.name))
        discord_members[self.guildId] = dictList
        print(dictList)
        print(discord_members)
        await interaction.channel.send("Pick a member", view=dropdownView(), delete_after=20)
        await interaction.response.send_message('Added', silent=True)
        print(self.guildId)
        return self.guildId
    
    # @classmethod
    # async def getguild(self, interaction: discord.Interaction) -> None:


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
        addactivities(bot),  
        guild=discord.Object(id=992966611797545030)
    )

# @commands.Cog.listener()
# async def on_ready(self):
#     print(f"{__name__} is ready")

# @commands.Cog.listener()
# async def on_command_error(self, ctx, err):