import discord
from discord.ext import commands
import youtube_dl
import asyncio

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.queue = []
    self.namequeue = []
    self.firstflag = True

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
    YDL_OPTIONS = {'format':'bestaudio',
                  'default_search': 'auto',
                  'forceduration': True,
                  'forcetitle': True,
                  'forcedescription': True 
                  }
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      #print(info)
      if 'entries' in info:
        url2 = info['entries'][0]['formats'][0]['url']
        title = info['entries'][0]['title']
        web_page = info['entries'][0]['webpage_url']
        duration = info['entries'][0]['duration']
        await ctx.send(web_page)

      else:
        url2 = info['formats'][0]['url']
        title = info['title']
        web_page = info['webpage_url']
        duration = info['duration']
      
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      self.queue.append(source)
      self.namequeue.append(title+'('+str(duration)+'sec)\n'+web_page)
      if not vc.is_playing():
        await ctx.send('Now playing...')
      else:
        await ctx.send('Song queued')
      self.playit()

  def playit(self):
    try:
        self.client.voice_clients[0].play(source=self.queue[0], after = self.myafter)
        self.queue.pop(0)
        if(self.firstflag==False):
          self.namequeue.pop(0)
        self.firstflag=False
    except Exception as e:
        print(e)

  def myafter(self,error):
    try:
        fut = asyncio.run_coroutine_threadsafe(self.playit(), self.client.loop)
        fut.result()
    except Exception as e:
        print(e)

  @commands.command()
  async def pause(self,ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

  @commands.command()
  async def resume(self,ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resume")

  @commands.command()
  async def skip(self,ctx):
    await ctx.voice_client.stop()
    await ctx.send("Skipped")

  @commands.command()
  async def view(self,ctx):
    await ctx.send('Song List to Play:')
    for i, x in enumerate(self.namequeue):
      message = "Queue["+str(i+1)+"]: "+str(x)
      await ctx.send(message)

def setup(client):
  client.add_cog(music(client))