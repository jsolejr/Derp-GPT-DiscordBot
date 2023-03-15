import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

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

    async with ctx.typing():
        async with requests.get(image_url) as r:
            if r.status_code != 200:
                await ctx.send('Failed to generate an image. Please try again.')
                return

            image_data = r.content

        with io.BytesIO(image_data) as image_io:
            await ctx.send(file=discord.File(image_io, 'generated_image.png'))

bot.run(DISCORD_TOKEN)
