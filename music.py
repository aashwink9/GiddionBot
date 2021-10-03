import discord
from discord.ext import commands
import youtube_dl
import asyncio

import urllib.parse, urllib.request, re
import requests
from discord import Embed, FFmpegPCMAudio
from discord.utils import get

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ytdl = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, play=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=False)
        )

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)


class music(commands.Cog):
    def __init__(self, client, queue):
        self.client = client
        self.queue = queue

    @commands.command()
    async def dc(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return

        elif not (voice == None):
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            print(self.queue.keys())

            try:
              if len(self.queue) == 0:
                self.start_playing(ctx.voice_client, player)
                await ctx.send(
                    f":mag_right: **Searching for** "
                    + url
                    + "\n<:play_pause:763374159567781890> **Now Playing:** ``{}".format(
                        player.title
                    )
                    + "``"
                )
                return

              else:
                self.queue[len(self.queue)] = player
                await ctx.send(
                    f":mag_right: **Searching for**"
                    + url
                    + "\n<:play_pause:763374159567781890> **Added to queue:** ``{}".format(
                        player.title
                    )
                    + "``"
                )


            except:
              await ctx.send("Somenthing went wrong - please try again later!")

        else:
            await channel.connect()
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            print(self.queue.keys())
            try:
              if len(self.queue) == 0:
                self.start_playing(ctx.voice_client, player)
                await ctx.send(
                    f":mag_right: **Searching for** "
                    + url
                    + "\n<:play_pause:763374159567781890> **Now Playing:** ``{}".format(
                        player.title
                    )
                    + "``"
                )
                return

              else:
                self.queue[len(self.queue)] = player
                await ctx.send(
                    f":mag_right: **Searching for** "
                    + url
                    + "\n<:play_pause:763374159567781890> **Added to queue:** ``{}".format(
                        player.title
                    )
                    + "``"
                  )
                
            except:
              await ctx.send("Somenthing went wrong - please try again later!")


    def start_playing(self, voice_client, player):

        self.queue[0] = player

        i = 0
        while i < len(self.queue):
            try:
                voice_client.play(
                    self.queue[i],
                    after=lambda e: print("Player error:   %s" % e) if e else None,
                )

            except:
                pass
            i += 1


    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused!")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("resumed!")

    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user = ctx.message.author.mention
        await voice_client.disconnect()
        await ctx.send(f'Disconnected from {user}')


    @commands.command()
    async def 



def setup(client):
    q = {}
    client.add_cog(music(client, q))
