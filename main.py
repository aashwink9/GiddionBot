import nextcord as discord
from nextcord.ext import commands
import music
import os

# -------------FOR HEROKU ENV------------------
TOKEN = os.getenv("DISCORD_TOKEN")
# ---------------------------------------------

cogs = [music]

bot = commands.Bot(command_prefix="#", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(bot)


@bot.event
async def on_ready():
    print("logged in! as {0.user}".format(bot))

bot.run(TOKEN)
