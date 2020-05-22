import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load local environment vars from .env
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='q!')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

print(os.listdir('./cogs'))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(DISCORD_TOKEN)