import discord
from discord.ext import commands
import asyncio
from itertools import cycle

class HelpView(discord.ui.View):

  @discord.ui.button(
    label = "My Invite Link!",
    style = discord.ButtonStyle.success,
    emoji = "🔗",
  )

  async def button_callback(self, button, interaction):
        await interaction.response.send_message('https://google.com', ephemeral=True)

  @discord.ui.select(
    placeholder='Select a Command Category!',
    min_values=1, 
    max_values=1, 
    options = [
            discord.SelectOption(
                label="Discord", description="All of the Discord Commands!", emoji="🖥️"
            ),
            discord.SelectOption(
                label="Roblox", description="All of the Roblox commands!", emoji="🟥"
            ),
        ])

  async def select_callback(self, select, interaction):

      if select.values[0] == "Discord Commands":
        embed=discord.Embed(title="**[🖥️] Discord Commands ~**",color=0x00ff33)

        embed.add_field(
          name="`Add Admin Role` -", 
          value="**Aliases -** `addadminrole` \n **Description -** Add a role that can run admin-level commands! \n **Examples -** `!addadminrole [role-id]`",
          inline=False
          )
        embed.add_field(
          name="`Add Commander Role` -",
          value="**Aliases -** `addcommanderrole ` \n **Description -** Add a role that can run commander-level commands! \n **Examples -** `!addcommanderrole [role-id]`",
          inline=False
        )
        embed.add_field(
            name="`Role` -",
            value="**Aliases -** `role` \n **Description -** Give a role to a user within your Regiment! \n **Examples -** `!role [user] [role-name]`",
            inline=False
        )
        embed.add_field(
            name="`Set Nick` -",
            value="**Aliases -** `setnick` \n **Description -** Set another user's nickname! \n **Examples -** `!setnick [user] [nickname]`",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

      if select.values[0] == "Roblox Commands":
        embed=discord.Embed(title="**[🟥] Discord Commands ~**",color=0x00ff33)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

class Help(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def help(self, ctx):

    embed=discord.Embed(color=0xae00ff)
    embed.add_field(name="You've asked for help!", value="Hey! I'm [INSERT BOT NAME HERE]! Use the Dropdown Menu below and choose the command that you need help with! Thanks for using Squid Games Bot! Below are my support servers and my invite link if you want to invite me to other servers!", inline=False)
    embed.set_footer(text="This Dropdown Menu closes in 180 Seconds Due to Limitations.")

    await ctx.send(embed=embed, view=HelpView(timeout=180))

def setup(bot):
  bot.add_cog(Help(bot))