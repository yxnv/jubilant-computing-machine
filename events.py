import discord
from discord.ext import commands
import asyncio
from itertools import cycle

class events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):

      print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
      print("------")

      status = [[f"to !help", 2]]
      displaying = cycle(status)

      running = True
      
      while running is True:
        current_status = next(displaying)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=current_status[0] ,type=current_status[1]))
        await asyncio.sleep(5)
    
def setup(bot):
  bot.add_cog(events(bot))