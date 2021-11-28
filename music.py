import discord
from discord.ext import commands
import youtube_dl
import asyncio
from functools import partial

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
        self.url = data.get("webpage_url")
        self.duration = data.get("duration")

    @classmethod
    async def from_url(cls, url: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=False)
        )

        if "entries" in data:
            data = data["entries"][0]

        if download:
            filename = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'title': data['title'], 'duration': data['duration']}

        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data)


class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

    def destroy(self, ctx):
        """Disconnect and cleanup the player."""
        return self.client.loop.create_task(ctx.cog.cleanup(ctx.guild))

    @commands.command()
    async def play(self, ctx, *, search: str):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        getsong = await YTDLSource.from_url(search, loop=self.client.loop, download=False)
        song = await YTDLSource.regather_stream(getsong, loop=self.client.loop)
        position = self.queue.qsize() + 1

        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return

        elif voice:
            if not voice.is_playing():
                await self.queue.put(song)

                while self.queue.qsize() > 0:
                    curr_song = await self.queue.get()
                    dur = curr_song.duration
                    ctx.voice_client.play(curr_song,
                                          after=lambda _: self.client.loop.call_soon_threadsafe(self.next.set))
                    await ctx.send(
                        f":mag_right: **Searching for** "
                        "*" + search + "*"
                        + "\n<:arrow_forward:763374159567781890> **Now Playing: ** ``{}".format(
                            song.title
                        )
                        + "``"
                    )
                    await asyncio.sleep(dur + 1)

            else:
                await self.queue.put(song)
                await ctx.send(
                    f":mag_right: **Searching for** "
                    + "*" + search + "*"
                    + "\n<:play_pause:763374159567781890> **Queued Song: ** ``{}".format(
                        song.title
                    )
                    + "``"
                    + " **At Position ("
                    + str(position)
                    + ")**"
                )

        else:
            await channel.connect()
            await self.queue.put(song)

            while self.queue.qsize() > 0:
                curr_song = await self.queue.get()
                dur = curr_song.duration
                ctx.voice_client.play(curr_song, after=lambda _: self.client.loop.call_soon_threadsafe(self.next.set))
                await ctx.send(
                    f":mag_right: **Searching for** "
                    "*" + search + "*"
                    + "\n<:arrow_forward:763374159567781890> **Now Playing: ** ``{}".format(
                        song.title
                    )
                    + "``"
                )
                await asyncio.sleep(dur + 1)

    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.pause()
        await ctx.send(":pause_button: Paused!")

    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.resume()
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
        while self.queue.empty() is not True:
            await self.queue.get()
        await ctx.send(":gun: The queue has been reset! Exiting...")
        await voice_client.disconnect()

    @commands.command()
    async def clearq(self, ctx):
        while self.queue.empty() is not True:
            await self.queue.get()
        await ctx.send(":gun: The queue has been cleared!")

    @commands.command()
    async def skip(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if self.queue.qsize() == 0:
            await ctx.send(":stop_sign: *Stopping...\nLooks like you've at the end of the queue!*")
            voice_client.stop()
            return
        else:
            voice_client.stop()
            nextsong = await self.queue.get()
            ctx.voice_client.play(nextsong, after=lambda _: self.client.loop.call_soon_threadsafe(self.next.set))
            await ctx.send(":fast_forward: *Skipping!*\n**Playing:** " + "``" + str(nextsong.title) + "``")
            return

    @commands.command()
    async def next(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if self.queue.qsize() == 0:
            await ctx.send(":stop_sign: *Stopping...\nLooks like you've at the end of the queue!*")
            voice_client.stop()
            return
        else:
            voice_client.stop()
            nextsong = await self.queue.get()
            ctx.voice_client.play(nextsong, after=lambda _: self.client.loop.call_soon_threadsafe(self.next.set))
            await ctx.send(":fast_forward: *Skipping!*\n**Playing:** " + "``" + str(nextsong.title) + "``")
            return

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        voice_client.stop()
        await ctx.send(":stop_sign: *Stopped!*")

    @commands.command()
    async def show(self, ctx):
        if self.queue.qsize() == 0:
            await ctx.send("The queue is empty!")
            return

        await ctx.send("**Songs in queue:**\n")


def setup(client):
    client.add_cog(music(client))
