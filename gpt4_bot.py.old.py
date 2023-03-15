import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD_Token']
OPENAI_KEY = os.environ['OPENAI_KEY']

openai.api_key = OPENAI_KEY

# Create a bot instance with necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix=None, intents=intents)

# Remove the default help command
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

#    response = openai.Completion.create(
#        engine="gpt-4",
#        prompt=message.content,
#        max_tokens=150,
#        n=1,
#        stop=None,
#        temperature=0.5,
#    )

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

# Error handler to ignore CommandNotFound exception
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

bot.run(DISCORD_TOKEN)
