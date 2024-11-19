import discord
import os
from discord.ext import commands
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("OPEN_API_KEY"),
)

joke_messages = [
    {"role": "system", "content": "You are a comedian. Very casual and raw"},
    ]


class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="joke", description="Tells a joke")
    async def joke(self, interaction: discord.Interaction):
        joke_messages.append({"role": "user", "content": "Tell me a unique joke! Don't say 'Sure Thing' just say the joke."})
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model
            messages=joke_messages,
            temperature=0.9,
            max_tokens=150
            )
        joke = (completion.choices[0].message.content.strip())
        joke_messages.append({"role": "assistant", "content": joke})
        await interaction.response.send_message(joke)
    
async def setup(bot):
    await bot.add_cog(Joke(bot))