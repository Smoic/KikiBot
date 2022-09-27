from distutils.log import error
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
import tracemalloc
from main import economy, on_command_error

class rpsview (discord.ui.View):
        def __init__(self,ctx):
            super().__init__(timeout=10)
            self.ctx = ctx
            self.value = None
            


        @discord.ui.button(label="Rock", style=discord.ButtonStyle.green, emoji= "🤘" , custom_id="rock")
        
        async def rock (self, interaction: discord.Interaction, button=discord.ui.Button):
            button1 = [x for x in self.children if x.custom_id== "rock"][0]
            button2 = [x for x in self.children if x.custom_id=="paper"][0]
            button3 = [x for x in self.children if x.custom_id=="sgun"][0]
            button1.label = "Rock"
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            embed =discord.Embed(color=discord.Color.random())
            embed =discord.Embed(title="You choose rock!", description="Time to Smash!")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-rocker-sing-with-guitar-cartoon-vector-icon-illustration-animal-music-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3794.jpg?w=1380")
            embed.set_author(name="Kiki RPS")

            await interaction.response.edit_message(embed=embed,view=self)
            self.value = "1"
            self.stop()  

        @discord.ui.button(label="Paper", style=discord.ButtonStyle.blurple, emoji= "🧻" , custom_id="paper")
        async def paper (self, interaction: discord.Interaction, button=discord.ui.Button):
            button1 = [x for x in self.children if x.custom_id== "rock"][0]
            button2 = [x for x in self.children if x.custom_id=="paper"][0]
            button3 = [x for x in self.children if x.custom_id=="sgun"][0]
            button2.label = "Paper"
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            embed =discord.Embed(color=discord.Color.random())
            embed =discord.Embed(title="You choose paper!", description="Time to roll into paper!")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-play-toilet-tissue-paper-illustration-mascot-cartoon-character-animal-isolated_138676-1049.jpg?w=1380")
            embed.set_author(name="Kiki RPS")

            await interaction.response.edit_message(embed=embed,view=self)
            self.value = "2"
            self.stop()   


        @discord.ui.button(label="Shotgun", style=discord.ButtonStyle.red, emoji= "🔫" , custom_id="sgun")
        async def sgun (self, interaction: discord.Interaction, button=discord.ui.Button):
            button1 = [x for x in self.children if x.custom_id== "rock"][0]
            button2 = [x for x in self.children if x.custom_id=="paper"][0]
            button3 = [x for x in self.children if x.custom_id=="sgun"][0]
            button3.label = "Shotgun"
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            embed =discord.Embed(color=discord.Color.random())
            embed =discord.Embed(title="You choose shotgun!", description="Weapons actually illegal, so why not try a bat instead!")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-bad-cat-wearing-suit-sunglasses-with-baseball-bat-cartoon-icon-illustration-animal-fashion-icon-concept-isolated-flat-cartoon-style_138676-2170.jpg?w=1380&t=st=1661625042~exp=1661625642~hmac=2e67ed3b44a29312a91e3abea41d468214e2c5f0b0d152f4419c9d7bd871d656")
            embed.set_author(name="Kiki RPS")

            await interaction.response.edit_message(embed=embed,view=self)
            self.value = "3"
            self.stop()   
          
        
        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user != self.ctx.author:
                embed =discord.Embed(color=discord.Color.random())
                embed =discord.Embed(title="The current screen is not yours.", description="Please try again")
                embed.add_field(name="Did you try earning your own coins?", value="Start with !daily and join the mini games.")
                embed.set_footer(text="***Summon screen belongs to {}***".format(self.ctx.author.name),icon_url= (self.ctx.author.avatar))
                embed.set_thumbnail(url="https://i.pinimg.com/originals/4f/c6/59/4fc659d1c70c6a5ded85595c8e19a3d8.png")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False
            
            else:
                return True
    
        
            
    



class games (commands.Cog):
    def __init__(self,bot):
        self.bot = bot
 


    async def cog_check(self,ctx:commands.Context):
        r =await economy.is_registered(ctx.message.author.id)
        return r 
    
    async def cog_check(self,ctx:commands.Context):
        a =await economy.is_lvlregistered(ctx.message.author.id)
        return a 
       
      
    @commands.Cog.listener()
    async def on_ready(self):
        
        print("Games.cog loaded.")

    



