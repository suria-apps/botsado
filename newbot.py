import discord
from discord import app_commands
from discord.ext import commands, tasks
import os
import asyncio

id = 200802844075491328

class myBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
        )
    
    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f"cogs.{filename[:-3]}")
        await bot.tree.sync(guild=discord.Object(id=992966611797545030))
    
    async def on_ready(self):
        # guild = bot.get_guild(992966611797545030)
        print(f'{self.user} has connected')
        #your_loop_name.start()
        print("hello")
        # print(guild.fetch_members(limit=None))
        # for guild in bot.guilds:
        #     for member in guild.members:
        #         print(member)
        # print("eeee")
    

# a = "aaa"
# b = "bbb"


# @tasks.loop(seconds=10)
# async def your_loop_name():
#     global a, b
#     print(a)
#     print(b)
#     if a != b:
#         # You can put everything here, this is just an example
#         user = bot.get_user(id)
#         await user.send('a is not equal to b')
#     else:
#         pass


    # async def message(self):
    #     user = await bot.fetch_user(id)
    #     await bot.loop.create_task(user.send("Hello"))
    #     print('send')

async def main():
        # asyncio.create_task(message())
    async with bot:
        await bot.start('MTI1NDY1MjY2ODYzNTI1NDc4NA.Gb3htq.-TsbiJKWyj_xXWal83pAJA9g0EEI1DCtAf3UsI')
        
# async def message():
#     user = await bot.fetch_user(id)
#     await bot.loop.create_task(user.send("Hello"))
#     print('send')

# async def message():
#     user = await bot.fetch_user(id)
#     if user:
#         await user.send("Hello")
#     else:
#         print(f"User with ID {id} found not.")


bot = myBot()

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
    elif isinstance(error, app_commands.MissingPermissions):
        return await interaction.response.send_message(f"You're missing permissions to use that")
    else:
        raise error

bot.tree.on_error = on_tree_error
asyncio.run(main())