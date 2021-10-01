import discord
from discord.ext import commands
import random
import music


cogs = [music]

client = commands.Bot(command_prefix='-', intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

def jokes():
    jokes = ["I ate a clock yesterday, it was very time-consuming.",
             "Have you played the updated kids' game? I Spy With My Little Eye . . . Phone.",
             "A perfectionist walked into a bar...apparently, the bar wasn’t set high enough.",
             ]

    return random.choice(jokes)


def allcommands(com):
    if com == "greeting":
        intro_mssg = "Hi I'm Giddion, Aashwin's proud creation. Nice to meet you! I can crack jokes, or generate a random " \
                     "number for you. Simply type 'crack jokes' if you want me to crack jokes, or 'generate num' if you want " \
                     "me to generate a random number between 1 and 100. "
        return intro_mssg

        
@client.event
async def on_ready():
    print('logged in! as {0.user}'.format(client))


client.run('ODQ0NDYwMzAyODIxMjI4NTc1.YKSu8Q.ZvhDRb51nUFi2CFJCPEnqq_-KKw')