from code import interact
from email import message
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
import tracemalloc
from main import economy

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Economy System",emoji="💰",description="Help about Economy System and subcommands!"),
            discord.SelectOption(label="Fishing System", emoji="🐠",description="Help about Fishing System!"),
            discord.SelectOption(label="Gacha", emoji="🎁",description="Help about how to gacha!"),
            discord.SelectOption(label="Games & Gamba", emoji="🎲",description="Help about games & gamba subcommands!"),
            discord.SelectOption(label="Level System", emoji="💎",description="Help about Level System and subcommands!"),
            discord.SelectOption(label="Crime System", emoji="🗡",description="Help about Crime System and subcommands!"),
            discord.SelectOption(label="Shop", emoji="🛒",description="Help about shopping in Kiki MetaVerse and subcommands!"),
            discord.SelectOption(label="Quit", emoji="❌",description="Quit the helping system!"),
            ]
        super().__init__(placeholder="Kiki MetaVerse Helper", max_values=1,min_values=1,options=options)
        

    async def callback(self, interaction: discord.Interaction):
        embed =discord.Embed(color=discord.Color.random())
        embed.set_author(name="Kiki MetaVerse Helper 24/7")
        view= HelpSelectView(self)

        
        
        
        if self.values[0]=="Economy System":
            embed.add_field(name = "!welcome", value= "A one time only for Kikis. Adds a token for gacha and 100 coins for games.", inline=False)
            embed.add_field(name = "!daily", value= "Gives a random amount of coins daily!", inline=False)
            embed.add_field(name = "!inventory", value= "Shows your current items in your bag.", inline=False)
            embed.add_field(name = "!balance", value= "Shows your current coins in your wallet and bank.", inline=False)
            embed.add_field(name = "!withdraw", value= "Allows you to withdraw coins from bank to your wallet. \n !withdraw <amount>", inline=False)
            embed.add_field(name = "!deposit", value= "Allows you to deposit coins from your wallet to your bank. \n !deposit <amount>", inline=False)
            embed.add_field(name = "!leaderboard", value= "Shows the current leaderboard of richest players!", inline=False)
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_thumbnail(url="https://img.freepik.com/free-vector/cute-cat-with-money-gold-coin-bottle-cartoon-vector-icon-illustration-animal-business-flat_138676-5866.jpg?w=1380&t=st=1662063978~exp=1662064578~hmac=08a61b8d4152177a6a667bd18553ab78aebcc5548187aa9e7d43c88b23759c7f")
            embed.set_author(name = "Economy System Help")      
            self.disabled=True
            await interaction.response.edit_message(embed=embed, view=view)
            
        elif self.values[0]=="Fishing System":
            embed.add_field(name="Basics", value="Fishing system involves an interactive menu with buttons of **Fish**, **Net** and **Sail**")
            embed.add_field(name = "Fish Button", value="Basic fishing game. You cast your rod and grab a fish!. You also earn experience. Requires **Baits and/or Lures** as item.")
            embed.add_field(name="Net Button", value = "It's fishing with a net for multiple fish gains. Unlocked after your fishing level is ***5*** or more. You also earn experience. Requires **Nets** as item.")
            embed.add_field(name = "Sail Button", value = "An ultimate fishing sailing journey across the deadly Kiki seas. Unlocked after fishing skill ***10*** or more. You also earn experience. A mini game to collect **Sea Artifacts**")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_author(name = "Fishing System Help")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-reading-book-with-coffee-cartoon-vector-icon-illustration-animal-education-icon-isolated_138676-5548.jpg?w=1380")
            
            self.disabled=True
            await interaction.response.edit_message(embed=embed, view=view)
            
        elif self.values[0] == "Gacha":
            embed.add_field(name = "Basics", value = "Gacha system allows you to obtain Kiki Collectibles.\n\n It's used by !gacha command. \n\n Collectible items has different rarities. \n\n Playing gacha requires ***Token*** obtainable from shop.\n\n Use !shop buy token <amount> to get your token. ")
            embed.add_field(name = "Rarities", value="Common \n Uncommon \n Rare \n Epic \n Legendary \n Mega Legendary")
            embed.add_field(name ="Sellback", value = "By using !shop bargain command you can sell all your collectibles up to epic rarity in exchange for coins.")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_author(name = "Gacha System Help")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-box-vector-icon-illustration_138676-411.jpg?w=1380")
            self.disabled=True
            await interaction.response.edit_message(embed=embed, view=view)
            
        elif self.values[0] == "Games & Gamba":
            embed.add_field(name = "Basics", value = "Kiki MetaVerse allows you to play different games to earn coins and experience!")
            embed.add_field(name = "!dice <amount>", value="Allows you to play a dice game against the bot. Maximum amount to bet is ***10 coins***")
            embed.add_field(name = "!rps <amount>", value="Allows you to play a basic Rock & Paper & Shotgun game against the bot. Maximum amount to bet is ***10 coins***")
            embed.add_field(name = "!horse <amount>", value = "Allows you to play a horse racing gamba. Unlocked after your gamba level is ***5*** or more. Maximum amount to bet is ***10 coins***")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_author(name = "Games & Gamba Help")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-tiger-jump-ring-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-flat_138676-5353.jpg?w=1380")
            self.disabled=True
            await interaction.response.edit_message(embed=embed, view=view)
            
        elif self.values[0] == "Shop":
            embed.add_field(name= "!shop", value = "Allows you to browse the Kiki MetaVerse Mall 24/7")
            embed.add_field(name = "!shop buy <item name> <amount>", value="Allows you to buy requested amount of item from the shop in exchange for coins. ")
            embed.add_field(name = "!shop sell <item name> <amount>", value="Allows you to sell requested amount of item to the shop in exchange for coins. \n For items listed in shop browse, you will get half amount their buying price when you sell the item back. ")
            embed.add_field(name = "!shop empty fish", value="Allows you to sell all your fishes in your inventory in exchange for coins.")
            embed.add_field(name = "!shop Bargain", value = "Allows you to sell all your gacha collectibles up to epic rarity in exchange for coins.")
            embed.add_field(name = "!buy <item name>", value = "Also allows you to quick buy the item. You can enter amount after the item name upto 9 max.")
            embed.add_field(name = "!sell <item name>", value = "Also allows you to quick sell the item. You can enter amount after the item name upto 9 max.")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_author(name = "Kiki Mall Help")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/business-cat-character-illustration_138676-300.jpg?w=1800")
            self.disabled=True
            await interaction.response.edit_message(embed=embed, view=view)
        elif self.values[0] == "Level System":
            embed.add_field(name="Basics", value = "Minigames in the Kiki MetaVerse allows you to gain experience points in your journey.")
            embed.add_field(name ="!level", value = "Allows you to reach Levelling System Menu with buttons Level Status and Level Up.")
            embed.add_field(name = "Level Status Button", value="Shows your current progress in Kiki MetaVerse.")
            embed.add_field(name = "Level Up Button", value="Allows you to level up and gain skill points that you can spend on various skills. \n\n Current skills are ***Fishing*** and ***Gambling***. \n\n After you level up excess xp will be added to your current progress to next level. \n\n You can only level up and gain skill points manually by using this system!" )
            embed.add_field(name = "!skill", value="Opens up the menu for increasing your skills. \n\n You can use your skill up points that you gained from levelling up on either ***Fishing*** or ***Gambling*** by clicking their buttons.")
            embed.add_field(name ="!skill reset", value= "Allows you to reset your current skills meanwhile keeping your levelling progress.\n\n Requires a **Skill Reset** item from shop.\n\n !shop buy skill reset <amount> will give allow you to buy skill reset item.")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_author(name = "Levelling System Help")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-gaming-with-game-console-cartoon_138676-2315.jpg?w=1380")
            self.disabled=True
            await interaction.response.edit_message(embed=embed, view=view)
        elif self.values[0] == "Crime System":
            embed.add_field(name = "Basics", value = "Kiki MetaVerse allows you to do fun crime activities with a rpg-ish system!")
            embed.add_field(name = "!crime", value="Opens up a menu to spend your actions. Gather for gathering resources. Recruit for gaining henchmen. Work for earning coins.")
            embed.add_field(name = "Gather", value="You can get Plant, Metal, Wood, Stone, Water or Electric to produce materials for crafting related to your gatherers.")
            embed.add_field(name = "Recruit", value = "You can get Worker, Gatherer, Thug, Agent to boost your criminal activities.")
            embed.add_field(name = "Work", value = "You gain coins related to your worker capacity.")
            embed.add_field(name = "!record", value = "Shows your current status on crime rpg system. Your resources, inventory, henchmen, etc...")
            embed.add_field(name = "!intel @target_user", value = "Depending on your agents you can gather information about your target. Open's up the target's !record window. Requires **Knuckle** item.")
            embed.add_field(name = "!attack @target_user", value = "Depending on your thugs you can attack your targets henchmen. Requires **Gun** item.")
            embed.add_field(name = "!arson @target_user", value = "Attacks to your target's resources. Requires ** Molotov Cocktail** item.")
            embed.add_field(name = "!rob @target_user", value= "Tries to steal coins from your target's wallet directly. Requires **Knife** item.")
            embed.add_field(name = "!craft", value = "Opens up the crafting menu. More detailed info in that screen.")
            embed.add_field(name = "!craft goods", value = "Opens up the menu to turn your materials into actual items.")
            embed.add_field(name = "!deal", value = "Sells out all your weeds in your inventory in exchange for coins.")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_author(name = "Games & Gamba Help")
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-tiger-jump-ring-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-flat_138676-5353.jpg?w=1380")
            self.disabled=True
            await interaction.response.edit_message(embed=embed, view=view)
        elif self.values[0] =="Quit":
            embed.set_author(name="Come back soon!")
            embed.add_field(name = "You have quit from the helping system!", value="Don't forget the commands you learnt!")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
            embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-reading-book-with-coffee-cartoon-vector-icon-illustration-animal-education-icon-isolated_138676-5548.jpg?w=1380")
            await interaction.response.edit_message(embed = embed, view=None)

    

class HelpSelectView(discord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.add_item(HelpSelect())

  
       
       
    
    

    


class helper (commands.Cog):
    def __init__(self,bot):
        self.bot= bot
        
    @commands.Cog.listener()
        
    async def on_ready(self):
        print("Help.cog loaded.")

    async def cog_check(self,ctx:commands.Context):
        a =await economy.is_registered(ctx.message.author.id)
        a = await economy.is_lvlregistered(ctx.message.author.id)
        return a 

    
    

    ##Help
    @commands.group(invoke_without_command=True, aliases = ['h', 'helper'])
    async def help(self,ctx: commands.Context, member: discord.Member = None):
        
        
        view = HelpSelectView(ctx)
        member = ctx.author 
        embed = discord.Embed(title= "Kiki MetaVerse Helper 24/7", description= "Choose the topic you want to get help!:", color=ctx.author.color)
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-working-laptop-cartoon-icon-illustration_138676-2647.jpg?w=1380")
        
        await ctx.send(embed=embed, view=view)
        await view.wait()


async def setup(bot):
    await bot.add_cog(helper(bot))