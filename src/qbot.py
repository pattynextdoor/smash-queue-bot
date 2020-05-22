import os
import discord
from dotenv import load_dotenv

# Load local environment vars from .env
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    name = client.user.name
    user_id = client.user.id
    print(f'Logged in as {name} with user id {user_id}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('q!list'):
        print('q!list command run!')

client.run(DISCORD_TOKEN)