import discord
from discord.ext import commands
import asyncio
import json
import requests
from roblox import Client

class roblox_cmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.client = Client("INSERT YOUR ROBLOX TOKEN HERE")
    
    @commands.command()
    async def verify(self, ctx):

        r = requests.get(f"https://api.blox.link/v1/user/{ctx.author.id}")
        user_id = r.json()["primaryAccount"]
        status = r.json()["status"]
        
        if status == "ok":
            user = await self.client.get_user(user_id)
            await open_account(ctx.author, user.name)
            em = discord.Embed( 
                title="Signed In!", 
                description=f"You have successfully been signed in as `{user.display_name} (@{user.name})`", 
                colour=discord.Colour.green()
                )
            await ctx.send(embed=em)

        else:
            em = discord.Embed(title="No Linked Account!", 
            description="I've detected that you have no Roblox Account linked to your account. Please visit https://blox.link/verify and do `!verify` to link an account to discord.", 
            colour = discord.Colour.red())
            await ctx.send(embed=em)
        return
        
    @commands.command()
    async def user(self, ctx, member:discord.Member=None):

        users = await get_user_data()

        username = users[str(member.id)]
        ropy_user = await self.client.get_user_by_username(f"{username}", expand=True)

        r = requests.get(f"https://api.roblox.com/users/get-by-username?username={username}")
        user_id = r.json()["Id"]

        user = await self.client.get_user(user_id)
        user_thumbnails = await self.client.thumbnails.get_user_avatar_thumbnails(
            users=[user],
            type=AvatarThumbnailType.full_body,
            size=(420, 420)
        )

        if len(user_thumbnails) > 0:
            user_thumbnail = user_thumbnails[0]
            print(user_thumbnail.image_url)
            thumbnail = user_thumbsnail.image_url
        
        em = discord.Embed(colour=discord.Colour.green())
        em.add_field(name="User's ID -", value=ropy_user.id)
        em.add_field(name="Display Name -", value=ropy_user.display_name)
        em.add_field(name="Creation Date -", value=ropy_user.created.strftime("%m/%d/%Y, %H:%M:%S"))
        em.set_thumbnail(url=thumbnail)
        await ctx.send(embed=em)

        return

    @commands.command()
    async def bgcheck(self, ctx, member:discord.Member=None):

        if member == None:
            em = discord.Embed(
                title="Background Check -",
                description="!bgcheck [member]",
                colour=discord.Colour.blue()
            )

        else:
            try:
                users = await get_user_data()
                await ctx.send()
            except:
                em = discord.Embed(
                    title="Error!", 
                    description="This user has not Signed In. Please ask them to run !verify to get cached.", 
                    colour = discord.Colour.red())
                await ctx.send(embed=em)

        return

    @commands.command()
    async def discharge(self, ctx, member_id:discord.Member=None):
#        try:

            member = ctx.author
            
            embed = discord.Embed(title="Discharge | 🔨",
                        description="Time to discharge a user. Answer the following questions in 90 seconds each of the Discharge Information.",
                        color=ctx.author.color)
            await ctx.send("Discharge Process has started in DMs!")
            await member.send(embed=embed)

            questions=[
                "What is the username of the person you are discharging?",
                "What type of Discharge is it?",
                "What rank are they being discharged from?",
                "Why are they being discharged?",
                "Would you like to submit this discharge? ( type yes or no)"
                ]
            answers = []

            def check(m):
                    return m.author == ctx.author
            
            for i, question in enumerate(questions):
                embed = discord.Embed(title=f"Question {i+1}",
                            description=question, footer="If you would like to cancel at anytime, you can type cancel.")
                await member.send(embed=embed)
                try:
                    message = await self.bot.wait_for('message', timeout=90, check=check)
                except TimeoutError:
                    await member.send("You didn't answer the questions in Time")
                    return
                answers.append(message.content)

            if answers[5] == "yes":

                discharged_id = answers[0]
                discharged_username = answers[1]
                discharge_type = answers[2]
                discharged_rank = answers[3]
                discharged_reason = answers[4]
                officer_id = ctx.author.id

                await log_discharge(discharged_id, discharged_username, discharge_type,  discharged_rank, discharged_reason, officer_id)
                await member.send(f"{answers[0]}\n{answers[1]}\n{answers[2]}\n{answers[3]}\n{answers[4]}") 
            else:
                await member.send("Your discharge request has been revoked.")
#       except:
#            await ctx.send("Your Direct Messages are Off. Please turn them back on and try again.")

    @commands.command()
    async def setrank(self, ctx, user:discord.Member=None, rank=None):

        group = await self.client.get_group("GROUP ID GOES HERE")
        users = await get_user_data()
        username = users[str(user.id)]

        if user is None:
            await ctx.send("Please, include a valid username.")

        elif rank is None:
            await ctx.send("Please, include the new rank.")

        elif rank is not None and user is not None:
            if rank == "RANK NAME HERE":
                rank = "RANK ID GOES HERE"
                player = await self.client.get_user_by_username(username)
                player.set_rank(int(rank),group)
            
            else:
                rank = "RANK ID GOES HERE"
                player = await self.client.get_user_by_username(username)
                player.set_rank(int(rank),group)

def setup(bot):
  bot.add_cog(roblox_cmds(bot))


async def get_user_data():

    with open("roblox_users.json","r") as f:
        users = json.load(f)
    
    return users

async def open_account(user, username):

    with open("roblox_users.json", "r") as f:
            users = json.load(f)

    users[str(user.id)] = f"{username}"

    with open("roblox_users.json", "w") as f:
        json.dump(users,f)

async def log_discharge(discord_id, roblox, type, where, reason, officer):

    with open("discharges.json","r") as f:
        users = json.load(f)
    
    with open("config.json","r") as f:
        data = json.load(f)

    discharge_id = int(data["discharge-number"])
    discharge_id += 1

    data["discharge_number"] = int(discharge_id)
    with open("config.json", 'w') as f:
        json.dump(data, f)

    users["discharge-id"] = f"{discharge_id}"
    users["discharge-id"]["user-id"]=f"{discord_id}"
    users["discharge-id"]["roblox-user"] = f"{roblox}"
    users["discharge-id"]["discharge-type"] = f"{type}"
    users["discharge-id"]["discharge-location"] = f"{where}"
    users["discharge-id"]["discharge-reason"] = f"{reason}"
    users["discharge-id"]["officer-id"] = f"{officer}"

    with open("discharges.json","w") as f:
        json.dump(users,f)
        
