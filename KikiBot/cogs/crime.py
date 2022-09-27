from code import interact
from itertools import count
from operator import countOf
from tracemalloc import stop
from turtle import clear
from urllib import response
import discord
import os
import asyncio
from discord.ext import commands, tasks
from discord.ui import Button, View
import sqlite3
import random
from time import sleep
from DiscordEconomy.Sqlite import Economy
from lists.itemslist import *
import tracemalloc
from main import economy
from lists.itemslist import *
from lists.crimelist import *
from easy_pil import *


class CrimeView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.cooldown = commands.CooldownMapping.from_cooldown(
            3, 300, commands.BucketType.member)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Gather",
                       style=discord.ButtonStyle.blurple,
                       custom_id="gather")
    async def c1(self, interaction: discord.Interaction,
                 button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "gather"][0]
        button2 = [x for x in self.children if x.custom_id == "recruit"][0]
        button3 = [x for x in self.children if x.custom_id == "work"][0]
        button4 = [x for x in self.children if x.custom_id == "quit"][0]
        interaction.message.author = interaction.user
        user = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)

        retry = bucket.update_rate_limit()
        if retry:
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            button4.disabled = False
            embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-fat-cat-sitting-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-flat_138676-4619.jpg?w=826&t=st=1663535655~exp=1663536255~hmac=7b58c80881faeedca9e94d7b9e04863e7885d2fe4be7f2beff227d3e797a32fb"
            )
            embed.set_footer(text=f"Invoked by {user.name}",
                             icon_url=user.avatar.url)
            embed.add_field(name="You have used all of your actions.",
                            value=f"Try again in {round(retry,1)} seconds.")
            return await interaction.response.edit_message(embed=embed,
                                                           view=self)
        else:

            rlist = ["plant", "metal", "wood", "stone", "water", "electric"]
            embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
            data = await economy.get_c_user(user.id)
            gatherers = data.gatherer
            if gatherers >= 0 and gatherers <= 10:
                gatherers = 10
                amount = random.randint(1, gatherers)
            elif gatherers >10 and gatherers <=100:
                amount = random.randint(1, int(gatherers/4)) + int(gatherers/4)
            elif gatherers >100 and gatherers <=500:
                amount = random.randint(1, int(gatherers/8)) + int(gatherers/8)
            elif gatherers >500:
                amount = random.randint(1,int(gatherers/10)) + int(gatherers/10)

            chance = random.randint(0, 5)
            rs = rlist[chance]

            await economy.add_crime_stat(user.id, f"{rs}", amount)
            embed.add_field(
                name=f"You have gained {rs.capitalize()}",
                value=
                f"{amount} amount of {rs.capitalize()} added to your resources."
            )
            embed.set_footer(text=f"Invoked by {user.name}",
                             icon_url=user.avatar.url)
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/cute-cat-playing-rubbish-bin-trash-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3713.jpg?w=826"
            )
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Recruit",
                       style=discord.ButtonStyle.blurple,
                       custom_id="recruit")
    async def c2(self, interaction: discord.Interaction,
                 button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "gather"][0]
        button2 = [x for x in self.children if x.custom_id == "recruit"][0]
        button3 = [x for x in self.children if x.custom_id == "work"][0]
        button4 = [x for x in self.children if x.custom_id == "quit"][0]
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)

        retry = bucket.update_rate_limit()
        if retry:
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            button4.disabled = False
            embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                             icon_url=interaction.user.avatar.url)
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-fat-cat-sitting-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-flat_138676-4619.jpg?w=826&t=st=1663535655~exp=1663536255~hmac=7b58c80881faeedca9e94d7b9e04863e7885d2fe4be7f2beff227d3e797a32fb"
            )
            embed.add_field(name="You have used all of your actions.",
                            value=f"Try again in {round(retry,1)} seconds.")
            return await interaction.response.edit_message(embed=embed,
                                                           view=self)
        else:
            user = interaction.user.id
            embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
            hlist = ["worker", "gatherer", "thug", "agent"]
            chance = random.randint(0, 3)
            amount = random.randint(1, 5)
            rh = hlist[chance]
            await economy.add_crime_stat(user, f"{rh}", amount)
            embed.add_field(
                name=f"You have gained {rh.capitalize()}",
                value=
                f"{amount} amount of {rh.capitalize()} added to your henchmen."
            )
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                             icon_url=interaction.user.avatar.url)
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/couple-cat-cartoon-character-animal-love-isolated_138676-3154.jpg?w=826"
            )
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Work",
                       style=discord.ButtonStyle.blurple,
                       custom_id="work")
    async def c3(self, interaction: discord.Interaction,
                 button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "gather"][0]
        button2 = [x for x in self.children if x.custom_id == "recruit"][0]
        button3 = [x for x in self.children if x.custom_id == "work"][0]
        button4 = [x for x in self.children if x.custom_id == "quit"][0]
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            button4.disabled = False
            embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                             icon_url=interaction.user.avatar.url)
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-fat-cat-sitting-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-flat_138676-4619.jpg?w=826&t=st=1663535655~exp=1663536255~hmac=7b58c80881faeedca9e94d7b9e04863e7885d2fe4be7f2beff227d3e797a32fb"
            )
            embed.add_field(name="You have used all of your actions.",
                            value=f"Try again in {round(retry,1)} seconds.")
            return await interaction.response.edit_message(embed=embed,
                                                           view=self)
        else:
            user = interaction.user.id
            data = await economy.get_c_user(user)
            workers = data.worker
            if workers >= 0 and workers <= 10:
                workers = 10
                amount = random.randint(1, workers)
            elif workers >10 and workers <=100:
                amount = random.randint(1, int(workers/2)) + int(workers/2)
            elif workers >100 and workers <=500:
                amount = random.randint(1, int(workers/4)) + int(workers/4)
            elif workers >500:
                amount = random.randint(1,int(workers/5)) + int(workers/5)
            embed = discord.Embed(color=discord.Color.random())
            await economy.add_money(user, "wallet", amount)

            embed.add_field(
                name="Your workers succesfully made you some profit",
                value=
                f"{amount} Kiki Coins from crime work added to your balance.")
            embed.set_footer(text=f"Invoked by {interaction.user.name}",
                             icon_url=interaction.user.avatar.url)
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/angry-cat-working-laptop-illustration_138676-305.jpg?w=1060"
            )
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Quit",
                       style=discord.ButtonStyle.red,
                       custom_id="quit",
                       emoji="✖")
    async def c4(self, interaction: discord.Interaction,
                 button: discord.ui.Button):
        self.clear_items()
        self.stop()
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Kiki Crime Central!")
        embed.add_field(name="You have quit from the Kiki Crime Central!",
                        value="We await for your return!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                         icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-fat-cat-sitting-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated-flat_138676-4619.jpg?w=826&t=st=1663535655~exp=1663536255~hmac=7b58c80881faeedca9e94d7b9e04863e7885d2fe4be7f2beff227d3e797a32fb"
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    async def interaction_check(self,
                                interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            embed = discord.Embed(color=discord.Color.random())
            embed = discord.Embed(title="The current screen is not yours.",
                                  description="Please try again")
            embed.add_field(name="Did you try starting your own journey?",
                            value="Start with !daily and join the mini games.")
            embed.set_footer(text="***Summon screen belongs to {}***".format(
                self.ctx.author.name),
                             icon_url=(self.ctx.author.avatar))
            embed.set_thumbnail(
                url=
                "https://i.pinimg.com/originals/4f/c6/59/4fc659d1c70c6a5ded85595c8e19a3d8.png"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
            return False

        else:
            return True

class crime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        print("Crime.cog loaded.")

    async def cog_check(self, ctx: commands.Context):
        r = await economy.is_cregistered(ctx.message.author.id)
        return r

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def crime(self, ctx: commands.Context):
        view = CrimeView(ctx)
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Kiki Crime Central")
        embed.add_field(
            name="Time to do some questionable activity!",
            value=
            "Gather resources. \n Recruit henchmen. \n Work for coins. \n\n You have 3 action selections. \n Choose wisely."
        )
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/premium-vector/cute-cat-wearing-pumpkin-halloween-with-knife_138676-3316.jpg?w=826"
        )
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed, view=view)

    ##RECORD
    @commands.command()
    async def record(self, ctx: commands.Context):
        user = ctx.message.author
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        data = await economy.get_c_user(user.id)
        plant = data.plant
        metal = data.metal
        wood = data.wood
        stone = data.stone
        water = data.water
        electric = data.electric
        worker = data.worker
        gatherer = data.gatherer
        thug = data.thug
        agent = data.agent
        rob = data.rob
        arson = data.arson
        deal = data.deal
        inv = data.item

        umat = [
            f"{inv.count(i)} x {i.title()} " for i in c_materials if i in inv
        ]
        uitems = [
            f"{inv.count(i)} x {i.title()} " for i in c_items if i in inv
        ]
        umat = "\n".join(umat) if len(umat) >= 1 else "Nothing in inventory"
        uitems = "\n".join(
            uitems) if len(uitems) >= 1 else "Nothing in inventory"

        embed.add_field(
            name="Resources",
            value=
            f"Plant {plant} \n Metal: {metal} \n Wood: {wood}\n Stone: {stone} \n Water: {water} \n Electric: {electric}"
        )
        embed.add_field(
            name="Henchmen",
            value=
            f"Worker: {worker} \n Gatherer: {gatherer} \n Thug: {thug} \n Agent: {agent}"
        )
        embed.add_field(name="Criminal Record",
                        value=f"Rob: {rob} \n Arson: {arson} \n Deal: {deal}")
        embed.add_field(name="Materials", value=umat)
        embed.add_field(name="Items", value=uitems)
        embed.set_author(name=f"{user.name.title()}'s Stats")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/premium-vector/cat-businessman-with-phone-icon-illustration-animal-profession-icon-concept_138676-1836.jpg?w=826"
        )
        await ctx.send(embed=embed)

        ###EVENTS###

    ##INTEL
    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def intel(self, ctx: commands.Context, target: discord.Member):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author.id
        target = ctx.message.mentions[0]

        if ctx.author == target:
            await ctx.send("You can't rob yourself!")

            return
        else:

            udata = await economy.get_c_user(user)
            tdata = await economy.get_c_user(target.id)
            inv = udata.item
            if "knuckle" in inv:
                await economy.remove_crime_item(user, "knuckle")
                uagents = udata.agent
                tagents = tdata.agent
                plant = tdata.plant
                metal = tdata.metal
                wood = tdata.wood
                stone = tdata.stone
                water = tdata.water
                electric = tdata.electric
                worker = tdata.worker
                gatherer = tdata.gatherer
                thug = tdata.thug
                agent = tdata.agent
                rlist = [plant, metal, wood, stone, water, electric]
                rnlist = [
                    "plant", "metal", "wood", "stone", "water", "electric"
                ]
                hlist = [worker, gatherer, thug, agent]
                hnlist = ["worker", "gatherer", "thug", "agent"]

                if uagents is None or uagents == 0:
                    uagents = 0

                if tagents is None or tagents == 0:
                    tagents = 0

                uroll = random.randint(0, 100) + int(uagents / 10)
                troll = random.randint(0, 100) + int(tagents / 10)

                if uroll > troll:
                    embed.add_field(
                        name="Your intel action was successful.",
                        value="Your agents bring you the victim's info.")
                    embed.set_footer(
                        text=f"Invoked by {ctx.message.author.name}",
                        icon_url=ctx.message.author.avatar.url)
                    msg = await ctx.send(embed=embed)
                    await asyncio.sleep(3)
                    embed.clear_fields()
                    embed.add_field(
                        name="Resources",
                        value=
                        f"Plant {plant} \n Metal: {metal} \n Wood: {wood}\n Stone: {stone} \n Water: {water} \n Electric: {electric}"
                    )
                    embed.add_field(
                        name="Henchmen",
                        value=
                        f"Worker: {worker} \n Gatherer: {gatherer} \n Thug: {thug} \n Agent: {agent}"
                    )
                    embed.set_author(name=f"{target.name.title()}'s Intel")
                    embed.set_footer(
                        text=f"Invoked by {ctx.message.author.name}",
                        icon_url=ctx.message.author.avatar.url)
                    await msg.edit(embed=embed)
                elif uroll <= troll:
                    embed.add_field(
                        name="Your intel action was countered.",
                        value=
                        f"{target.name.title()}'s agents noticed your agents!")
                    embed.set_footer(
                        text=f"Invoked by {ctx.message.author.name}",
                        icon_url=ctx.message.author.avatar.url)

                    await ctx.send(embed=embed)
            else:
                embed.add_field(
                    name="You don't have any knuckles left to make them talk.",
                    value="Try crafting more.")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-with-knife-cartoon-illustration_138676-3253.jpg?w=1380&t=st=1662086193~exp=1662086793~hmac=d3c530af4f664498e03ad6a3ddad6f924a3164ba6bea7e991b9a13a6477d1d86"
                )
                embed.set_author(name="Kiki Crime")
                await ctx.send(embed=embed)

    ##ATTACK
    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def attack(self, ctx: commands.Context, target: discord.Member):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author.id
        target = ctx.message.mentions[0]

        if ctx.author == target:
            await ctx.send("You can't attack yourself!")
            return
        else:
            udata = await economy.get_c_user(user)
            tdata = await economy.get_c_user(target.id)
            inv = udata.item
            if "gun" in inv:
                await economy.remove_crime_item(user, "gun")
                uthugs = udata.thug
                tthugs = tdata.thug
                worker = tdata.worker
                gatherer = tdata.gatherer
                thug = tdata.thug
                agent = tdata.agent

                if uthugs is None or uthugs == 0:
                    uthugs = 0

                if tthugs is None or tthugs == 0:
                    tthugs = 0

                uroll = random.randint(0, 100) + int(uthugs / 10)
                troll = random.randint(0, 100) + int(tthugs / 10)

                if uroll > troll:
                    damage = random.randint(1, 10)
                    hlist = [worker, gatherer, thug, agent]
                    hnlist = ["worker", "gatherer", "thug", "agent"]
                    chance = random.randint(0, 5)
                    hs = hnlist[chance]
                    di = hlist[chance]

                    embed = discord.Embed(color=discord.Color.random())
                    if di == 0:
                        ndi = 0
                    elif di > 0:
                        ndi = di - damage

                    if ndi == 0:

                        embed.add_field(
                            name=
                            f"You have succesfully attacked {hs.capitalize()}",
                            value=
                            f"But {target.name}'s henchmen weren't enough to scare off."
                        )
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/cute-cat-ninja-holding-sword-cartoon-vector-icon-illustration-animal-holiday-icon-concept-isolated_138676-6049.jpg?w=1380&t=st=1663535891~exp=1663536491~hmac=2c8963c3ead92c4a9569d5a80e09d91c68158cdda8e68ea1ba85c5f15aead10f"
                        )
                        embed.set_footer(
                            text=f"Invoked by {ctx.message.author.name}",
                            icon_url=ctx.message.author.avatar.url)
                        await ctx.send(embed=embed)
                        return

                    elif ndi > 0:

                        await economy.set_crime_stat(target.id, f"{hs}", ndi)
                        embed.set_footer(
                            text=f"Invoked by {ctx.message.author.name}",
                            icon_url=ctx.message.author.avatar.url)
                        embed.add_field(
                            name=
                            f"You have succesfully attacked {hs.capitalize()}",
                            value=
                            f"{damage} amount of {hs.capitalize()} were scared off from {target.name.title()}'s henchmen."
                        )

                elif uroll == troll:
                    embed.add_field(
                        name=f"You couldn't attempt the attack!",
                        value=
                        f"{target.name}'s agents found your actions beforehand."
                    )

                elif uroll < troll:
                    embed.add_field(
                        name=f"Your attack attempt failed!",
                        value=f"{target.name} called Kiki FBI on your arse.")

                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-ninja-holding-sword-cartoon-vector-icon-illustration-animal-holiday-icon-concept-isolated_138676-6049.jpg?w=1380&t=st=1663535891~exp=1663536491~hmac=2c8963c3ead92c4a9569d5a80e09d91c68158cdda8e68ea1ba85c5f15aead10f"
                )
                await ctx.send(embed=embed)
            else:
                embed.add_field(name="You don't have any guns left to attack.",
                                value="Try crafting more.")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-with-knife-cartoon-illustration_138676-3253.jpg?w=1380&t=st=1662086193~exp=1662086793~hmac=d3c530af4f664498e03ad6a3ddad6f924a3164ba6bea7e991b9a13a6477d1d86"
                )
                embed.set_author(name="Kiki Crime")
                await ctx.send(embed=embed)

    ##ARSON
    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def arson(self, ctx: commands.Context, target: discord.Member):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author.id
        target = ctx.message.mentions[0]

        if ctx.author == target:
            await ctx.send("You can't arson yourself!")
            return
        else:
            udata = await economy.get_c_user(user)
            tdata = await economy.get_c_user(target.id)
            await economy.add_crime_stat(user, "arson", 1)
            inv = udata.item
            if "molotov" in inv:
                await economy.remove_crime_item(user, "molotov")
                uthugs = udata.thug
                tthugs = tdata.thug
                plant = tdata.plant
                metal = tdata.metal
                wood = tdata.wood
                stone = tdata.stone
                water = tdata.water
                electric = tdata.electric

                if uthugs is None or uthugs == 0:
                    uthugs = 0

                if tthugs is None or tthugs == 0:
                    tthugs = 0

                uroll = random.randint(0, 100) + int(uthugs / 10)
                troll = random.randint(0, 100) + int(tthugs / 10)

                if uroll > troll:
                    damage = random.randint(1, 10)
                    rlist = [plant, metal, wood, stone, water, electric]
                    rnlist = [
                        "plant", "metal", "wood", "stone", "water", "electric"
                    ]
                    chance = random.randint(0, 5)
                    rs = rnlist[chance]
                    di = rlist[chance]

                    embed = discord.Embed(color=discord.Color.random())
                    if di == 0:
                        ndi = 0
                    elif di > 0:
                        ndi = di - damage

                    if ndi == 0:

                        embed.add_field(
                            name=
                            f"You have succesfully arsoned {rs.capitalize()}",
                            value=
                            f"But {target.name}'s resources wasn't enough to deal damage by fire."
                        )
                        await ctx.send(embed=embed)
                        return

                    elif ndi > 0:

                        await economy.set_crime_stat(target.id, f"{rs}", ndi)

                        embed.add_field(
                            name=
                            f"You have succesfully arsoned {rs.capitalize()}",
                            value=
                            f"{damage} amount of {rs.capitalize()} destroyed from {target.name.title()}'s resources."
                        )

                elif uroll == troll:
                    embed.add_field(
                        name=f"You couldn't attempt the arson!",
                        value=
                        f"{target.name}'s agents found your actions beforehand."
                    )

                elif uroll < troll:
                    embed.add_field(
                        name=f"Your arson attempt failed!",
                        value=f"{target.name} called Kiki FBI on your arse.")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-angry-fire-element-cartoon-vector-icon-illustration-nature-object-icon-concept-isolated-flat_138676-5769.jpg?w=1380&t=st=1663628813~exp=1663629413~hmac=bab9c1db4fae0bf243c67c5513abff4b9d8a2cce9fdb79610d19a98f9b72bcad"
                )
                await ctx.send(embed=embed)

            else:
                embed.add_field(
                    name="You don't have any molotovs left to attempt arson.",
                    value="Try crafting more.")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-with-knife-cartoon-illustration_138676-3253.jpg?w=1380&t=st=1662086193~exp=1662086793~hmac=d3c530af4f664498e03ad6a3ddad6f924a3164ba6bea7e991b9a13a6477d1d86"
                )
                embed.set_author(name="Kiki Crime")
                await ctx.send(embed=embed)

    ##Rob

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def rob(self, ctx: commands.Context, target: discord.Member):
        embed = discord.Embed(color=discord.Color.random())
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-with-knife-cartoon-illustration_138676-3253.jpg?w=1380&t=st=1662086193~exp=1662086793~hmac=d3c530af4f664498e03ad6a3ddad6f924a3164ba6bea7e991b9a13a6477d1d86"
        )
        embed.set_author(name="Kiki Crime")

        if ctx.author == target:
            embed = discord.Embed(color=discord.Color.random())
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                             icon_url=ctx.message.author.avatar.url)
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-with-knife-cartoon-illustration_138676-3253.jpg?w=1380&t=st=1662086193~exp=1662086793~hmac=d3c530af4f664498e03ad6a3ddad6f924a3164ba6bea7e991b9a13a6477d1d86"
            )
            embed.set_author(name="Kiki Crime")
            embed.add_field(name="You can't rob yourself!",
                            value="Try another victim.")

            await ctx.send(embed=embed)
            return
        else:
            user = ctx.message.author
            target = ctx.message.mentions[0]
            tname = target.name
            data = await economy.get_c_user(user.id)
            inv = data.item
            embed = discord.Embed(color=discord.Color.random())
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                             icon_url=ctx.message.author.avatar.url)
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-with-knife-cartoon-illustration_138676-3253.jpg?w=1380&t=st=1662086193~exp=1662086793~hmac=d3c530af4f664498e03ad6a3ddad6f924a3164ba6bea7e991b9a13a6477d1d86"
            )
            embed.set_author(name="Kiki Crime")
            nitem = "knife"
            if nitem in inv:
                attack = random.randint(1, 100)
                defense = random.randint(1, 100)
                await economy.remove_crime_item(user.id, "knife")
                if attack > defense:
                    embed.add_field(
                        name=
                        "You have successfully made the first move to your victim.",
                        value="Your victim never see you coming.")
                    embed.set_thumbnail(
                        url=
                        "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                    )
                    rob = 1
                    msg = await ctx.send(embed=embed)
                elif attack == defense:
                    embed.add_field(name="Your victim saw you coming.",
                                    value="It's gonna be a tough paw fight.")
                    embed.set_thumbnail(
                        url=
                        "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                    )
                    rob = 2
                    msg = await ctx.send(embed=embed)
                elif attack < defense:
                    embed.add_field(
                        name="Your victim noticed you.",
                        value="Kiki FBI sirens calling. Time to flee.")
                    embed.set_thumbnail(
                        url=
                        "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                    )
                    msg = await ctx.send(embed=embed)
                    return

                await asyncio.sleep(3)
                if rob == 1:
                    attack2 = random.randint(1, 100) + attack
                    defense2 = random.randint(1, 100) + defense
                    chance = int(attack2 - defense2)
                    money = random.randint(10, 50)
                    if attack2 > defense2 and chance > 50:

                        await economy.add_money(user.id, "wallet", money)
                        await economy.remove_money(target.id, "wallet", money)
                        await economy.add_level(user.id, "xp", money)
                        embed.clear_fields()
                        embed.add_field(
                            name=
                            "You have neutralized your victim with your hex magic.",
                            value="Time to snatch some wallets.")
                        embed.add_field(
                            name=
                            f"You have robbed {money} Kiki Coins from {tname.capitalize()}",
                            value=
                            f"{tname.capitalize()} lost {money} amount of Kiki Coins."
                        )
                        embed.add_field(
                            name="You have gained some xp!",
                            value=f"{money} xp added to your progress!")
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        await msg.edit(embed=embed)
                        await economy.add_crime_stat(user, "rob", 1)
                    elif attack2 > defense2 and chance <= 50:

                        await economy.add_money(user.id, "wallet", money)
                        await economy.remove_money(target.id, "wallet", money)
                        await economy.add_level(user.id, "xp", money)
                        embed.clear_fields()
                        embed.add_field(
                            name="You have neutralized your victim with a bat.",
                            value="Time to snatch some money.")
                        embed.add_field(
                            name=
                            f"You have robbed {money} Kiki Coins from {tname.capitalize()}",
                            value=
                            f"{tname.capitalize()} lost {money} amount of Kiki Coins."
                        )
                        embed.add_field(
                            name="You have gained some xp!",
                            value=f"{money} xp added to your progress!")
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        await msg.edit(embed=embed)
                        await economy.add_crime_stat(user, "rob", 1)
                    elif attack2 > defense2 and chance <= 20:

                        await economy.add_money(user.id, "wallet", money)
                        await economy.remove_money(target.id, "wallet", money)
                        await economy.add_level(user.id, "xp", money)
                        embed.clear_fields()
                        embed.add_field(
                            name=
                            "You have barely neutralized your victim in a paw fight.",
                            value="Time to snatch some money.")
                        embed.add_field(
                            name=
                            f"You have robbed {money} Kiki Coins from {tname.capitalize()}",
                            value=
                            f"{tname.capitalize()} lost {money} amount of Kiki Coins."
                        )
                        embed.add_field(
                            name="You have gained some xp!",
                            value=f"{money} xp added to your progress!")
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        await economy.add_crime_stat(user, "rob", 1)
                        await msg.edit(embed=embed)

                    elif attack2 <= defense2:
                        embed.clear_fields()
                        embed.add_field(
                            name="Your victim saw you coming this time.",
                            value="Kiki FBI is on the way. Time to flee.")
                        embed.add_field(
                            name="You have gained some xp!",
                            value=f"{money} xp added to your progress!")
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        await msg.edit(embed=embed)

                if rob == 2:
                    attack2 = random.randint(1, 100) + attack
                    defense2 = random.randint(1, 100) + defense
                    chance = int(attack2 / defense2)
                    money = random.randint(10, 50)
                    if attack2 > defense2 and chance > 1:

                        await economy.add_money(user.id, "wallet", money)
                        await economy.remove_money(target.id, "wallet", money)
                        await economy.add_level(user.id, "xp", money)
                        embed.clear_fields()
                        embed.add_field(
                            name=
                            "You have neutralized your victim with your hex magic.",
                            value="Time to snatch some wallets.")
                        embed.add_field(
                            name=
                            f"You have robbed {money} Kiki Coins from {tname.capitalize()}",
                            value=
                            f"{tname.capitalize()} lost {money} amount of Kiki Coins."
                        )
                        embed.add_field(
                            name="You have gained some xp!",
                            value=f"{money} xp added to your progress!")
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        await economy.add_crime_stat(user, "rob", 1)
                        await msg.edit(embed=embed)

                    elif attack2 > defense2 and chance == 1:

                        await economy.add_money(user.id, "wallet", money)
                        await economy.remove_money(target.id, "wallet", money)
                        await economy.add_level(user.id, "xp", money)
                        embed.clear_fields()
                        embed.add_field(
                            name="You have neutralized your victim with a bat.",
                            value="Time to snatch some money.")
                        embed.add_field(
                            name=
                            f"You have robbed {money} Kiki Coins from {tname.capitalize()}",
                            value=
                            f"{tname.capitalize()} lost {money} amount of Kiki Coins."
                        )
                        embed.add_field(
                            name="You have gained some xp!",
                            value=f"{money} xp added to your progress!")
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        await economy.add_crime_stat(user, "rob", 1)
                        await msg.edit(embed=embed)
                    elif attack2 <= defense2:
                        embed.clear_fields()
                        embed.add_field(
                            name="Your victim saw you coming this time.",
                            value="Kiki FBI is on the way. Time to flee.")
                        embed.add_field(
                            name="You have gained some xp!",
                            value=f"{money} xp added to your progress!")
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/magnet-pull-gold-coin-cartoon-vector-icon-illustration-object-finance-icon-concept-isolated-premium_138676-5437.jpg?w=1380&t=st=1663628949~exp=1663629549~hmac=b391e501f67b1db631080af5249f6a2665d820f6ff09700893fdcd39dcd697c4"
                        )
                        await msg.edit(embed=embed)
                        return
            else:
                embed.add_field(
                    name="You don't have any knives left to attempt rob.",
                    value="Try crafting more.")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                                 icon_url=ctx.message.author.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-with-knife-cartoon-illustration_138676-3253.jpg?w=1380&t=st=1662086193~exp=1662086793~hmac=d3c530af4f664498e03ad6a3ddad6f924a3164ba6bea7e991b9a13a6477d1d86"
                )
                embed.set_author(name="Kiki Crime")
                await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def craft(self, ctx: commands.Context):
        embed = discord.Embed(color=discord.Color.random())
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        embed.set_author(name="Kiki Crime Central Crafting.")
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/premium-vector/cute-cat-playing-yarn-ball-cartoon-icon-illustration_138676-2837.jpg?w=826"
        )
        embed.add_field(
            name="Crafting Options",
            value=
            ".craft smelt <amount>: Uses metal to gain materials. \n .craft lumber <amount>: Uses wood to gain materials. \n .craft grind <amount> Uses stone to gain materials. \n .craft harvest <amount>: Uses plants to gain materials."
        )
        await ctx.send(embed=embed)

    @craft.command()
    async def smelt(self, ctx: commands.Context, amount: int):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author
        data = await economy.get_c_user(user.id)
        metal = data.metal
        if metal == 0:
            embed.add_field(
                name="You don't have enough metal to smelt.",
                value=
                "You require at least 1 metal for smelting. \n Try !gather to gain more resources."
            )
            await ctx.send(embed=embed)
            return
        elif amount > metal:
            embed.add_field(name="You don't have enough metal to smelt.",
                            value="Try lowering your amount.")
            await ctx.send(embed=embed)
            return

        slist = ["iron", "copper", "brass"]
        mlist = [""]
        mlist = mlist[0].split(" | ")
        for i in range(amount):
            chance = random.randint(1, 100)
            if chance >= 66:
                a = random.randint(0, 2)
                m = slist[a]
                mlist.append(m)
                await economy.add_crime_item(user.id, m)
        bucket = [
            f" {mlist.count(i)} x {i.title()}" for i in slist if i in mlist
        ]
        bucket = "\n".join(bucket)
        embed.add_field(name=f"You have smelted {amount} metal successfully.",
                        value=f"{bucket} added to your items.")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        await economy.remove_crime_stat(user.id, "metal", amount)
        await ctx.send(embed=embed)

    @craft.command()
    async def lumber(self, ctx: commands.Context, amount: int):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author
        data = await economy.get_c_user(user.id)
        wood = data.wood
        if wood == 0:
            embed.add_field(
                name="You don't have enough wood to lumber.",
                value=
                "You require at least 1 wood for lumbering. \n Try !gather to gain more resources."
            )
            await ctx.send(embed=embed)
            return
        elif amount > wood:
            embed.add_field(name="You don't have enough wood to lumber.",
                            value="Try lowering your amount.")
            await ctx.send(embed=embed)
            return
        slist = ["handle", "pot", "paper"]
        mlist = [""]
        mlist = mlist[0].split(" | ")
        for i in range(amount):
            chance = random.randint(1, 100)
            if chance >= 66:
                a = random.randint(0, 2)
                m = slist[a]
                mlist.append(m)
                await economy.add_crime_item(user.id, m)
        bucket = [
            f" {mlist.count(i)} x {i.title()}" for i in slist if i in mlist
        ]
        bucket = "\n".join(bucket)
        embed.add_field(name=f"You have lumbered {amount} wood successfully.",
                        value=f"{bucket} added to your items.")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        await economy.remove_crime_stat(user.id, "wood", amount)
        await ctx.send(embed=embed)

    @craft.command()
    async def grind(self, ctx: commands.Context, amount: int):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author
        data = await economy.get_c_user(user.id)
        stone = data.stone
        if stone == 0:
            embed.add_field(
                name="You don't have enough stone to grind.",
                value=
                "You require at least 1 stone for grinding. \n Try !gather to gain more resources."
            )
            await ctx.send(embed=embed)
            return
        elif amount > stone:
            embed.add_field(name="You don't have enough stone to grind.",
                            value="Try lowering your amount.")
            await ctx.send(embed=embed)
            return
        slist = ["blackpowder", "glass", "pot"]
        mlist = [""]
        mlist = mlist[0].split(" | ")
        for i in range(amount):
            chance = random.randint(1, 100)
            if chance >= 66:
                a = random.randint(0, 2)
                m = slist[a]
                mlist.append(m)
                await economy.add_crime_item(user.id, m)
        bucket = [
            f" {mlist.count(i)} x {i.title()}" for i in slist if i in mlist
        ]
        bucket = "\n".join(bucket)
        embed.add_field(name=f"You have grinded {amount} stone successfully.",
                        value=f"{bucket} added to your items.")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        await economy.remove_crime_stat(user.id, "stone", amount)
        await ctx.send(embed=embed)

    @craft.command()
    async def harvest(self, ctx: commands.Context, amount: int):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author
        data = await economy.get_c_user(user.id)
        plant = data.plant
        if plant == 0:
            embed.add_field(
                name="You don't have enough plants to harvest.",
                value=
                "You require at least 1 plant for harvesting. \n Try !gather to gain more resources."
            )
            await ctx.send(embed=embed)
            return
        elif amount > plant:
            embed.add_field(name="You don't have enough plants to harvest.",
                            value="Try lowering your amount.")
            await ctx.send(embed=embed)
            return
        slist = ["seed", "fruit", "paper"]
        mlist = [""]
        mlist = mlist[0].split(" | ")
        for i in range(amount):
            chance = random.randint(1, 100)
            if chance >= 66:
                a = random.randint(0, 2)
                m = slist[a]
                mlist.append(m)
                await economy.add_crime_item(user.id, m)
        bucket = [
            f" {mlist.count(i)} x {i.title()}" for i in slist if i in mlist
        ]
        bucket = "\n".join(bucket)
        embed.add_field(
            name=f"You have harvested {amount} plant successfully.",
            value=f"{bucket} added to your items.")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        await economy.remove_crime_stat(user.id, "plant", amount)
        await ctx.send(embed=embed)

    @craft.command()
    async def goods(self, ctx: commands.Context):
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name="Crafting Goods!")
        view = CraftView(ctx)
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed, view=view)
        await view.wait()

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def deal(self, ctx: commands.Context):
        embed = discord.Embed(color=discord.Color.random())
        user = ctx.message.author
        data = await economy.get_c_user(user.id)
        inv = data.item
        i1 = "weed"
        i2 = "coins"
        ni2c = 0

        if i1 not in inv:
            i1c = 0

            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(
                name=f"You don't have any {i1.title()} to sell.",
                value=
                f"Try gathering more resources and crafting more {i1.title()}."
            )
            await ctx.send(embed=embed)
            return
        else:
            i1c = countOf(inv, i1)
            await economy.add_crime_stat(user.id, "deal", 1)

        for i in range(i1c):
            i2c = random.randint(5, 12)
            ni2c = i2c + ni2c
            await economy.remove_crime_item(user.id, i1)
            await economy.add_money(user.id, "wallet", i2c)

            

        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)
        embed.add_field(
            name=f"You have successfully sell your {i1c}x {i1.title()}",
            value=f"You have gained {ni2c} {i2.title()}.")
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/premium-vector/cute-cat-sitting-laptop-icon-illustration_138676-85.jpg?w=1060"
        )
        await ctx.send(embed=embed)


