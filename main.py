import json
import discord
from discord.ext import commands
import music

cogs = [music]

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)


@client.event
async def on_ready():
    print("logged in! as {0.user}".format(client))

# ----------Get token------------
credsf = open("creds.json")
creds = json.load(credsf)
TOKEN = creds["token"]
# -------------------------------

client.run(TOKEN)
