from os import times
import warnings
import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    "Moderation itself"
    def __init__(self,bot: commands.Bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation.cog loaded.")

    @commands.command(aliases = ['ba'])
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx: commands.Context,member:discord.Member,*,reason="No reason Provided"):
        "Ban's user from the guild"
        embed = discord.Embed(title = "Member Banned", 
        description=f"{member.mention} is Banned from {ctx.guild.name} by {ctx.author.mention}\nReason: {reason}", 
        color = discord.Color.random(), timestamp=datetime.datetime.utcnow)
        try:
            await member.ban(reason = reason)
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed = discord.Embed(title = "Missing permissions", 
            description="The bot doesn't has the required permissions to Ban member"),
            color=discord.Color.red())


    @commands.command(aliases = ['k'])
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx: commands.Context, member:discord.Member,*,reason="No reason Provided"):
        "Kicks user from the guild"
        embed = discord.Embed(title = "Member Kick", 
        description=f"{member.mention} is kicked from {ctx.guild.name} by {ctx.author.mention}\nReason: {reason}", 
        color = discord.Color.random(), timestamp=datetime.datetime.utcnow)
        try:
            await member.kick(reason = reason)
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed = discord.Embed(title = "Missing permissions", 
            description="The bot doesn't has the required permissions to Kick member"),
            color=discord.Color.red())
    
    @commands.command(aliases = ['ub'])
    @commands.has_permissions(ban_members = True)
    async def unban(self,ctx: commands.Context,member_id):
        "Unbans user from the guild"
        user = await self.bot.fetch_user(member_id)
        embed = discord.Embed(title = "Member UnBanned", 
        description=f"{user.name} is unbanned from {ctx.guild.name} by {ctx.author.mention}", 
        color = discord.Color.random(), timestamp=datetime.datetime.utcnow)
        try:
            await ctx.guild.unban(user)
            await ctx.send(embed=embed)
            return
        except discord.NotFound:
            await ctx.send(embed= discord.Embed(title = "Member not Found!!",color=discord.Color.red()))
            await ctx.send(embed = discord.Embed(title = "Missing permissions", 
            description="The bot doesn't has the required permissions to UnBan member"),
            color=discord.Color.red())

    @commands.command(aliases = ['c'])
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx: commands.Context, amount:int = 2):
        "Clears messages"
        if amount < 1:
            await ctx.send("Amount should be more than 1")
            return
        try:
            await ctx.channel.purge(limit = amount+1)
        except:
            await ctx.send(embed = discord.Embed(title = "Missing permissions", 
            description="The bot doesn't has the required permissions to purge"),
            color=discord.Color.red())



            
                   
   

async def setup(bot):
   await bot.add_cog(Moderation(bot))
