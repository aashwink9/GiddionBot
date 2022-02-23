import os
import discord
from discord.ext import commands
import music

# -------------FOR HEROKU ENV------------------
TOKEN = os.getenv("DISCORD_TOKEN")
# ---------------------------------------------

cogs = [music]

client = commands.Bot(command_prefix='=', intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)


@client.event
async def on_ready():
    print('logged in! as {0.user}'.format(client))


client.run(TOKEN)
