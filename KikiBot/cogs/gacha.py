from tracemalloc import stop
import discord
import os
import asyncio
from discord.ext import commands, tasks
from discord.ui import Button, View
import sqlite3
import random
from time import sleep
from DiscordEconomy.Sqlite import Economy
from lists.gachalist import *
from main import economy




class MyView(discord.ui.View):

        def __init__(self, ctx):
               super().__init__(timeout=10)
               self.ctx = ctx
               self.value = None
        
        @discord.ui.button(label="Gacha", style=discord.ButtonStyle.green, emoji= "🎁" , custom_id="gacha")
       
        async def gbut1(self, interaction: discord.Interaction, button: discord.ui.Button):
            button1 = [x for x in self.children if x.custom_id== "cancel"][0]
            button2 = [x for x in self.children if x.custom_id=="gacha"][0]
    
            button1.label = "Summoning"
            button1.disabled = True
            button2.disabled = True
            
            embed =discord.Embed(color=discord.Color.random())
            embed =discord.Embed(title="Kiki Gods Have Sent the Gacha Machine", description="Gacha Machine Demanding Token")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-playing-ball-with-cat-food_138676-12.jpg?w=1800")
            embed.set_author(name="Kiki Gacha")
            
            
            
            
            await interaction.response.edit_message(embed=embed,view=self)
            self.value = "1"
            self.stop()
            
            
            
        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.blurple, emoji= "❌" , custom_id="cancel")
        async def gbut2(self, interaction: discord.Interaction, button: discord.ui.Button):
            button1 = [x for x in self.children if x.custom_id== "cancel"][0]
            button2 = [x for x in self.children if x.custom_id=="gacha"][0]
            
            button2.label= "Cancelled"
            button2.disabled = True
            button1.disabled = True
            

            
            
            
            embed =discord.Embed(color=discord.Color.random())
            embed =discord.Embed(title="Kiki Police Busted the Cultist Gathering", description="Summon Cancelled!")
            embed.set_author(name="Kiki Gacha FBI")
           
            
            await interaction.response.edit_message(embed=embed,view=self)
            
            self.value = "2"
            self.stop()

            
        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user !=self.ctx.author:
                embed =discord.Embed(color=discord.Color.random())
                embed =discord.Embed(title="The current screen is not yours.", description="Please try again")
                embed.add_field(name="Did you try earning your own coins?", value="Start with !daily and join the mini games.")
                embed.set_thumbnail(url="https://i.pinimg.com/originals/4f/c6/59/4fc659d1c70c6a5ded85595c8e19a3d8.png")
                embed.set_footer(text="***Summon screen belongs to {}***".format(self.ctx.author.name),icon_url= (self.ctx.author.avatar))
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False
            
            else:
                return True
            
            

class gacha(commands.Cog):
    def __init__ (self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Gacha.cog loaded.")
    
    async def cog_check(self,ctx:commands.Context):
        r =await economy.is_registered(ctx.message.author.id)
        return r 

    @commands.command(aliases = ['g','claw'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    
    async def gacha(self,ctx: commands.Context):
        user_id= ctx.message.author.id
        item = "token"
        item = item.lower()
        

        view = MyView(ctx)
        
        data = await economy.get_user(user_id)
        inv = data.items
            
        if item in inv:


            common = (33.0)
            uncommon = (22.5)
            rare = (12.5)
            epic = (5.0)
            legendary = (1.5)
            chance_roll = random.uniform(0, 100)
            
            if chance_roll >= common:

                cname = "common" 
                gitem = gacha_list["Common"].items()
                a = random.choice(list(gitem))
                name = a[0].lower()
                oput = f"{cname.title()} {a[1]['type'].title()} {a[0].title()}"          
            
                        
            elif  chance_roll < common and chance_roll >= uncommon:
                cname = "uncommon" 
                gitem = gacha_list["Uncommon"].items()
                a = random.choice(list(gitem))
                name = a[0].lower()
                oput = f"{cname.title()} {a[1]['type'].title()} {a[0].title()}"              
                
                        
                        
            elif chance_roll < uncommon and chance_roll>=rare:
                            
                cname = "rare" 
                gitem = gacha_list["Rare"].items()
                a = random.choice(list(gitem))
                name = a[0].lower()
                oput = f"{cname.title()} {a[1]['type'].title()} {a[0].title()}" 
                        
                    
                    
            elif chance_roll < rare and chance_roll>=epic:

                cname = "epic" 
                gitem = gacha_list["Epic"].items()
                a = random.choice(list(gitem))
                name = a[0].lower()
                oput = f"{cname.title()} {a[1]['type'].title()} {a[0].title()}" 
                        
                        
                        
            elif chance_roll < epic and chance_roll >=legendary:
                        
                cname = "legendary" 
                gitem = gacha_list["Legendary"].items()
                a = random.choice(list(gitem))
                name = a[0].lower()
                oput = f"{cname.title()} {a[1]['type'].title()} {a[0].title()}" 
                        
                        

            elif chance_roll < legendary:
                cname = "mega legendary" 
                gitem = gacha_list["Mega Legendary"].items()
                a = random.choice(list(gitem))
                name = a[0].lower()
                oput = f"{cname.title()} {a[1]['type'].title()} {a[0].title()}" 

            gembed = discord.Embed(color=discord.Color.random())
            gembed.set_author(name="Kiki Gacha")
            gembed.set_footer(text="Summon invoked by {}".format(ctx.message.author.name),icon_url= (ctx.message.author.avatar))
            gembed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-play-box-cartoon-icon-illustration-animal-icon-concept-isolated-flat-cartoon-style_138676-1361.jpg?w=1380")            
            await ctx.send(embed=gembed,view=view)  
                       
        

            await view.wait()
            if view.value == "1":
                    
                        embed2 =discord.Embed(color=discord.Color.random())
                        embed2 =discord.Embed(title="Gods Have Spoken the Words of GAMBA", description="Kiki Gods accepted your token offer!")
                        embed2.set_image(url="https://media1.tenor.com/images/9ae39653ad1baf236fcede393ac3613d/tenor.gif?itemid=26437577")
                        msg = await ctx.send(embed=embed2)
                        await asyncio.sleep(3)
                        embed2 =embed2.add_field(name= "You got", value = oput)  
                        embed2.set_author(name="SUCCESS!")
                        embed2.set_footer(text="Summon invoked by {}".format(ctx.message.author.name),icon_url= (ctx.message.author.avatar))
                        embed2.set_thumbnail(url="https://img.freepik.com/premium-vector/claw-machine-with-cute-teddy-bear-illustration_138676-142.jpg?w=1800")
                        await msg.edit (embed=embed2)
                        

                        if item in inv:
                            await economy.remove_item(user_id,item)
                            await economy.add_item(user_id,name)
                        True

        else:
                fembed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
                fembed.add_field(name="Error", value=f"You don't have the necessary sacrifice token!. Try buying from !shop")
                fembed.set_footer(text=f"Invoked by {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
                await ctx.send(embed=fembed)
                False

    
           
                      
           
        


            
        
async def setup(bot):
    await bot.add_cog(gacha(bot))
   