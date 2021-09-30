import os
from discord.ext import commands
import discord
import music

cogs = [music]
bot = commands.Bot(command_prefix="!",  intents = discord.Intents.all())
TOKEN = os.getenv("DISCORD_TOKEN")

for i in range(len(cogs)):
      cogs[i].setup(bot)

if __name__ == "__main__":
    bot.run(TOKEN)
