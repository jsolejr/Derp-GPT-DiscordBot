import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import io


load_dotenv()
DISCORD_TOKEN = os.environ['DALL-E_KEY']
OPENAI_API_KEY = os.environ['OPENAI_KEY']

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')

@bot.command()
async def generate_image(ctx, *, prompt: str):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            image_data = await resp.read()

    image_file = discord.File(io.BytesIO(image_data), filename="generated_image.png")
    await ctx.send(file=image_file)

bot.run(DISCORD_TOKEN)