##Dice

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def dice (self,ctx:commands.Context, amount:int):
        user = await economy.get_user(ctx.message.author.id)
        items = user.items
        xp = random.randint(1,amount)
        doubles = ["(1,1)","(2,2)","(3,3)","(4,4)","(5,5)","(6,6)"]
        embed =discord.Embed(color=discord.Color.random())
        embed =discord.Embed(title="***Will you get lucky?***", description="Shake & Roll!")
        embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/lg/307/game-die_1f3b2.png")
        embed.set_author(name="Kiki Gamba Dice")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)

        if amount > 10:
            embed.add_field(name = "You can't bet more than 10 coins!", value="Try lowering your bet!", inline= False)
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            return await ctx.send(embed=embed)
        if not user.wallet >= amount:
            embed.add_field(name = "You don't have enough coins to gamba!", value="Try next time!", inline= False)
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            return await ctx.send(embed=embed)

        msg = await ctx.send(embed=embed)
        dicegear = [ f"{i}" for i in dices if i in items]
        count = len(dicegear)
        control = []
        dc = 0
        udice = "dice" if  not dicegear else random.choice(dicegear).title()

        while count != 0:
            for i in range(count):
                if "bone dice" in dicegear and "1" not in control:
                    control.append("1")
                    dc = dc + 1
                else:
                    dc = dc+0
                if "skull dice" in dicegear and "2" not in control:
                    control.append("2")
                    dc = dc + 1
                else:
                    dc = dc +0
                if "metal dice" in dicegear and "3" not in control:
                    control.append("3")
                    dc = dc + 1
                else:
                    dc = dc+ 0
                if "bullet dice" in dicegear and "4" not in control:
                    control.append("4")
                    dc= dc + 2
                else:
                    dc = dc +0
                if "fantasy dice" in dicegear and "5" not in control:
                    control.append("5")
                    dc = dc + 3
                else:
                    dc = dc + 0
                if "lucky dice" in dicegear and "6" not in control:
                    control.append("6")
                    dc = dc + 3
                else:
                    dc = dc + 0
                if "rgb dice" in dicegear and "7" not in control:
                    control.append("7")
                    dc = dc + 5
                else:
                    dc = dc + 0
            break
        
        if dc > 0:
            chance = random.randint(1,100)
            if chance > 91-dc:
                embed.clear_fields()
                embed.add_field(name = "You sneakiki!", value=f"Your {udice} allowed you to cheat this time!")
                await msg.edit(embed=embed)
                ud1 = random.randint(4,6)
                ud2 = random.randint(5,6)
                
            else:
                ud1 = random.randint(1,6)
                ud2 = random.randint(1,6)
        else:
            ud1 = random.randint(1,6)
            ud2 = random.randint(1,6)        
        ut = ud1 + ud2
        uroll = (ud1,ud2)  

        
        

        bd1 = random.randint(1,6)
        bd2 = random.randint(1,6)
        bt = bd1 + bd2
        await asyncio.sleep(3)
        embed.clear_fields()
        embed =discord.Embed(color=discord.Color.random())
        embed.add_field(name=f"🎲You have rolled your {udice} 🎲", value = f"{ud1} and {ud2}", inline = False)

        await msg.edit(embed=embed)
        await asyncio.sleep(3)

        embed.add_field(name="🎲Kiki Bot has rolled it's dice!🎲", value= f"{bd1} and {bd2}", inline=False)
        
        await msg.edit(embed=embed)
        await asyncio.sleep(3)

        if ut > bt:
            if uroll in doubles:
                await economy.add_money(ctx.message.author.id, "wallet", amount*2 )
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                embed.add_field(name = "You won!", value= f"{amount*2} coins added to your wallet!")
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-cool-cat-wearing-eyeglasses-hoodie-cartoon-vector-icon-illustration-animal-fashion-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4234.jpg?w=1380&t=st=1661818093~exp=1661818693~hmac=210c0621c469428b55dc149e54b50f179368ce9fff83a3f6d46c8af132cf88a9")
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await msg.edit(embed=embed)
            else:
                await economy.add_money(ctx.message.author.id, "wallet", amount)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                embed.add_field(name = "You won!", value= f"{amount} coins added to your wallet!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-cool-cat-wearing-eyeglasses-hoodie-cartoon-vector-icon-illustration-animal-fashion-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4234.jpg?w=1380&t=st=1661818093~exp=1661818693~hmac=210c0621c469428b55dc149e54b50f179368ce9fff83a3f6d46c8af132cf88a9")
                await msg.edit(embed=embed)
        elif bt > ut:
            await economy.remove_money(ctx.message.author.id, "wallet", amount )
            await economy.add_xp(ctx.message.author.id, "xp", xp)
            embed.add_field(name = "You lost!", value= f"{amount} coins taken from your wallet!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-cat-get-mad-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4075.jpg?w=1380&t=st=1661818154~exp=1661818754~hmac=73fdab902a966178e6a19c3610ba2e73682021d5432022ce9e1ed9c8fae69254")
            await msg.edit(embed=embed)
        elif ut == bt:
            
            embed.add_field(name = "No winner!", value= "Better luck next time!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-lucky-cat-sleeping-with-gold-coin-cartoon-vector-icon-illustration-animal-business-isolated_138676-4859.jpg?w=1380")
            await msg.edit(embed=embed)

    

