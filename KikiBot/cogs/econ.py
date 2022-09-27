from ntpath import join
from tkinter.messagebox import RETRY
from tracemalloc import stop
import discord
import os
import asyncio
from discord.ext import commands, tasks
from discord.ui import Button, View, Select
import sqlite3
import random
from time import sleep
from DiscordEconomy.Sqlite import Economy
from lists.itemslist import *
from lists.fishinglist import *
import tracemalloc
from main import economy


                                          
class econ(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
     
        
    
    
      
    @commands.Cog.listener()
    async def on_ready(self):
        print("Econ.cog loaded.")
    
    async def cog_check(self,ctx:commands.Context):
        a =await economy.is_registered(ctx.message.author.id)
        return a 
        
    

    
    
    
   
                    ###NECESSARY STUFF###
    
    ##Balance
    @commands.command(aliases = ['bal'])
    
    async def balance(self,ctx: commands.Context, member: discord.Member = None):
            
            member = member or ctx.message.author
            user_account = await economy.get_user(member.id)

            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name=f"{member.display_name}'s balance", value=f"""Bank: **{user_account.bank} coins**
                                                                            Wallet: **{user_account.wallet} coins**
                                                                            """)
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/saving-money-icon-stack-coins-money-bag-business-icon-isolated_138676-516.jpg?w=1380")
            await ctx.send(embed=embed)
            

    ##Withdraw
    @commands.command(aliases = ['w', 'wth'])
    

    async def withdraw(self,ctx: commands.Context, money: int, member: discord.Member = None):
        
        
        r = await economy.get_user(ctx.message.author.id)
        

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        if r.bank >= money:
            await economy.add_money(ctx.message.author.id, "wallet", money)
            await economy.remove_money(ctx.message.author.id, "bank", money)

            embed.add_field(name="Withdraw", value=f"Successfully withdrawn {money} coins!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed)

        else:

            embed.add_field(name="Withdraw", value=f"You don't have enough coins to withdraw!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed)
            
    ##Deposit
    @commands.command(aliases = ['d', 'dep'])
    async def deposit(self,ctx: commands.Context, money: int, member: discord.Member = None):
        
        
        r = await economy.get_user(ctx.message.author.id)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        if r.wallet >= money:
            await economy.add_money(ctx.message.author.id, "bank", money)
            await economy.remove_money(ctx.message.author.id, "wallet", money)

            embed.add_field(name="Deposit", value=f"Successfully deposited {money} coins!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed)

        else:

            embed.add_field(name="Deposit", value=f"You don't have enough coins to deposit!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed)


   

 

    ##Inventory    
    @commands.command(aliases = ['i', 'inv'])
    async def inventory(self,ctx:commands.Context, member: discord.Member = None):
        
        user = await economy.get_user(ctx.author.id)

        inv = user.items
        gacitems= [ f"{inv.count(i)} x {i.title()} " for i in gac_items if i in inv ]

        fitems = [ f"{inv.count(i)} x {i.title()} " for i in fishes_list if i in inv ]

        ritems = [ f"{inv.count(i)} x {i.title()} " for i in reg_items if i in inv ]

        fgear = [ f"{inv.count(i)} x {i.title()} " for i in f_items if i in inv ]

        gambaitems = [ f"{inv.count(i)} x {i.title()} " for i in dices if i in inv ]

        fcollect = [ f"{inv.count(i)} x {i.title()} " for i in artifacts if i in inv ]
        
        
        
        gacitems = "\n".join(gacitems) if len(gacitems) >= 1 else "Nothing in inventory"
        fitems = "\n".join(fitems) if len(fitems) >= 1 else "Nothing in inventory"
        ritems = "\n".join(ritems) if len(ritems) >= 1 else "Nothing in inventory"
        fgear =  "\n".join(fgear) if len(fgear) >= 1 else "Nothing in inventory"
        gambaitems =  "\n".join(gambaitems) if len(gambaitems) >= 1 else "Nothing in inventory"
        fcollect =  "\n".join(fcollect) if len(fcollect) >= 1 else "Nothing in inventory"
        
        
        embed = discord.Embed(title= "Inventory", description= "Inventory includes:", color=ctx.author.color)
        embed.add_field(name = "Items", value = ritems)
        embed.add_field(name = "Fishes", value = fitems)
        embed.add_field(name= "Gacha Collectibles", value = gacitems)
        embed.add_field(name = "Fishing Gear", value = fgear)
        embed.add_field(name = "Gamba Items", value = gambaitems)
        embed.add_field(name = "Sea Artifacts", value = fcollect)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-biting-pencil-with-bag-apple-cartoon-vector-icon-illustration-animal-education-icon-concept-flat-cartoon-style_138676-2589.jpg?w=1380")
        await ctx.send(embed = embed)

                    ###MONEY AND GAMES STUFF###

    ##Daily
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    
    async def daily(self,ctx: commands.Context, member: discord.Member = None):
        user = await economy.get_user(ctx.message.author.id)
        random_amount = random.randint(10, 100)
        await economy.add_money(ctx.message.author.id, "wallet", random_amount)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name=f"Reward", value=f"Successfully claimed reward! \n {random_amount} coins added to your wallet!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed)

    
    @commands.command(aliases = ['richest', 'leader', 'lb'])
    async def leaderboard(self,ctx:commands.Context):

        db = sqlite3.connect("database.db")

        cursor = db.cursor()

        cursor.execute(f"SELECT id, bank , wallet FROM economy ORDER by bank DESC, wallet DESC LIMIT 10")
     
        data = cursor.fetchall()
       
        
        
        if data:
            embed = discord.Embed(title= "Leaderboard")
            count = 0
            for table in data:
                count += 1
                user_id = table[0]
                user= await self.bot.fetch_user(user_id)
                coins = table[1] + table[2]
                embed.add_field(name = f"{count}. {user}", value=f"Coins- **{coins}**", inline=False )
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
            embed.set_author(name = "KikiVerse Richest")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/investment-statistic-with-money-illustration-growth-investment-finance-business-icon-concept-white-isolated_138676-619.jpg?w=1380")
            return await ctx.send(embed=embed)
        return await ctx.send("There are no users stored in the leaderboard")
        


    ##Welcome
    @commands.command()
    async def welcome(self, ctx:commands.Context):
        try:
            await economy.is_registered(ctx.message.author.id)
            await economy.is_cregistered(ctx.message.author.id)
            await economy.is_lvlregistered(ctx.message.author.id)
            user1 = await economy.get_user(ctx.message.author.id)
            user2 = await economy.get_c_user(ctx.message.author.id)
            user3 = await economy.get_user_lvl(ctx.message.author.id)
        except: 
            return user1, user2, user3
        control = user1.control
        
        if control == 0:
            await economy.set_money(ctx.message.author.id,"control",1)
            await economy.add_item(ctx.message.author.id, "token")
            await economy.add_money(ctx.message.author.id,"wallet", 100)

            embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89))
            embed.set_author(name = "Kiki Bot")
            embed.add_field(name ="You have claimed your welcome gift.", value=f"A gacha **token** and **100** coins added to your wallet.")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-singing-with-microphone-cartoon_138676-2312.jpg?w=1380")
            await ctx.send(embed=embed)
        elif control == 1:
            embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89))
            embed.set_author(name = "Kiki Bot")
            embed.add_field(name ="You have already claimed your welcome gift.", value="Start your journey with minigames.")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-singing-with-microphone-cartoon_138676-2312.jpg?w=1380")
            await ctx.send(embed=embed)
           
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def give(self,ctx:commands.Context,target:discord.Member,value:str,amount:int):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        ec = ["wallet","bank"]
        lvl = ["xp","level","points"]
        target = ctx.message.mentions[0]

        if value =="wallet":
            await economy.add_money(target.id,"wallet",amount)
            embed.add_field(name=f"You have succesfully given {target.display_name} Kiki Coins.", value=f"{amount} Kiki Coins added to {target.display_name}'s wallet.")
        elif value =="coins":
            await economy.add_money(target.id,"wallet",amount)
            embed.add_field(name=f"You have succesfully given {target.display_name} Kiki Coins.", value=f"{amount} Kiki Coins added to {target.display_name}'s wallet.")
        elif value == "bank":
            await economy.add_money(target.id,"bank",amount)
            embed.add_field(name=f"You have succesfully given {target.display_name} Kiki Coins.", value=f"{amount} Kiki Coins added to {target.display_name}'s bank.")
        elif value == "xp":
            await economy.add_xp(target.id,"xp",amount)
            embed.add_field(name=f"You have succesfully given {target.display_name} XP.", value=f"{amount} XP added to {target.display_name}'s progress.")
        elif value =="level":
            await economy.add_level(target.id,"level",amount)
            embed.add_field(name=f"You have succesfully given {target.display_name} Level.", value=f"{amount} Level added to {target.display_name}'s progress.")
        elif value =="points":
            await economy.add_level(target.id,"points",amount)
            embed.add_field(name=f"You have succesfully given {target.display_name} Points.", value=f"{amount} Points added to {target.display_name}'s progress.")
        else:
            embed.add_field(name="You have to enter wallet, coins, bank, xp, level or points.", value="Try again.")
            return
        
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
        embed.set_author(name = "Kiki Bot Admin")
        await ctx.send(embed=embed)        
    




async def setup(bot):
    await bot.add_cog(econ(bot))

