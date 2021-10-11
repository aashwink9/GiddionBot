import discord
from discord.ext import commands
import youtube_dl
import asyncio

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
    "ignoreerrors": True,
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
    def __init__(self, client):
        self.client = client
        self.queue = []


    @commands.command()
    async def play(self, ctx, url):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        song = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        position = len(self.queue) + 1

        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return

        elif not (voice is None):

            try:
                self.queue.append(song)
                await ctx.send(
                    f":mag_right: **Searching for** "
                    + "*" + url + "*"
                    + "\n<:play_pause:763374159567781890> **Queued Song: ** ``{}".format(
                        song.title
                    )
                    + "``"
                    + " **At Position ("
                    + str(position)
                    + ")**"
                )

            except:
                await ctx.send("Something went wrong - please try again later!")


        else:
            await channel.connect()
            try:
                self.queue.append(song)
                while self.queue:
                    ctx.voice_client.stop()
                    ctx.voice_client.play(self.queue.pop(0), after=lambda e: print("Player error:   %s" % e) if e else None, )

                await ctx.send(
                    f":mag_right: **Searching for** "
                    "*" + url + "*"
                    + "\n<:arrow_forward:763374159567781890> **Now Playing: ** ``{}".format(
                        song.title
                    )
                    + "``"
                )

            except:
                await ctx.send("Something went wrong - please try again later!")


    @commands.command()
    async def p(self, ctx, url):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        song = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        position = len(self.queue) + 1

        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return

        elif not (voice is None):

            try:
                self.queue.append(song)
                await ctx.send(
                    f":mag_right: **Searching for** "
                    + "*" + url + "*"
                    + "\n<:play_pause:763374159567781890> **Queued Song: ** ``{}".format(
                        song.title
                    )
                    + "``"
                    + " **At Position ("
                    + str(position)
                    + ")**"
                )

            except:
                await ctx.send("Something went wrong - please try again later!")


        else:
            await channel.connect()
            try:
                self.queue.append(song)
                while self.queue:
                    ctx.voice_client.stop()
                    ctx.voice_client.play(self.queue.pop(0),
                                          after=lambda e: print("Player error:   %s" % e) if e else None, )

                await ctx.send(
                    f":mag_right: **Searching for** "
                    "*" + url + "*"
                    + "\n<:arrow_forward:763374159567781890> **Now Playing: ** ``{}".format(
                        song.title
                    )
                    + "``"
                )

            except:
                await ctx.send("Something went wrong - please try again later!")

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send(":pause_button: Paused!")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send(":arrow_forward: resumed!")


    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user = ctx.message.author.mention
        await voice_client.disconnect()
        await ctx.send(f"Disconnected by {user}")

    @commands.command()
    async def dc(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user = ctx.message.author.mention
        await voice_client.disconnect()
        await ctx.send(f"Disconnected by {user}")

    @commands.command()
    async def disconnect(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user = ctx.message.author.mention
        await voice_client.disconnect()
        await ctx.send(f"Disconnected by {user}")

    @commands.command()
    async def reset(self, ctx):
        voice_client = ctx.message.guild.voice_client
        self.queue.clear()
        await ctx.send(":gun: The queue has been reset! Exiting...")
        voice_client.disconnect()

    @commands.command()
    async def clearq(self, ctx):
        self.queue.clear()
        await ctx.send(":gun: The queue has been cleared!")


    @commands.command()
    async def skip(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if len(self.queue) == 0:
            await ctx.send(":stop_sign: *Stopping...\nLooks like you've at the end of the queue!*")
            voice_client.stop()
            return
        else:
            voice_client.stop()
            await ctx.send(":fast_forward: *Skipping!*")
            ctx.voice_client.play(self.queue.pop(0))
            return

    @commands.command()
    async def next(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if len(self.queue) == 0:
            voice_client.stop()
            await ctx.send(":stop_sign: *Stopping...\nLooks like you've at the end of the queue!*")
            return
        await ctx.send(":fast_forward: *Skipping!*")
        ctx.voice_client.play(self.queue.pop(0))

    @commands.command()
    async def stop(self, ctx):
      voice_client = ctx.message.guild.voice_client
      voice_client.stop()
      await ctx.send(":stop_sign: *Stopped!*")
      voice_client.disconnect()

    @commands.command()
    async def show(self, ctx):

      if len(self.queue) == 0:
        await ctx.send("The queue is empty!")
        return

      qstr = ""
      i = 1
      for q in self.queue:
        qstr += i + ". " + str(q.title)

      await ctx.send("Songs in queue:\n" + qstr)

def setup(client):
    client.add_cog(music(client))