##RPS
    

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def rps(self,ctx:commands.Context,amount:int):
        user = await economy.get_user(ctx.message.author.id)
        choices = [1, 2, 3]
        xp = random.randint(1,amount)
        view = rpsview(ctx)
        embed =discord.Embed(color=discord.Color.random())
        embed =discord.Embed(title="***Rock Paper Shotgun!!***", description="Get your weapons ready!")
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-ninja-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4232.jpg?w=1380")
        embed.set_author(name="Kiki RPS")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
        msg = await ctx.send(embed=embed,view=view)

        if amount > 10:
                embed =discord.Embed(color=discord.Color.random())
                embed = discord.Embed(title= "You can't bet more than 10 coins!", description="Try lowering your bet!")
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-ninja-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4232.jpg?w=1380")
                embed.set_author(name="Kiki RPS")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                view.clear_items()
                view.stop()
                return await msg.edit (embed=embed,view=view)
           
       
        if not user.wallet >= amount:
            embed =discord.Embed(color=discord.Color.random())
            embed = discord.Embed(title= "You don't have enough coins to gamba!", description="Try next time!")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-ninja-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4232.jpg?w=1380")
            embed.set_author(name="Kiki RPS")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            view.clear_items()
            view.stop()
            return await msg.edit(embed=embed,view=view)
        
        await view.wait()

        if view.value == "1":
            usec = choices[0]
            
            csec = random.choice(choices)
            

            if usec == csec:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.add_field(name="You both choose rock.", value="It's a double smash... No winners.")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You didn't lose any coins!", value= f"{amount} coins given back to your wallet!")
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-rocker-sing-with-guitar-cartoon-vector-icon-illustration-animal-music-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3794.jpg?w=1380")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await msg.edit(embed=embed,view=view)
                
            
            elif csec == 2:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.add_field(name="Bot chosen paper.", value="Your rock has been neutralized. You lost.")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have lost some coins!", value= f"{amount} coins taken from your wallet!")
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-rocker-sing-with-guitar-cartoon-vector-icon-illustration-animal-music-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3794.jpg?w=1380")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await economy.remove_money(ctx.message.author.id, "wallet", amount )
                await msg.edit(embed=embed,view=view)


            elif csec == 3:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-rocker-sing-with-guitar-cartoon-vector-icon-illustration-animal-music-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3794.jpg?w=1380")
                embed.add_field(name="Bot has brought a baseball bat.", value="You throw your rock to break the bat! You won.")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have gained some coins!", value= f"{amount} coins added to your wallet!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await economy.add_money(ctx.message.author.id,"wallet",amount)
                await msg.edit(embed=embed,view=view)

        
        
        if view.value == "2":
            usec = choices[1]
            
            csec = random.choice(choices)
            

            if usec == csec:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.add_field(name="You both choose paper.", value="You both rolled on papers... No winners.")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You didn't lose any coins!", value= f"{amount} coins given back to your wallet!")
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-play-toilet-tissue-paper-illustration-mascot-cartoon-character-animal-isolated_138676-1049.jpg?w=1380")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await msg.edit(embed=embed,view=view)
            
            elif csec == 1:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.add_field(name="Bot chosen rock.", value="Your have neutralized the rock. You won!")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have gained some coins!", value= f"{amount} coins added to your wallet!")
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-play-toilet-tissue-paper-illustration-mascot-cartoon-character-animal-isolated_138676-1049.jpg?w=1380")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await economy.add_money(ctx.message.author.id,"wallet",amount)
                await msg.edit(embed=embed,view=view)

            elif csec == 3:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.add_field(name="Bot has brought a baseball bat.", value="Your paper was inefficient to baseball bat! You lost.")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have lost some coins!", value= f"{amount} coins taken from your wallet!")
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-play-toilet-tissue-paper-illustration-mascot-cartoon-character-animal-isolated_138676-1049.jpg?w=1380")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await economy.remove_money(ctx.message.author.id, "wallet", amount )
                await msg.edit(embed=embed,view=view)
        
        if view.value == "3":
            usec = choices[2]
            
            csec = random.choice(choices)
            

            if usec == csec:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-bad-cat-wearing-suit-sunglasses-with-baseball-bat-cartoon-icon-illustration-animal-fashion-icon-concept-isolated-flat-cartoon-style_138676-2170.jpg?w=1380&t=st=1661625042~exp=1661625642~hmac=2e67ed3b44a29312a91e3abea41d468214e2c5f0b0d152f4419c9d7bd871d656")
                embed.add_field(name="You both choose shotgun.", value="It's a kiki bat fight. No winners.")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You didn't lose any coins!", value= f"{amount} coins given back to your wallet!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await msg.edit(embed=embed,view=view)
            
            elif csec == 2:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-bad-cat-wearing-suit-sunglasses-with-baseball-bat-cartoon-icon-illustration-animal-fashion-icon-concept-isolated-flat-cartoon-style_138676-2170.jpg?w=1380&t=st=1661625042~exp=1661625642~hmac=2e67ed3b44a29312a91e3abea41d468214e2c5f0b0d152f4419c9d7bd871d656")
                embed.add_field(name="Bot chosen paper.", value="Your have smacked the paper with your bat! You won!")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have gained some coins!", value= f"{amount} coins added to your wallet!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await economy.add_money(ctx.message.author.id,"wallet",amount)
                await msg.edit(embed=embed,view=view)

            elif csec == 1:
                await asyncio.sleep(3)
                embed.clear_fields()
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-bad-cat-wearing-suit-sunglasses-with-baseball-bat-cartoon-icon-illustration-animal-fashion-icon-concept-isolated-flat-cartoon-style_138676-2170.jpg?w=1380&t=st=1661625042~exp=1661625642~hmac=2e67ed3b44a29312a91e3abea41d468214e2c5f0b0d152f4419c9d7bd871d656")
                embed.add_field(name="Bot has brought a rock.", value="Your baseball bat wasn't hard enough to crack the bat! You lost.")
                embed.add_field(name = chr(173), value = chr(173))
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have lost some coins!", value= f"{amount} coins taken from your wallet!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await economy.add_xp(ctx.message.author.id, "xp", xp)
                await economy.remove_money(ctx.message.author.id, "wallet", amount )
                await ctx.send(embed=embed,view=view)


    ##Horse Gamba
    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def horse(self,ctx: commands.Context, amount: int, member: discord.Member = None):
        user = await economy.get_user(ctx.author.id)
        r = await economy.get_user_lvl(ctx.message.author.id)
        gamlvl = r.gamble
        
        embed =discord.Embed(color=discord.Color.random())
        

        
       


        if gamlvl >= 5:
            xp = random.randint(1,amount)
            if not user.wallet >= amount:
                embed =discord.Embed(title= "You don't have enough coins to gamba!", description="Try next time!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                embed.set_author(name = "Kiki Gamba")
                return await ctx.send(embed=embed)
            if amount > 10:
                embed.add_field(name = "You can't bet more than 10 coins!", value="Try lowering your bet!", inline= False)
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                return await ctx.send(embed=embed)

            author_path = [":horse_racing:", ":blue_square:", ":blue_square:", ":blue_square:", ":blue_square:",
                        ":blue_square:",
                        ":blue_square:", ":blue_square:", ":blue_square:", ":blue_square:", "  :checkered_flag:"]

            enemy_path = [":horse_racing:", ":red_square:", ":red_square:", ":red_square:", ":red_square:", ":red_square:",
                        ":red_square:", ":red_square:", ":red_square:", ":red_square:", "  :checkered_flag:"]

            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Kiki Gamba Horse Racing")
            embed.add_field(name = "Welcome to Horse Gamba", value="Encourage your horsie to finish!")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/horse-racing-cartoon-icon-illustration_138676-2255.jpg?w=1380&t=st=1661823931~exp=1661824531~hmac=bd2ba0033771256c1508c793abece31a0110be582dcfec583990dacb7c880295")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            msg = await ctx.send(embed=embed)

            await asyncio.sleep(3)
            embed.clear_fields()
            embed.set_author(name="Kiki Gamba Horse Racing STARTED")
            embed.add_field(name="You:", value="".join(author_path), inline=False)
            embed.add_field(name=f"Bot:", value="".join(enemy_path),
                            inline=False)
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            await msg.edit(embed=embed)
            await asyncio.sleep(3)

            author_path[0] = ":blue_square:"
            enemy_path[0] = ":red_square:"

            author_path_update = random.randint(2, 6)
            enemy_path_update = random.randint(2, 6)

            author_path[author_path_update] = ":horse_racing:"
            enemy_path[enemy_path_update] = ":horse_racing:"

            embed.clear_fields()
            embed.add_field(name="You:", value="".join(author_path), inline=False)
            embed.add_field(name=f"Bot:", value="".join(enemy_path),
                            inline=False)

            await msg.edit(embed=embed)
            await asyncio.sleep(3)

            author_path[author_path_update] = ":blue_square:"
            enemy_path[enemy_path_update] = ":red_square:"

            author_path_update = random.randint(author_path_update, 9)
            enemy_path_update = random.randint(enemy_path_update, 9)

            author_path[author_path_update] = ":horse_racing:"
            enemy_path[enemy_path_update] = ":horse_racing:"

            embed.clear_fields()
            embed.add_field(name="You:", value="".join(author_path), inline=False)
            embed.add_field(name=f"Bot:", value="".join(enemy_path),
                            inline=False)
            await msg.edit(embed=embed)

            if author_path_update > enemy_path_update:
                await economy.add_money(ctx.message.author.id ,"wallet", amount)
                await economy.add_xp(ctx.message.author.id,"xp",xp)
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have gained some coins!", value= f"{amount} coins added to your wallet!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(url = "https://img.freepik.com/free-vector/horse-racing-cartoon-icon-illustration_138676-2255.jpg?w=1380&t=st=1661823931~exp=1661824531~hmac=bd2ba0033771256c1508c793abece31a0110be582dcfec583990dacb7c880295")
                embed.set_author(name = "You won your bet on Horse Racing!")
                await msg.edit(embed=embed)

            else:
                await economy.remove_money(ctx.message.author.id, "wallet", amount)
                await economy.add_xp(ctx.message.author.id,"xp",xp)
                embed.add_field(name = "You have gained some xp!", value= f"{xp} xp added to your progress!")
                embed.add_field(name = "You have lost some coins!", value= f"{amount} coins taken from your wallet!")
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/horse-racing-cartoon-icon-illustration_138676-2255.jpg?w=1380&t=st=1661823931~exp=1661824531~hmac=bd2ba0033771256c1508c793abece31a0110be582dcfec583990dacb7c880295")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                embed.set_author(name = "You lost your bet on Horse Racing!")
                await msg.edit(embed=embed)
        
        else:
            embed =discord.Embed(color=discord.Color.random())
            embed.add_field(name ="Your gamba level is not enough for Horse Gamba", value = f"You need to be at least **level 5** to bet on horses. \n\n Your current gamba level is **{gamlvl}**.")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/horse-racing-cartoon-icon-illustration_138676-2255.jpg?w=1380&t=st=1661823931~exp=1661824531~hmac=bd2ba0033771256c1508c793abece31a0110be582dcfec583990dacb7c880295")
            embed.set_author(name="Gamba")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed)
            
    

















async def setup(bot):

    await bot.add_cog(games(bot))