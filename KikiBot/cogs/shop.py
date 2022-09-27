from email import message
import numbers
from sre_compile import isstring
from tracemalloc import stop
from typing import ValuesView
import discord
import os
import asyncio
from discord.ext import commands, tasks
from discord.ui import Button, View , Select
import sqlite3
import random
from time import sleep
from DiscordEconomy.Sqlite import Economy
from lists.itemslist import *
from lists.fishinglist import *
import tracemalloc
from main import economy


class GeneralShop(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        
    @discord.ui.button(label = "General Shop", style=discord.ButtonStyle.green, custom_id="gen", emoji="🛒")
    async def gs1(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id== "gen"][0]
        button2 = [x for x in self.children if x.custom_id=="gacha"][0]
        button3 = [x for x in self.children if x.custom_id=="gamba"][0]
        button4 = [x for x in self.children if x.custom_id=="quit"][0]
        button5 = [x for x in self.children if x.custom_id == "mall"][0]       
        button1.label = "General Shop"
        button1.disabled = True
        button2.disabled = False
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False
        
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="General Shop")

        for item in shop_list["Items"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0], value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                

        await interaction.response.edit_message(embed = embed, view=self)

    @discord.ui.button(label = "Gacha Shop", style=discord.ButtonStyle.green, custom_id="gacha", emoji="🎟")
    async def gs2(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id== "gen"][0]
        button2 = [x for x in self.children if x.custom_id=="gacha"][0]
        button3 = [x for x in self.children if x.custom_id=="gamba"][0]
        button4 = [x for x in self.children if x.custom_id=="quit"][0]
        button5 = [x for x in self.children if x.custom_id == "mall"][0]    
        button2.label = "Gacha Shop"
        button1.disabled = False
        button2.disabled = True
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False
        
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="General Shop")

        for item in gacha_list["Items"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0], value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        
        await interaction.response.edit_message(embed = embed, view=self)
    
    @discord.ui.button(label = "Gamba Shop", style=discord.ButtonStyle.green, custom_id="gamba", emoji="🎲")
    async def gs3(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id== "gen"][0]
        button2 = [x for x in self.children if x.custom_id=="gacha"][0]
        button3 = [x for x in self.children if x.custom_id=="gamba"][0]
        button4 = [x for x in self.children if x.custom_id=="quit"][0]
        button5 = [x for x in self.children if x.custom_id == "mall"][0]   
        button2.label = "Gamba Shop"
        button1.disabled = False
        button2.disabled = True
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False
        
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="General Shop")

        for item in dice_list["Items"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0], value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        
        await interaction.response.edit_message(embed = embed, view=self)



    

    @discord.ui.button(label = "Quit", style=discord.ButtonStyle.red, custom_id="quit", emoji="✖")
    async def gs4(self,interaction:discord.Interaction, button:discord.ui.Button):
        self.clear_items()
        self.stop()
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Come back soon!")
        embed.add_field(name = "You have quit from the shop!", value="Don't forget to pack your items!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                        icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
        await interaction.response.edit_message(embed = embed, view=None)

    @discord.ui.button(label = "Mall", style=discord.ButtonStyle.grey, custom_id="mall", emoji="🛒")
    async def gs5(self,interaction:discord.Interaction, button:discord.ui.Button):
        view = SelectView()
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Return to Mall!")
        embed.add_field(name = "You have return to the mall entrance!", value="Time to shop for new items!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                        icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
        await interaction.response.edit_message(embed = embed, view=view)

    



class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        
        

    @discord.ui.button(label = "Stream Fish Shelf", style=discord.ButtonStyle.green, custom_id="stream", emoji="🐡")
    async def menu1(self,interaction:discord.Interaction, button:discord.ui.Button):

        button1 = [x for x in self.children if x.custom_id== "stream"][0]
        button2 = [x for x in self.children if x.custom_id=="dock"][0]
        button3 = [x for x in self.children if x.custom_id=="oceanic"][0] 
        button4 = [x for x in self.children if x.custom_id=="quit"][0]   
        button5 = [x for x in self.children if x.custom_id=="mall"][0]  
        button1.label = "Stream Fish"
        button1.disabled = True
        button2.disabled = False
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False

        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Stream Fish")

        for item in fishes_shop["Stream Fishes"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        await interaction.response.edit_message(embed = embed, view=self)
        
            
        
           
    
    @discord.ui.button(label = "Dock Fish Shelf", style=discord.ButtonStyle.grey, custom_id="dock", emoji="🐟")
    async def menu2(self,interaction:discord.Interaction, button:discord.ui.Button):
        
        button1 = [x for x in self.children if x.custom_id== "stream"][0]
        button2 = [x for x in self.children if x.custom_id=="dock"][0]
        button3 = [x for x in self.children if x.custom_id=="oceanic"][0]
        button4 = [x for x in self.children if x.custom_id=="quit"][0]    
        button5 = [x for x in self.children if x.custom_id=="mall"][0]  
        button2.label = "Dock Fish"
        button1.disabled = False
        button2.disabled = True
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Dock Fishes")

        for item in fishes_shop["Dock Fishes"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        await interaction.response.edit_message(embed = embed, view=self)
        
           
    
    @discord.ui.button(label = "Oceanic Fish Shelf", style=discord.ButtonStyle.blurple, custom_id="oceanic", emoji="🦈")
    async def menu3(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id== "stream"][0]
        button2 = [x for x in self.children if x.custom_id=="dock"][0]
        button3 = [x for x in self.children if x.custom_id=="oceanic"][0]  
        button4 = [x for x in self.children if x.custom_id=="quit"][0]
        button5 = [x for x in self.children if x.custom_id=="mall"][0]  
        button3.label = "Oceanic Fish"
        button1.disabled = False
        button2.disabled = False
        button3.disabled = True
        button4.disabled = False
        button5.disabeld = False

        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Oceanic Fish")

        for item in fishes_shop["Oceanic Fishes"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        await interaction.response.edit_message(embed = embed, view=self)

    @discord.ui.button(label = "Quit", style=discord.ButtonStyle.red, custom_id="quit", emoji="✖")
    async def menu4(self,interaction:discord.Interaction, button:discord.ui.Button):
        self.clear_items()
        self.stop()
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Come back soon!")
        embed.add_field(name = "You have quit from the shop!", value="Don't forget to pack your items!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                        icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
        await interaction.response.edit_message(embed = embed, view=None)

    @discord.ui.button(label = "Mall", style=discord.ButtonStyle.grey, custom_id="mall", emoji="🛒")
    async def menu5(self,interaction:discord.Interaction, button:discord.ui.Button):
        view = SelectView()
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Return to Mall!")
        embed.add_field(name = "You have return to the mall entrance!", value="Time to shop for new items!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                        icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
        await interaction.response.edit_message(embed = embed, view=view)

   
    
class FishingGearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        
        

    @discord.ui.button(label = "Fishing Rods", style=discord.ButtonStyle.green, custom_id="rods", emoji="🎣")
    async def fg1(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id=="rods"][0]
        button2 = [x for x in self.children if x.custom_id=="nets"][0]
        button3 = [x for x in self.children if x.custom_id=="fbal"][0]  
        button4 = [x for x in self.children if x.custom_id=="ship"][0]
        button5 = [x for x in self.children if x.custom_id=="quit"][0]
        button6 = [x for x in self.children if x.custom_id=="mall"][0]  

        button1.disabled= True
        button2.disabled = False
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False
        button6.disabled = False

        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Fishing Rods")

        for item in fishing_gear["Rods"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**
                                                                    Required Level: **{item[1]['reqlevel']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        await interaction.response.edit_message(embed = embed, view=self)

    @discord.ui.button(label = "Fishing Nets", style=discord.ButtonStyle.green, custom_id="nets", emoji="🐋")
    async def fg2(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id=="rods"][0]
        button2 = [x for x in self.children if x.custom_id=="nets"][0]
        button3 = [x for x in self.children if x.custom_id=="fbal"][0]  
        button4 = [x for x in self.children if x.custom_id=="ship"][0]
        button5 = [x for x in self.children if x.custom_id=="quit"][0]
        button6 = [x for x in self.children if x.custom_id=="mall"][0]   

        button1.disabled = False
        button2.disabled = True
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False
        button6.disabled = False

        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Fishing Nets")

        for item in fishing_gear["Nets"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**
                                                                    Required Level: **{item[1]['reqlevel']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        await interaction.response.edit_message(embed = embed, view=self)
    @discord.ui.button(label = "Fishing Baits & Lures", style=discord.ButtonStyle.green, custom_id="fbal", emoji="🐚")
    async def fg3(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id=="rods"][0]
        button2 = [x for x in self.children if x.custom_id=="nets"][0]
        button3 = [x for x in self.children if x.custom_id=="fbal"][0]  
        button4 = [x for x in self.children if x.custom_id=="ship"][0]
        button5 = [x for x in self.children if x.custom_id=="quit"][0]
        button6 = [x for x in self.children if x.custom_id=="mall"][0]  

        button1.disabled = False
        button2.disabled = False
        button3.disabled = True
        button4.disabled = False
        button5.disabled = False
        button6.disabled = False

        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Fishing Baits & Lures")

        for item in fishingbal["Baits"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**
                                                                    Required Level: **{item[1]['reqlevel']}**""")
        for item in fishingbal["Lures"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**
                                                                    Required Level: **{item[1]['reqlevel']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        await interaction.response.edit_message(embed = embed, view=self)

    @discord.ui.button(label = "Ships", style=discord.ButtonStyle.green, custom_id="ship", emoji="⚓")
    async def fg4(self,interaction:discord.Interaction, button:discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id=="rods"][0]
        button2 = [x for x in self.children if x.custom_id=="nets"][0]
        button3 = [x for x in self.children if x.custom_id=="fbal"][0]  
        button4 = [x for x in self.children if x.custom_id=="ship"][0]
        button5 = [x for x in self.children if x.custom_id=="quit"][0]
        button6 = [x for x in self.children if x.custom_id=="mall"][0]  

        button1.disabled = False
        button2.disabled = False
        button3.disabled = False
        button4.disabled = True
        button5.disabled = False
        button6.disabled = True

        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Ships")

        for item in fishing_gear["Ships"].items():

            if item[1]["available"]:
                embed.add_field(name=item[0].title(), value=f"""Price: **{item[1]['price']}**
                                                                    Description: **{item[1]['description']}**
                                                                    Required Level: **{item[1]['reqlevel']}**""")

                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
                
        await interaction.response.edit_message(embed = embed, view=self)

    @discord.ui.button(label = "Quit", style=discord.ButtonStyle.red, custom_id="quit", emoji="✖")
    async def fg5(self,interaction:discord.Interaction, button:discord.ui.Button):
        self.clear_items()
        self.stop()
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Come back soon!")
        embed.add_field(name = "You have quit from the shop!", value="Don't forget to pack your items!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                        icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
        await interaction.response.edit_message(embed = embed, view=None)

    @discord.ui.button(label = "Mall", style=discord.ButtonStyle.grey, custom_id="mall", emoji="🛒")
    async def fg6(self,interaction:discord.Interaction, button:discord.ui.Button):
        view = SelectView()
        embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Return to Mall!")
        embed.add_field(name = "You have return to the mall entrance!", value="Time to shop for new items!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                        icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380")
        await interaction.response.edit_message(embed = embed, view=view)
    
   

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Kiki Mart",emoji="💳",description="Browse the general goods!"),
            discord.SelectOption(label="Saul's Catch", emoji="🐠",description="Browse the fish market!"),
            discord.SelectOption(label="Angler's Paradise", emoji="🎣",description="Browse the fishing goods!"),
            ]
        super().__init__(placeholder="Kiki Mall 24/7", max_values=1,min_values=1,options=options)
        
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Kiki Mart":
            
            view = GeneralShop()
            
            embed =discord.Embed(color=discord.Color.random())
            embed.set_author(name="Kiki Shopping")
            embed = discord.Embed(title= "Kiki Mall 24/7", description= "Choose the shop you want to visit!:")
            embed.add_field(name="Available commands", value=f"""!shop buy <item> <amount>
                                                            !shop sell <item> <amount>""")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/shop-cart-shop-building-cartoon_138676-2085.jpg?w=1380&t=st=1661480631~exp=1661481231~hmac=dfd06761dc2bdd09851b7f07e7b542d54947ccf9730c384882a78608fafdd783")
            await interaction.response.edit_message(embed=embed, view=view)

            
        
        elif self.values[0] == "Saul's Catch":
            
            view = ShopView()
            
            embed =discord.Embed(color=discord.Color.random())
            embed.set_author(name="Kiki Shopping")
            embed = discord.Embed(title= "Kiki Mall 24/7", description= "Choose the shop you want to visit!:")
            embed.add_field(name="Available commands", value=f"""!shop buy <item> <amount>
                                                            !shop sell <item> <amount>""")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/shop-cart-shop-building-cartoon_138676-2085.jpg?w=1380&t=st=1661480631~exp=1661481231~hmac=dfd06761dc2bdd09851b7f07e7b542d54947ccf9730c384882a78608fafdd783")
            await interaction.response.edit_message(embed=embed, view=view)

        elif self.values[0] == "Angler's Paradise":

            view = FishingGearView()
            
            embed =discord.Embed(color=discord.Color.random())
            embed.set_author(name="Kiki Shopping")
            embed = discord.Embed(title= "Kiki Mall 24/7", description= "Choose the shop you want to visit!:")
            embed.add_field(name="Available commands", value=f"""!shop buy <item> <amount>
                                                            !shop sell <item> <amount>""")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/shop-cart-shop-building-cartoon_138676-2085.jpg?w=1380&t=st=1661480631~exp=1661481231~hmac=dfd06761dc2bdd09851b7f07e7b542d54947ccf9730c384882a78608fafdd783")
            await interaction.response.edit_message(embed=embed, view=view)


    
    
    



class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(Select())
        

    

   

    


    

        
            
class shop(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.Cog.listener()
        
    async def on_ready(self):
        print("Shop.cog loaded.")
    
    
  
    

    ##Shop
    @commands.group(invoke_without_command=True)
    
    async def shop(self,ctx: commands.Context, member: discord.Member = None):
        
        
        view = SelectView()
        member = ctx.author 
        embed = discord.Embed(title= "Kiki Mall 24/7", description= "Choose the shop you want to visit!:", color=ctx.author.color)
        embed.set_thumbnail(url="https://images.emojiterra.com/google/noto-emoji/v2.034/512px/1f3ea.png")
        
        await ctx.send(embed=embed, view=view)
        await view.wait()

   
    @shop.command()
    async def buy(self,ctx: commands.Context, _item:str, _item2 = None, _item3 = None, amount = None):
        r = await economy.get_user(ctx.message.author.id)
        _cache = []

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        


        if _item2 is not None and _item3 is None and amount is None:
            
            _item2 = int(_item2)
            amount = _item2
            _item = _item.lower()

            for item in items_list["Items"].items():
                if item[0] == _item:
                    _cache.append(item)

                    iprice = item[1]["price"]*amount
                    
                    if r.wallet >= iprice:
                        for i in range(amount):
                            await economy.add_item(ctx.message.author.id, item[0])
                            await economy.remove_money(ctx.message.author.id, "wallet", item[1]["price"])
                            iprice = int(iprice)
                        if amount == 1:
                            embed.add_field(name="Success", value=f"Successfully bought **{amount} {item[0].title()}!**")
                            embed.add_field(name="You paid", value =f"{iprice} coins to the shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        else: 
                            embed.add_field(name="Success", value=f"Successfully bought **{amount} {item[0].title()}s!**")
                            embed.add_field(name="You paid", value =f"{iprice} coins to the shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        await ctx.send(embed=embed)

                    else:

                        embed.add_field(name="Error", value=f"You don't have enought coins to buy this item!")
                        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        await ctx.send(embed=embed)
                    break

        elif _item2 is not None and _item3 is not None and amount is None:
            _item1 = _item
            amount = int(_item3)
            _item2 = str(_item2)
            _item = _item.lower()
            _item2= _item2.lower()
            _item  = _item +" "+_item2
            

            for item in items_list["Items"].items():
                if item[0] == _item:
                    _cache.append(item)

                    iprice = item[1]["price"]*amount
                    
                    if r.wallet >= iprice:
                        for i in range(amount):
                            await economy.add_item(ctx.message.author.id, item[0])
                            await economy.remove_money(ctx.message.author.id, "wallet", item[1]["price"])
                            iprice = int(iprice)
                        if amount == 1:
                            embed.add_field(name="Success", value=f"Successfully bought **{amount} {_item1.title()} {_item2.title()}!**")
                            embed.add_field(name="You paid", value =f"{iprice} coins to the shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        else: 
                            embed.add_field(name="Success", value=f"Successfully bought **{amount} {_item.title()} {_item2.title()}s!**")
                            embed.add_field(name="You paid", value =f"{iprice} coins to the shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        await ctx.send(embed=embed)

                    else:

                        embed.add_field(name="Error", value=f"You don't have enought coins to buy this item!")
                        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        await ctx.send(embed=embed)
                    break
        
        elif _item2 is not None and _item3 is not None and amount is not None:
            _item1 = _item
            amount = int(amount)
            _item3 = str(_item3)
            _item2 = str(_item2)
            _item = _item.lower()
            _item2= _item2.lower()
            _item3= _item3.lower()
            _item = _item +" "+ _item2+" "+_item3

            for item in items_list["Items"].items():
                if item[0] == _item:
                    _cache.append(item)

                    iprice = item[1]["price"]*amount
                    
                    if r.wallet >= iprice:
                        for i in range(amount):
                            await economy.add_item(ctx.message.author.id, item[0])
                            await economy.remove_money(ctx.message.author.id, "wallet", item[1]["price"])
                            iprice = int(iprice)
                        if amount == 1:
                            embed.add_field(name="Success", value=f"Successfully bought **{amount} {_item1.title()} {_item2.title()} {_item3.title()}!**")
                            embed.add_field(name="You paid", value =f"{iprice} coins to the shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        else: 
                            embed.add_field(name="Success", value=f"Successfully bought **{amount} {_item.title()} {_item2.title()} {_item3.title()}s!**")
                            embed.add_field(name="You paid", value =f"{iprice} coins to the shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        await ctx.send(embed=embed)

                    else:

                        embed.add_field(name="Error", value=f"You don't have enought coins to buy this item!")
                        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        await ctx.send(embed=embed)
                    break
        
        


        if len(_cache) <= 0:
            embed.add_field(name="Error", value="Item with that name does not exists! \n\n Try browsing !shop instead!")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-dinosaur-box-cartoon-illustration-animal-icon-concept_138676-1922.jpg?w=1380&t=st=1661918365~exp=1661918965~hmac=555a74f79835d8248122b242dd1877d8321fd62e6d68dd16e2e1b5f9aa3912fc")
            await ctx.send(embed=embed)


    @shop.command()
    async def sell(self,ctx: commands.Context, _item: str, _item2 = None, _item3 = None, amount = None):
        r = await economy.get_user(ctx.message.author.id)
        _cache = []
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89))
        
        if _item2 is not None and _item3 is None and amount is None:
            _item2 = int(_item2)
            amount = _item2

            if _item in r.items:
                for item in items_list["Items"].items():
                    if item[0] == _item:
                        _cache.append(item)
                        item_prc = item[1]["price"] / 2
                        for i in range(amount):
                            await economy.add_money(ctx.message.author.id, "wallet", item_prc)
                            await economy.remove_item(ctx.message.author.id, item[0])
                            item_prc=int(item_prc)
                        if amount == 1:
                            embed.add_field(name="Success", value=f"Successfully sold **{amount} {item[0].title()}**!")
                            embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)

                        else:
                            embed.add_field(name="Success", value=f"Successfully sold **{amount} {item[0].title()}s**!")
                            embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        
                        await ctx.send(embed=embed)
                        break
       
        elif _item2 is not None and _item3 is not None and amount is None:
            _item1 = _item
            amount = int(_item3)
            _item2 = str(_item2)
            _item = _item.lower()
            _item2= _item2.lower()
            _item  = _item +" "+_item2

            if _item in r.items:
                for item in items_list["Items"].items():
                    if item[0] == _item:
                        _cache.append(item)
                        item_prc = item[1]["price"] / 2
                        for i in range(amount):
                            await economy.add_money(ctx.message.author.id, "wallet", item_prc)
                            await economy.remove_item(ctx.message.author.id, item[0])
                            item_prc=int(item_prc)
                        if amount == 1:
                            embed.add_field(name="Success", value=f"Successfully sold **{amount} {_item1.title()} {_item2.title()}**!")
                            embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)

                        else:
                            embed.add_field(name="Success", value=f"Successfully sold **{amount} {_item1.title()} {_item2.title()}s**!")
                            embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        
                        await ctx.send(embed=embed)
                        break 

        elif _item2 is not None and _item3 is not None and amount is not None:
            _item1 = _item
            amount = int(amount)
            _item3 = str(_item3)
            _item2 = str(_item2)
            _item = _item.lower()
            _item2= _item2.lower()
            _item3= _item3.lower()
            _item = _item +" "+ _item2+" "+_item3

            
            if _item in r.items:
                for item in items_list["Items"].items():
                    if item[0] == _item:
                        _cache.append(item)
                        item_prc = item[1]["price"] / 2
                        for i in range(amount):
                            await economy.add_money(ctx.message.author.id, "wallet", item_prc)
                            await economy.remove_item(ctx.message.author.id, item[0])
                            item_prc=int(item_prc)
                        if amount == 1:
                            embed.add_field(name="Success", value=f"Successfully sold **{amount} {_item1.title()} {_item2.title()} {_item3.title()}**!")
                            embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)

                        else:
                            embed.add_field(name="Success", value=f"Successfully sold **{amount} {_item1.title()} {_item2.title()} {_item3.title()}s**!")
                            embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                        icon_url=ctx.message.author.avatar.url)
                        
                        await ctx.send(embed=embed)
                        break 
        
        
        
            
        
        if len(_cache) <= 0:
            embed.add_field(name="Error", value="Item with that name does not exists! \n\n Try browsing !shop instead!")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-dinosaur-box-cartoon-illustration-animal-icon-concept_138676-1922.jpg?w=1380&t=st=1661918365~exp=1661918965~hmac=555a74f79835d8248122b242dd1877d8321fd62e6d68dd16e2e1b5f9aa3912fc")
            await ctx.send(embed=embed)

        

       
    @shop.command()
    async def empty(self,ctx:commands.Context, _items:str = None):
        r = await economy.get_user(ctx.message.author.id)

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        
        total_amount = 0
        
        
        if _items is not None:
            _items = _items.lower()

        if _items == "fish":
            sellables = [i for i in r.items if i in fishes_list]
            if len(sellables) == 0:
                embed.add_field(name = "You don't have any fishes to sell!", value= "Try our minigames to get more fishes!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(url= "https://img.freepik.com/premium-vector/cute-sad-cat-sitting-rain-cloud-cartoon-vector-icon-illustration-animal-nature-icon-isolated_138676-5215.jpg?w=1380")
                await ctx.send(embed = embed)
            else:
                for i in range(len(sellables)):
                    for item in shopf_list["Items"].items():
                        if item[0] == sellables[i]:
                            item_prc = item[1]["price"]/2
                            total_amount = total_amount + item_prc
                            await economy.remove_item(ctx.message.author.id, item[0])
                total_amount= int(total_amount)
                await economy.add_money(ctx.message.author.id, "wallet", total_amount)
                embed.add_field(name="Success", value=f"Successfully sold your items!")
                embed.add_field(name="You gained", value =f"**{total_amount}** coins back from shop." )
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-cat-with-fish-bag-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-flat_138676-5812.jpg?w=1380&t=st=1661817568~exp=1661818168~hmac=79960fa9cac50d68ab541c78d4081475916e67440a6e33b7f728b83e26fa4910")            
                await ctx.send(embed=embed)
        elif _items is None:
            embed.add_field(name = "You can only empty your fishing buckets!", value= "Try 'fish' command after empty!")
            embed.set_thumbnail(url= "https://img.freepik.com/premium-vector/cute-sad-cat-sitting-rain-cloud-cartoon-vector-icon-illustration-animal-nature-icon-isolated_138676-5215.jpg?w=1380")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed = embed)
        else:
            embed.add_field(name = "You can only empty your fishing buckets!", value= "Try 'fish' command after empty!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
            embed.set_thumbnail(url= "https://img.freepik.com/premium-vector/cute-sad-cat-sitting-rain-cloud-cartoon-vector-icon-illustration-animal-nature-icon-isolated_138676-5215.jpg?w=1380")                                
            await ctx.send(embed = embed)

    @shop.command()
    async def bargain(self,ctx:commands.Context, _items:str = None):
        r = await economy.get_user(ctx.message.author.id)

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        
        total_amount = 0
        
        
        if _items is not None:
            _items = _items.lower()

        if _items == "gacha":
            sellables = [i for i in r.items if i in gac_items]
            if len(sellables) == 0:
                embed.add_field(name = "You don't have any gacha collectibls to sell!", value= "Try our !gacha minigame!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(url= "https://img.freepik.com/premium-vector/cute-sad-cat-sitting-rain-cloud-cartoon-vector-icon-illustration-animal-nature-icon-isolated_138676-5215.jpg?w=1380")
                await ctx.send(embed = embed)
            else:
                for i in range(len(sellables)):
                    for item in gshop_list["Items"].items():
                        if item[0] == sellables[i]:
                            item_prc = item[1]["price"]
                            total_amount = total_amount + item_prc
                            await economy.remove_item(ctx.message.author.id, item[0])
                total_amount= int(total_amount)
                await economy.add_money(ctx.message.author.id, "wallet", total_amount)
                embed.add_field(name="Successful Bargain", value=f"Successfully sold your items!")
                embed.add_field(name="You gained", value =f"**{total_amount}** coins back from shop." )
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-cat-with-fish-bag-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-flat_138676-5812.jpg?w=1380&t=st=1661817568~exp=1661818168~hmac=79960fa9cac50d68ab541c78d4081475916e67440a6e33b7f728b83e26fa4910")            
                await ctx.send(embed=embed)
        elif _items is None:
            embed.add_field(name = "You can only bargain for your gacha collectibles!", value= "Try 'gacha' command after bargain!")
            embed.set_thumbnail(url= "https://img.freepik.com/premium-vector/cute-sad-cat-sitting-rain-cloud-cartoon-vector-icon-illustration-animal-nature-icon-isolated_138676-5215.jpg?w=1380")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed = embed)
        else:
            embed.add_field(name = "You can only bargain for your gacha collectibles!", value= "Try 'gacha' command after bargain!")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                            icon_url=ctx.message.author.avatar.url)
            embed.set_thumbnail(url= "https://img.freepik.com/premium-vector/cute-sad-cat-sitting-rain-cloud-cartoon-vector-icon-illustration-animal-nature-icon-isolated_138676-5215.jpg?w=1380")                                
            await ctx.send(embed = embed)

    @commands.command(aliases = ['buy', 'b'])
    async def qbuy(self,ctx: commands.Context, _item:str, _item2 = None, _item3 = None, amount = None):
        r = await economy.get_user(ctx.message.author.id)
        data = await economy.get_user_lvl(ctx.message.author.id)
        flvl = data.fish
        _cache = []

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        if _item2 is None and _item3 is None and amount is None:
            _item = _item.lower()
            amount = 1

        elif _item2 is not None and _item3 is None and amount is None:
            if len(_item2) == 1:
                _item = _item.lower()
                amount = int(_item2)
                    
            elif len(_item2) > 1:
                _item = _item.lower()
                _item2= str(_item2).lower()
                _item = _item + " "+_item2
                amount = 1
        elif _item2 is not None and _item3 is not None and amount is None:
            if len(_item3) == 1:
                _item = _item.lower()
                _item2 = str(_item2).lower()
                amount = int(_item3)
                _item = _item+" "+_item2
            elif len(_item3) > 1:
                _item = _item.lower()
                _item2 = str(_item2).lower()
                _item3 = str(_item3).lower()
                amount = 1
                _item = _item+" "+_item2+" "+_item3
        elif _item2 is not None and _item3 is not None and amount is not None:
            _item = _item.lower()
            _item2 = str(_item2).lower()
            _item3 = str(_item3).lower()
            _item = _item+" "+_item2+" "+_item3
            amount = int(amount)
        
        

        for item in items_list["Items"].items():
            if item[0] == _item:
                _cache.append(item)

                iprice = item[1]["price"]*amount
                rlvl = item[1]["reqlevel"]

                if r.wallet >= iprice and flvl >=rlvl:
                    for i in range(amount):
                        await economy.add_item(ctx.message.author.id, item[0])
                        await economy.remove_money(ctx.message.author.id, "wallet", item[1]["price"])
                        iprice = int(iprice)
                    
                    embed.add_field(name="Success", value=f"Successfully bought **{amount} {item[0].title()}!**")
                    embed.add_field(name="You paid", value =f"{iprice} coins to the shop" )
                    embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                icon_url=ctx.message.author.avatar.url)
                    
                    await ctx.send(embed=embed)
                
                elif r.wallet >= iprice and flvl < rlvl:

                    embed.add_field(name="Error", value=f"You don't have enough levels to buy this item!")
                    embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                    icon_url=ctx.message.author.avatar.url)
                    await ctx.send(embed=embed)
                    break
                
                elif r.wallet < iprice:

                    embed.add_field(name="Error", value=f"You don't have enough coins to buy this item!")
                    embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                    icon_url=ctx.message.author.avatar.url)
                    await ctx.send(embed=embed)
                    break
                break
        if len(_cache) <= 0:
            embed.add_field(name="Error", value="Item with that name does not exists! \n\n Try browsing !shop instead!")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-dinosaur-box-cartoon-illustration-animal-icon-concept_138676-1922.jpg?w=1380&t=st=1661918365~exp=1661918965~hmac=555a74f79835d8248122b242dd1877d8321fd62e6d68dd16e2e1b5f9aa3912fc")
            await ctx.send(embed=embed)


    @commands.command(aliases = ['sell', 's'])
    async def qsell(self,ctx: commands.Context, _item: str, _item2 = None, _item3 = None, amount = None):
        r = await economy.get_user(ctx.message.author.id)
        _cache = []
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89))
        
        if _item2 is None and _item3 is None and amount is None:
            _item = _item.lower()
            amount = 1

        elif _item2 is not None and _item3 is None and amount is None:
            if len(_item2) == 1:
                _item = _item.lower()
                amount = int(_item2)
                    
            elif len(_item2) > 1:
                _item = _item.lower()
                _item2= str(_item2).lower()
                _item = _item + " "+_item2
                amount = 1
        elif _item2 is not None and _item3 is not None and amount is None:
            if len(_item3) == 1:
                _item = _item.lower()
                _item2 = str(_item2).lower()
                amount = int(_item3)
                _item = _item+" "+_item2
            elif len(_item3) > 1:
                _item = _item.lower()
                _item2 = _item2.lower()
                _item3 = _item3.lower()
                amount = 1
                _item = _item+" "+_item2+" "+_item3
        elif _item2 is not None and _item3 is not None and amount is not None:
            _item = _item.lower()
            _item2 = str(_item2).lower()
            _item3 = str(_item3).lower()
            _item = _item+" "+_item2+" "+_item3
            amount = int(amount)

        if _item in r.items:
            for item in items_list["Items"].items():
                if item[0] == _item:
                    _cache.append(item)
                    item_prc = item[1]["price"] / 2
                    for i in range(amount):
                        await economy.add_money(ctx.message.author.id, "wallet", item_prc)
                        await economy.remove_item(ctx.message.author.id, item[0])
                        item_prc=int(item_prc)
                    if amount == 1:
                        embed.add_field(name="Success", value=f"Successfully sold **{amount} {item[0].title()}**!")
                        embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                    icon_url=ctx.message.author.avatar.url)

                    else:
                        embed.add_field(name="Success", value=f"Successfully sold **{amount} {item[0].title()}s**!")
                        embed.add_field(name="You gained", value =f"**{item_prc}** coins back from shop" )
                        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                    icon_url=ctx.message.author.avatar.url)
                    
                    await ctx.send(embed=embed)
                    break
       
        
        
        
        
        if len(_cache) <= 0:
            embed.add_field(name="Error", value="Item with that name does not exists! \n\n Try browsing !shop instead!")
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-dinosaur-box-cartoon-illustration-animal-icon-concept_138676-1922.jpg?w=1380&t=st=1661918365~exp=1661918965~hmac=555a74f79835d8248122b242dd1877d8321fd62e6d68dd16e2e1b5f9aa3912fc")
            await ctx.send(embed=embed)
                

    




    

async def setup(bot):
    await bot.add_cog(shop(bot))
