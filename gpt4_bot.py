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

class ChatBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'{self.user} is connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        input_content = message.content

        if message.attachments:
            for attachment in message.attachments:
                # Read the attachment bytes
                image_bytes = await attachment.read()
                input_content += f' [Attachment: {attachment.filename}]'

        # Prepare the API call
        response = openai.ChatCompletion.create(
            engine="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_content}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the assistant's reply from the response
        assistant_reply = response.choices[0].message.content

        # Send the reply back in the Discord channel
        await message.channel.send(assistant_reply)

client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)
