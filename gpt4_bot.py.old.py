import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD_Token']
OPENAI_KEY = os.environ['OPENAI_KEY']

openai.api_key = OPENAI_KEY

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix=None, intents=intents)

bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=message.content,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response_text = response.choices[0].text.strip()
        await message.channel.send(response_text)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

bot.run(DISCORD_TOKEN)