class CraftView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label='Weed Pot',
                       style=discord.ButtonStyle.green,
                       emoji="☘",
                       custom_id="wp")
    async def cr1(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]

        user = await economy.get_c_user(interaction.user.id)
        inv = user.item

        i1 = "pot"
        i2 = "seed"
        i3 = "weed pot"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        check1 = [i1c, i2c]
        
        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i3.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**")
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i3c+1}x **{i3.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i3)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_item(interaction.user.id, i2)

            check2 = [ni1c, ni2c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i3.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i3c+1}x **{i3.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = True
                button2.disabled = False
                button3.disabled = False
                button4.disabled = False
                button5.disabled = False
                button6.disabled = False
                button7.disabled = False
                button8.disabled = False
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = True
            button2.disabled = False
            button3.disabled = False
            button4.disabled = False
            button5.disabled = False
            button6.disabled = False
            button7.disabled = False
            button8.disabled = False
            button9.disabled = False

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Gun',
                       style=discord.ButtonStyle.green,
                       emoji="🔫",
                       custom_id="gun")
    async def cr2(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]
        user = await economy.get_c_user(interaction.user.id)
        inv = user.item

        i1 = "bullet"
        i2 = "iron"
        i3 = "gun"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        check1 = [i1c, i2c]
        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i3.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**")
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i3c+1}x **{i3.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i3)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_item(interaction.user.id, i2)

            check2 = [ni1c, ni2c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i3.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i3c+1}x **{i3.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = False
                button2.disabled = True
                button3.disabled = False
                button4.disabled = False
                button5.disabled = False
                button6.disabled = False
                button7.disabled = False
                button8.disabled = False
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = False
            button2.disabled = True
            button3.disabled = False
            button4.disabled = False
            button5.disabled = False
            button6.disabled = False
            button7.disabled = False
            button8.disabled = False
            button9.disabled = False

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Knife',
                       style=discord.ButtonStyle.green,
                       emoji="🔪",
                       custom_id="knife")
    async def cr3(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]
        user = await economy.get_c_user(interaction.user.id)
        inv = user.item

        i1 = "handle"
        i2 = "iron"
        i3 = "knife"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        check1 = [i1c, i2c]
        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i3.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**")
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i3c+1}x **{i3.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i3)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_item(interaction.user.id, i2)

            check2 = [ni1c, ni2c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i3.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i3c+1}x **{i3.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = False
                button2.disabled = False
                button3.disabled = True
                button4.disabled = False
                button5.disabled = False
                button6.disabled = False
                button7.disabled = False
                button8.disabled = False
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = False
            button2.disabled = False
            button3.disabled = True
            button4.disabled = False
            button5.disabled = False
            button6.disabled = False
            button7.disabled = False
            button8.disabled = False
            button9.disabled = False

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Bullet',
                       style=discord.ButtonStyle.green,
                       emoji="🎯",
                       custom_id="bullet")
    async def cr4(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]
        user = await economy.get_c_user(interaction.user.id)
        inv = user.item

        i1 = "copper"
        i2 = "blackpowder"
        i3 = "bullet"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        check1 = [i1c, i2c]
        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i3.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**")
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i3c+1}x **{i3.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i3)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_item(interaction.user.id, i2)

            check2 = [ni1c, ni2c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i3.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i3c+1}x **{i3.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = False
                button2.disabled = False
                button3.disabled = False
                button4.disabled = True
                button5.disabled = False
                button6.disabled = False
                button7.disabled = False
                button8.disabled = False
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = False
            button2.disabled = False
            button3.disabled = False
            button4.disabled = True
            button5.disabled = False
            button6.disabled = False
            button7.disabled = False
            button8.disabled = False
            button9.disabled = False

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Knuckle',
                       style=discord.ButtonStyle.green,
                       emoji="👊",
                       custom_id="knuckle")
    async def cr5(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]
        user = await economy.get_c_user(interaction.user.id)
        inv = user.item

        i1 = "handle"
        i2 = "brass"
        i3 = "knuckle"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        check1 = [i1c, i2c]
        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i3.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**")
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i3c+1}x **{i3.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i3)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_item(interaction.user.id, i2)

            check2 = [ni1c, ni2c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i3.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** and 1x **{i2.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** and {ni2c}x **{i2.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i3c+1}x **{i3.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = False
                button2.disabled = False
                button3.disabled = False
                button4.disabled = False
                button5.disabled = True
                button6.disabled = False
                button7.disabled = False
                button8.disabled = False
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = False
            button2.disabled = False
            button3.disabled = False
            button4.disabled = False
            button5.disabled = True
            button6.disabled = False
            button7.disabled = False
            button8.disabled = False
            button9.disabled = False

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Alcohol',
                       style=discord.ButtonStyle.green,
                       emoji="🍾",
                       custom_id="alc")
    async def cr6(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]
        user = await economy.get_c_user(interaction.user.id)
        inv = user.item
        water = user.water

        i1 = "fruit"
        i2 = "brass"
        i3 = "water"
        i4 = "alcohol"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i4 not in inv:
            i4c = 0
        else:
            i4c = countOf(inv, i4)
        check1 = [i1c, i2c, water]

        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            ni3c = water - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i4.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** , 1x **{i2.title()}** and 1x **{i3.title()}"
            )
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** , {ni2c}x **{i2.title()}** and {ni3c}x **{i3.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i4c+1}x **{i4.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i4)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_item(interaction.user.id, i2)
            await economy.remove_crime_stat(interaction.user.id, i3, 1)

            check2 = [ni1c, ni2c, ni3c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i4.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** , 1x **{i2.title()}** and 1x **{i3.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** , {ni2c}x **{i2.title()}** and {ni3c}x **{i3.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i4c+1}x **{i4.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = False
                button2.disabled = False
                button3.disabled = False
                button4.disabled = False
                button5.disabled = False
                button6.disabled = True
                button7.disabled = False
                button8.disabled = False
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

            await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = False
            button2.disabled = False
            button3.disabled = False
            button4.disabled = False
            button5.disabled = False
            button6.disabled = True
            button7.disabled = False
            button8.disabled = False
            button9.disabled = False

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Molotov',
                       style=discord.ButtonStyle.green,
                       emoji="🔥",
                       custom_id="molotov")
    async def cr7(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]
        user = await economy.get_c_user(interaction.user.id)
        inv = user.item

        i1 = "glass"
        i2 = "paper"
        i3 = "alcohol"
        i4 = "molotov"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        if i2 not in inv:
            i2c = 0
        else:
            i2c = countOf(inv, i2)

        if i3 not in inv:
            i3c = 0
        else:
            i3c = countOf(inv, i3)

        if i4 not in inv:
            i4c = 0
        else:
            i4c = countOf(inv, i4)
        check1 = [i1c, i2c, i3c]

        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            ni3c = i3c - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i4.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** , 1x **{i2.title()}** and 1x **{i3.title()}**"
            )
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** , {ni2c}x **{i2.title()}** and {ni3c}x **{i3.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i4c+1}x **{i4.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i4)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_item(interaction.user.id, i2)
            await economy.remove_crime_item(interaction.user.id, i3)

            check2 = [ni1c, ni2c, ni3c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i4.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** , 1x **{i2.title()}** and 1x **{i3.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** , {ni2c}x **{i2.title()}** and {ni3c}x **{i3.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i4c+1}x **{i4.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = False
                button2.disabled = False
                button3.disabled = False
                button4.disabled = False
                button5.disabled = False
                button6.disabled = False
                button7.disabled = True
                button8.disabled = False
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

            await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = False
            button2.disabled = False
            button3.disabled = False
            button4.disabled = False
            button5.disabled = False
            button6.disabled = False
            button7.disabled = True
            button8.disabled = False
            button9.disabled = False

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Weed',
                       style=discord.ButtonStyle.green,
                       emoji="🌵",
                       custom_id="weed")
    async def cr8(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "wp"][0]
        button2 = [x for x in self.children if x.custom_id == "gun"][0]
        button3 = [x for x in self.children if x.custom_id == "knife"][0]
        button4 = [x for x in self.children if x.custom_id == "bullet"][0]
        button5 = [x for x in self.children if x.custom_id == "knuckle"][0]
        button6 = [x for x in self.children if x.custom_id == "alc"][0]
        button7 = [x for x in self.children if x.custom_id == "molotov"][0]
        button8 = [x for x in self.children if x.custom_id == "weed"][0]
        button9 = [x for x in self.children if x.custom_id == "quit"][0]
        user = await economy.get_c_user(interaction.user.id)
        inv = user.item
        water = user.water
        elec = user.electric

        i1 = "weed pot"
        i2 = "water"
        i3 = "electric"
        i4 = "weed"

        if i1 not in inv:
            i1c = 0
        else:
            i1c = countOf(inv, i1)

        i2c = water
        i3c = elec

        if i4 not in inv:
            i4c = 0
        else:
            i4c = countOf(inv, i4)
        check1 = [i1c, i2c, i3c]

        if all(cc != 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            ni1c = i1c - 1
            ni2c = i2c - 1
            ni3c = i3c - 1
            embed.set_author(name="Craft Successful!")
            embed.add_field(
                name=f"You have crafted **{i4.title()}**",
                value=
                f"You have spent 1x **{i1.title()}** , 1x **{i2.title()}** and 1x **{i3.title()}**"
            )
            embed.add_field(
                name="You now have remaining:",
                value=
                f"{ni1c}x **{i1.title()}** , {ni2c}x **{i2.title()}** and {ni3c}x **{i3.title()}** remaining."
            )
            embed.add_field(name="You have now:",
                            value=f"{i4c+1}x **{i4.title()}**")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))

            await economy.add_crime_item(interaction.user.id, i4)
            await economy.remove_crime_item(interaction.user.id, i1)
            await economy.remove_crime_stat(interaction.user.id, i2, 1)
            await economy.remove_crime_stat(interaction.user.id, i3, 1)

            check2 = [ni1c, ni2c, ni3c]
            if any(cc == 0 for cc in check2):
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name="Craft Successful!")
                embed.add_field(
                    name=f"You have crafted **{i4.title()}**",
                    value=
                    f"You have spent 1x **{i1.title()}** , 1x **{i2.title()}** and 1x **{i3.title()}**"
                )
                embed.add_field(
                    name="You now have remaining:",
                    value=
                    f"{ni1c}x **{i1.title()}** , {ni2c}x **{i2.title()}** and {ni3c}x **{i3.title()}** remaining."
                )
                embed.add_field(name="You have now:",
                                value=f"{i4c+1}x **{i4.title()}**")
                embed.add_field(name="You don't have **enough** materials.",
                                value="Please come back when you gather more!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                button1.disabled = False
                button2.disabled = False
                button3.disabled = False
                button4.disabled = False
                button5.disabled = False
                button6.disabled = False
                button7.disabled = False
                button8.disabled = True
                button9.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

            await interaction.response.edit_message(embed=embed, view=self)

        if any(cc == 0 for cc in check1):
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="You don't have **enough** materials.",
                            value="Please come back when you gather more!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            button1.disabled = False
            button2.disabled = False
            button3.disabled = False
            button4.disabled = False
            button5.disabled = False
            button6.disabled = False
            button7.disabled = False
            button8.disabled = True
            button9.disabled = False
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Quit",
                       style=discord.ButtonStyle.red,
                       custom_id="quit",
                       emoji="✖")
    async def cr9(self, interaction: discord.Interaction,
                  button: discord.ui.Button):
        self.clear_items()
        self.stop()
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Come back again!")
        embed.add_field(name="You have quit from the craft central!",
                        value="Gather more for progress!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                         icon_url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed, view=None)

    async def interaction_check(self,
                                interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            embed = discord.Embed(color=discord.Color.random())
            embed = discord.Embed(title="The current screen is not yours.",
                                  description="Please try again")
            embed.add_field(name="Did you try starting your own journey?",
                            value="Start with !daily and join the mini games.")
            embed.set_footer(text="***Summon screen belongs to {}***".format(
                self.ctx.author.name),
                             icon_url=(self.ctx.author.avatar))
            embed.set_thumbnail(
                url=
                "https://i.pinimg.com/originals/4f/c6/59/4fc659d1c70c6a5ded85595c8e19a3d8.png"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
            return False

        else:
            return True
            
async def setup(bot):
    await bot.add_cog(crime(bot))
