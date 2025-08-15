import discord
import asyncio
import sqlite3 as sql
import sys
import os
from loguru import logger
from dotenv import load_dotenv
from discord.ext import commands
from discord import embeds, guild, client, Intents

logger.remove()

logger.add(
    sys.stdout,
    format="<black><bg white> {time:HH:mm:ss} </bg white></black><black><bg green>  {level}  </bg green></black> {message}",
    level="INFO",
    colorize=True
)
logger.add(
    sys.stdout,
    format="<black><bg white> {time:HH:mm:ss} </bg white></black><black><bg #FFA500>  {level}  </bg #FFA500></black> {message}",
    level="WARNING",
    colorize=True
)
logger.add(
    sys.stdout,
    format="<black><bg white> {time:HH:mm:ss} </bg white></black><black><bg red>  {level}  </bg red></black> {message}",
    level="ERROR",
    colorize=True
)

conn = sql.connect('databases/economy.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS economy (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)
""")
conn.commit()

env_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(env_path, ".env"))

intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="DaggerNodes host now!")
client = commands.Bot(command_prefix='dn!', help_command=None, activity=activity, intents=intents)
client.conn = conn
client.cursor = cursor

@client.event
async def on_ready():
    try:
      synced_commands = await client.tree.sync()
      logger.info(f'Successfully synced {len(synced_commands)} commands.')
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