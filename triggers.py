import nextcord as discord
from nextcord.ext import commands
import random


def commands_combos(com):
    if com == "kun":
        return "DO A KUNAL", "DO A KUNNU", "DO A SAUCY", "DO KUNAL", "DO SAUCY", "DO KUNNU"
    elif com == "wol":
        return "DO A WOLFY", "DO A WOODFIE", "DO A SHAHEEN", "DO WOLFY", "DO WOODFIE", "DO SHAHEEN"
    elif com == "im":
        return "I'M ", "IM ", "I AM "
    elif com == "yj":
        return "DO A YJ", "DO A YASHRAJ", "DO A STARK", "DO YJ", "DO STARK", "DO YASHRAJ"


class triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.master_countS = []
        self.master_countK = []
        self.master_countY = []

    def allcommands(self, com):
        # intro_mssg
        if com == 0:
            intro_mssg = "Hi I'm Giddion, Aashwin's proud creation. Nice to meet you! I can crack jokes, or generate " \
                         "a random number for you. Simply type 'crack jokes' if you want me to crack jokes, or " \
                         "'generate num' if you want me to generate a random number between 1 and 100. "
            return intro_mssg

        # I'm stuff message
        elif com == 1:
            return "https://i.kym-cdn.com/photos/images/facebook/002/057/173/8fa.png"

        # Kunal's impression
        elif com == 2:
            kun_responses = ["Yoooooooooooooooooooooooooooooooooooooon",
                             "What if- What if- pink floyd ya dark souls elden rings??? then wat???",
                             "*Random loud demonic singing in low pitched voice*",
                             "I'm [redacted] ??? :flushed::flushed:"]

            while True:
                response = random.choice(kun_responses)
                response_idx = kun_responses.index(response)

                if response_idx not in self.master_countK:
                    self.master_countK.append(response_idx)
                    return response
                elif len(kun_responses) == len(self.master_countK):
                    self.master_countK = []

        # Wolfy's impression
        elif com == 3:
            wolf_responses = ["OOOOOOOOOOO DEVANSH INSTAGRAM CHECK KAR" + ("JALDI " * 20),
                              "Bhai maa kasam kya maal dikh rahi hai :hot_face::hot_face:",
                              "gais mai zindaendar hu :smiley::smiley::smiley:",
                              "Medam meri nasen kaat do :pleading_face::sweat_smile:"
                              ]

            while True:
                response = random.choice(wolf_responses)
                response_idx = wolf_responses.index(response)

                if response_idx not in self.master_countS:
                    self.master_countS.append(response_idx)
                    return response
                elif len(wolf_responses) == len(self.master_countS):
                    self.master_countS = []

        # Yj's impression
        elif com == 4:
            yj_responses = ["Ooooo gais mai jatt hu :sweat_smile::sweat_smile:",
                            "Funni nai hai tu bhai funni nai hai :nose::nose::nose:",
                            "Devu F1 ke statistics bata jaldi",
                            "Gais mujhe ladkiyon me koi dilchaspi nahi hai sorri :pensive::pensive:",
                            "[manages to fit every conceivable gaali in a single sentence]"
                            ]

            while True:
                response = random.choice(yj_responses)
                response_idx = yj_responses.index(response)

                if response_idx not in self.master_countY:
                    self.master_countY.append(response_idx)
                    return response
                elif len(yj_responses) == len(self.master_countY):
                    self.master_countY = []

    @commands.Cog.listener()
    async def on_message(self, message):
        mssg = message.content

        if mssg.upper().startswith('ENDAR ') and (mssg.upper() != 'ENDAR'):
            idx = mssg.index(' ')
            rest = mssg[idx + 1:]
            await message.channel.send(f'{rest}endar :sweat_smile::sweat_smile::sweat_smile:')

        elif mssg.upper().startswith(commands_combos("im")):
            await message.channel.send(self.allcommands(1))

        elif mssg.upper().startswith(commands_combos("kun")):
            await message.channel.send(self.allcommands(2))

        elif mssg.upper().startswith(commands_combos("wol")):
            await message.channel.send(self.allcommands(3))

        elif mssg.upper().startswith(commands_combos("yj")):
            await message.channel.send(self.allcommands(4))


def setup(bot):
    bot.add_cog(triggers(bot))
