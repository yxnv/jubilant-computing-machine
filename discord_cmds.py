import discord
from discord.ext import commands
import json

class discord_cmds(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def setnick(self, ctx, member:discord.Member=None, *, nick=None):

    with open("config.json") as f:
      data = json.load(f)

      admin_role = False
    
    for role_id in data["admin-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                admin_role = True
        except:
            pass

    if ctx.author.guild_permissions.administrator or admin_role:
      if member == None or nick == None:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name="SetNick Command -", value="Usage - \n !setnick [user] [nick]")
        await ctx.send(embed=embed)
        return
      else:
        await member.edit(nick=nick)
        embed = discord.Embed(colour=discord.Colour.green())
        embed.add_field(name="Nick!", value=f"{member.mention}'s nickname was changed to `{nick}` by {ctx.author.mention}")
        await ctx.send(embed=embed)
        return
      
    else:
      embed = discord.Embed(colour=discord.Colour.red())
      embed.add_field(name="Error!", value="You don't have permission to run this command!")
      await ctx.send(embed=embed)
      return

  @commands.command()
  async def role(self, ctx, member:discord.Member=None, *, role_name=None):

    with open("config.json") as f:
      data = json.load(f)

      commander_role = False
    
    for role_id in data["commands-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                commander_role = True
        except:
            pass
    
    if ctx.author.guild_permissions.administrator or commander_role:

      if commander_role == "[ INSERT COMMANDER ROLE ID HERE ]":
        if role_name == "" or role_name == "" or role_name == "":
          try:
            await member.add_roles(role_name)
            em = discord.Embed(title="Success!", description=f"{member.mention} was given the role {role_name} by {ctx.author.mention}", colour=discord.Colour.green())
            await ctx.send(embed=em)
          except:
              em = discord.Embed(title="Error!", description="That isn't a valid role name. Please try again with a valid role Name.", colour=discord.Colour.red())
              await ctx.send(embed=em)
        else:
          em = discord.Embed(title="Error!", description="You don't have access to these regiment roles.", colour=discord.Colour.red())
          await ctx.send(embed=em)



    else:
      embed = discord.Embed(colour=discord.Colour.red())
      embed.add_field(name="Error!", value="You don't have permission to run this command!")
      await ctx.send(embed=embed)
      return

    

  @commands.command()
  async def addadminrole(self, ctx, input=None, role_id=None):
    if ctx.author.guild_permissions.administrator:

      if input == None or role_id == None:
        em = discord.Embed(title="Add Admin Command-", description="Usage - \n !addadminrole [add/remove] [role_id]", colour=discord.Colour.blue())
        await ctx.send(embed=em)
      
      else:
        if input == "add" or input == "Add":
          try:
              role_id = int(role_id)
              role = ctx.guild.get_role(role_id)

              with open("config.json") as f:
                  data = json.load(f)

              data["admin-roles"].append(role_id)

              with open('config.json', 'w') as f:
                  json.dump(data, f)
              
              em = discord.Embed(title="Success!", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0x00a8ff)
              await ctx.send(embed=em)

          except:
              em = discord.Embed(title="Error!", description="That isn't a valid role ID. Please try again with a valid role ID.", colour=discord.Colour.red())
              await ctx.send(embed=em)

        if input == "rm" or input == "remove":
          try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            admin_roles = data["verified-roles"]

            if role_id in admin_roles:
                index = admin_roles.index(role_id)

                del admin_roles[index]

                data["verified-roles"] = admin_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)
            
          except:
              em = discord.Embed(title="Error!", description="That isn't a valid role ID. Please try again with a valid role ID.", colour=discord.Colour.red())
              await ctx.send(embed=em)

    else:
      embed = discord.Embed(colour=discord.Colour.red())
      embed.add_field(name="Error!", value="You don't have permission to run this command!")
      await ctx.send(embed=embed)
      return

  @commands.command()
  async def addcommanderrole(self, ctx, input=None, role_id=None):
    if ctx.author.guild_permissions.administrator:

      if input == None or role_id == None:
        em = discord.Embed(title="Add Admin Command-", description="Usage - \n !addcommanderrole [add/remove] [role_id]", colour=discord.Colour.blue())
        await ctx.send(embed=em)
      
      else:
        if input == "add" or input == "Add":
          try:
              role_id = int(role_id)
              role = ctx.guild.get_role(role_id)

              with open("config.json") as f:
                  data = json.load(f)

              data["command-roles"].append(role_id)

              with open('config.json', 'w') as f:
                  json.dump(data, f)
              
              em = discord.Embed(title="Success!", description="You have successfully added `{}` to the list of roles that can run commander-level commands!".format(role.name), color=0x00a8ff)
              await ctx.send(embed=em)

          except:
              em = discord.Embed(title="Error!", description="That isn't a valid role ID. Please try again with a valid role ID.", colour=discord.Colour.red())
              await ctx.send(embed=em)

        if input == "rm" or input == "remove":
          try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("config.json") as f:
                data = json.load(f)

            admin_roles = data["command-roles"]

            if role_id in admin_roles:
                index = admin_roles.index(role_id)

                del admin_roles[index]

                data["command-roles"] = admin_roles

                with open('config.json', 'w') as f:
                    json.dump(data, f)
                
                em = discord.Embed(
                  title="Success!",
                  description="You have successfully removed `{}` from the list of roles that can run commander-level commands!".format(role.name), 
                  color=0x00a8ff
                )
            
          except:
              em = discord.Embed(title="Error!", description="That isn't a valid role ID. Please try again with a valid role ID.", colour=discord.Colour.red())
              await ctx.send(embed=em)

    else:
      embed = discord.Embed(colour=discord.Colour.red())
      embed.add_field(name="Error!", value="You don't have permission to run this command!")
      await ctx.send(embed=embed)
      return

def setup(bot):
  bot.add_cog(discord_cmds(bot))