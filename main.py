import json
import nextcord as discord
from nextcord.ext import commands
import music
import triggers

cogs = [music, triggers]
bot = commands.Bot(command_prefix="=", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(bot)


@bot.event
async def on_ready():
    print("logged in! as {0.user}".format(bot))


# ----------Get token------------
credsf = open("creds.json")
creds = json.load(credsf)
TOKEN = creds["token"]
# -------------------------------

bot.run(TOKEN)
