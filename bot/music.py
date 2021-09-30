import discord
from discord.ext import commands
import youtube_dl
import asyncio

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.queue = []

  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("You are not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def disconnect(self,ctx):
    await ctx.voice_client.disconnect()

  @commands.command()
  async def play(self,ctx,url):
    #ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
    YDL_OPTIONS = {'format':'bestaudio', 'default_search': 'auto'}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      if 'entries' in info:
        url2 = info['entries'][0]['formats'][0]['url']
      else:
        url2 = info['formats'][0]['url']

      source = await discord.FFmpegOpusAudio.from_probe(self.queue[0], **FFMPEG_OPTIONS)
      self.queue.append(source)
      if not vc.is_playing():
        vc.play(source, after=lambda e: self.play_next(ctx))
        await ctx.send('Now playing...')
      else:
        await ctx.send('Song queued')

  @commands.command()
  async def play_next(self,ctx):
    if len(self.queue) >= 1:
      del self.queue[0]
      vc = ctx.voice_client
      vc.play(self.queue[0], after=lambda e: self.play_next(ctx))

  @commands.command()
  async def pause(self,ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

  @commands.command()
  async def resume(self,ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resume")

  @commands.command()
  async def stop(self,ctx):
    await ctx.voice_client.stop()
    await ctx.send("Stopped")


def setup(client):
  client.add_cog(music(client))
