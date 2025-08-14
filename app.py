import discord
import asyncio
import os
from loguru import logger
from dotenv import load_dotenv
from discord.ext import commands
from discord import embeds, guild, client, Intents

logger.remove()

logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="INFO"
)

env_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(env_path, ".env"))

intents = discord.Intents.all()
client = commands.Bot(command_prefix='dn!', intents=intents)

@client.event
async def on_ready():
    activity = discord.Game(name="DaggerNodes host now!")
    try:
      synced_commands = await client.tree.sync()
      logger.info('Successfully synced commands.')
    except Exception as error:
     pass
    logger.info("{0.user} bot is now online".format(client))

async def load_cogs():
    for root, dirs, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file).replace("/", ".").replace("\\", ".")[:-3]
                try:
                    await client.load_extension(path)
                except Exception as error:
                    logger.error(f'Failed to load {path} error stack: {error}')

async def main():
    async with client:
        await load_cogs()
        await client.start(os.getenv("TOKEN"))

asyncio.run(main())