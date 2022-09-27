from datetime import datetime
import discord
from discord.ext import commands
import datetime
import asyncio



class Poll(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Poll.cog loaded.")
    
    @commands.command()
    async def poll(self,ctx: commands.Context,choice1, choice2, *, topic):
        embed= discord.Embed(title=topic, description= f":one: {choice1}\n\n:two: {choice2}",
        color=ctx.author.color,timestamp=datetime.datetime.utcnow())
        embed.set_footer(text= f"Poll by {ctx.author.name}")
        embed.set_thumbnail(url= ctx.author.avatar)
        message = await ctx.send(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await asyncio.sleep(5)

        newmessage = await ctx.fetch_message(message.id)
        
        
        
        onechoice=[user async for user in newmessage.reactions[0].users()]
        secchoice =[user async for user in newmessage.reactions[1].users()]
        
        result = "TIE"
        if len(onechoice)>len(secchoice):
            result = choice1
        elif len(secchoice)>len(onechoice):
            result = choice2
        
        embed= discord.Embed(title=topic, description= f"Result: {result}",
        color=ctx.author.color,timestamp=datetime.datetime.utcnow())
        embed.set_footer(text= f"{choice1} ||{choice2}")

        await newmessage.edit(embed=embed)

        


async def setup(bot):
   await bot.add_cog(Poll(bot))
