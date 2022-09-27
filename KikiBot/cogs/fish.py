from code import interact
from itertools import count
from operator import countOf
from site import venv
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
from lists.itemslist import *
import tracemalloc
from main import economy
from lists.itemslist import *
from lists.fishinglist import *
from lists.fishes import *
from collections import Counter


class FView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Fish",
                       style=discord.ButtonStyle.green,
                       emoji="🐟",
                       custom_id="fish")
    async def gbut1(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "fish"][0]
        button2 = [x for x in self.children if x.custom_id == "net"][0]
        button3 = [x for x in self.children if x.custom_id == "sail"][0]
        button4 = [x for x in self.children if x.custom_id == "quit"][0]
        button1.label = "Fishing"
        button1.disabled = True
        button4.disabled = True
        user = interaction.user
        data1 = await economy.get_user_lvl(user.id)
        data2 = await economy.get_user(user.id)
        fdata = data1.fish
        inv = data2.items

        fbaitlure = [f"{i}" for i in fbal if i in inv]

        count2 = len(fbaitlure)

        if count2 != 0:
            self.remove_item(button2)
            self.remove_item(button3)
            bait = random.choice(fbaitlure)
            await economy.remove_item(user.id, bait)
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(
                name=f"You have prepared {bait.title()} for casting!",
                value="Your chance to catch better fishes increased.")
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/cute-cat-catching-fish-with-ufo-cartoon-vector-icon-illustration-animal-technology-icon-isolated_138676-4791.jpg?w=826"
            )
            embed.set_footer(text=f"Invoked by {user.name}",
                             icon_url=user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=self)
            await asyncio.sleep(2)

            fgear = [f"{i}" for i in f_rods if i in inv]

            count1 = len(fgear)

            fc = 0
            control = []
            while count1 != 0:
                for i in range(count1):
                    if "spin fishing rod" in fgear and "1" not in control:
                        control.append("1")
                        fc = fc + 1
                    else:
                        fc = fc + 0
                    if "telescope rod" in fgear and "2" not in control:
                        control.append("2")
                        fc = fc + 2
                    else:
                        fc = fc + 0
                    if "carbon fiber rod" in fgear and "3" not in control:
                        control.append("3")
                        fc = fc + 3
                    else:
                        fc = fc + 0
                    if "kiki 3000 fisher" in fgear and "4" not in control:
                        control.append("4")
                        fc = fc + 4
                    else:
                        fc = fc + 0
                    if "embezzled rod" in fgear and "5" not in control:
                        control.append("5")
                        fc = fc + 5
                    else:
                        fc = fc + 0
                break

            if bait == "worms":
                bchance = 5
            elif bait == "dough":
                bchance = 3
            elif bait == "leeches":
                bchance = 6
            elif bait == "insects":
                bchance = 10
            elif bait == "mussels":
                bchance = 20
            elif bait == "jiggs":
                bchance = 20
            elif bait == "spinnerbait":
                bchance = 25
            elif bait == "flies":
                bchance = 35
            elif bait == "spoons":
                bchance = 35

            echance = fc + fdata + bchance

            if echance >= 0 and echance <= 25:
                fishes = fishcategory_list["Stream Fishes"].items()
                a = random.choice(list(fishes))

                name = a[0].lower()
                des = a[1]['description']
                thumb = a[1]['thumb']
                xp = a[1]['xp']
            elif echance > 25 and echance <= 50:
                fishes = fishcategory_list["Dock Fishes"].items()
                a = random.choice(list(fishes))

                name = a[0].lower()
                des = a[1]['description']
                thumb = a[1]['thumb']
                xp = a[1]['xp']
            elif echance > 50:
                fishes = fishcategory_list["Oceanic Fishes"].items()
                a = random.choice(list(fishes))

                name = a[0].lower()
                des = a[1]['description']
                thumb = a[1]['thumb']
                xp = a[1]['xp']

            rod = "rod" if not fgear else random.choice(fgear).title()
            embed = discord.Embed(color=discord.Color.random())
            embed = discord.Embed(title=f"You started casting your {rod}!",
                                  description="Fishes be bitin!")
            embed.set_author(name="Kiki Fishing Central")
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/cute-cat-catching-fish-with-ufo-cartoon-vector-icon-illustration-animal-technology-icon-isolated_138676-4791.jpg?w=826"
            )
            await interaction.message.edit(embed=embed, view=self)
            await asyncio.sleep(2)
            embed.set_author(name="You have caught!!")
            embed.add_field(name=f"{name.title()}", value=f"*{des}*")
            embed.add_field(name="You have gained some xp!",
                            value=f"{xp} xp added to your progress!")
            embed.set_footer(text=f"Invoked by {user.name}",
                             icon_url=user.avatar.url)
            embed.set_thumbnail(url=f"{thumb}")
            button1.label = "Continue Fishing"
            button1.disabled = False
            button4.disabled = False
            await economy.add_xp(user.id, "xp", xp)
            await economy.add_item(user.id, name)
            await interaction.message.edit(embed=embed, view=self)
            self.add_item(button2)
            self.add_item(button3)
        else:
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(
                name="You don't have any bait to fish.",
                value=
                "Try buying baits from !shop or try other options instead.")
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/cute-cat-catching-fish-with-ufo-cartoon-vector-icon-illustration-animal-technology-icon-isolated_138676-4791.jpg?w=826"
            )
            embed.set_footer(text=f"Invoked by {user.name}",
                             icon_url=user.avatar.url)
            button1.disabled = True
            button2.disabled = False
            button3.disabled = False
            button4.disabled = False
            self.timeout = None
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Net",
                       style=discord.ButtonStyle.red,
                       emoji="🥽",
                       custom_id="net")
    async def gbut2(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "fish"][0]
        button2 = [x for x in self.children if x.custom_id == "net"][0]
        button3 = [x for x in self.children if x.custom_id == "sail"][0]
        button4 = [x for x in self.children if x.custom_id == "quit"][0]
        button1.disabled = True
        button2.disabled = True
        button3.disabled = True
        button4.disabled = True

        user = interaction.user
        data1 = await economy.get_user_lvl(user.id)
        data2 = await economy.get_user(user.id)
        flvl = data1.fish
        inv = data2.items

        fgear = [f"{i}" for i in f_nets if i in inv]
        cnets = len(fgear)
        net = "net" if not fgear else random.choice(fgear).title()

        if flvl >= 5:
            if cnets != 0:
                fc = 0
                control = []
                while cnets != 0:
                    for i in range(cnets):
                        if "stick net" in fgear and "1" not in control:
                            control.append("1")
                            fc = fc + 1
                        else:
                            fc = fc + 0
                        if "dredge" in fgear and "2" not in control:
                            control.append("2")
                            fc = fc + 2
                        else:
                            fc = fc + 0
                        if "gillnet" in fgear and "3" not in control:
                            control.append("3")
                            fc = fc + 2
                        else:
                            fc = fc + 0
                        if "purse seine" in fgear and "4" not in control:
                            control.append("4")
                            fc = fc + 4
                        else:
                            fc = fc + 0
                        if "trap" in fgear and "5" not in control:
                            control.append("5")
                            fc = fc + 5
                        else:
                            fc = fc + 0
                    break
                if net == "Stick Net":
                    bchance = 15
                    fn = random.randint(5, 10)
                elif net == "Dredge":
                    bchance = 20
                    fn = random.randint(7, 12)
                elif net == "Gillnet":
                    bchance = 25
                    fn = random.randint(9, 15)
                elif net == "Purse Seine":
                    bchance = 30
                    fn = random.randint(9, 15)
                elif net == "Trap":
                    bchance = 35
                    fn = random.randint(9, 15)

                echance = fc + flvl + bchance
                fishess = [""]
                fishesss = fishess[0].split(" | ")
                net = random.choice(fgear)
                await economy.remove_item(user.id, net)
                embed = discord.Embed(color=discord.Color.random())
                embed.add_field(
                    name=f"You have prepared {net.title()} for casting!",
                    value="Time to snatch fishes!")
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-catching-fish-with-fishing-net-cartoon-vector-icon-illustration-animal-nature-isolated_138676-5505.jpg"
                )
                embed.set_footer(text=f"Invoked by {user.name}",
                                 icon_url=user.avatar.url)
                await interaction.response.edit_message(embed=embed, view=self)
                await asyncio.sleep(2)

                if echance >= 5 and echance <= 25:
                    fishes = fishcategory_list["Stream Fishes"].items()
                    xp = random.randint(5, 25)
                    for i in range(fn):
                        a = random.choice(list(fishes))
                        name = a[0].lower()
                        fishesss.append(name)
                        await economy.add_item(user.id, name)

                elif echance > 25 and echance <= 50:
                    fishes = fishcategory_list["Dock Fishes"].items()
                    xp = random.randint(25, 50)
                    for i in range(fn):
                        a = random.choice(list(fishes))
                        name = a[0].lower()
                        fishesss.append(name)
                        await economy.add_item(user.id, name)
                elif echance > 50:
                    fishes = fishcategory_list["Oceanic Fishes"].items()
                    xp = random.randint(50, 100)
                    for i in range(fn):
                        a = random.choice(list(fishes))
                        name = a[0].lower()
                        fishesss.append(name)
                        await economy.add_item(user.id, name)

                bucket = [
                    f" {fishesss.count(i)} x {i.title()}" for i in fishes_list
                    if i in fishesss
                ]
                bucket = "\n".join(bucket)

                embed = discord.Embed(color=discord.Color.random())
                embed = discord.Embed(
                    title=
                    f"You have thrown your {net.title()} to the vast sea!",
                    description="Seems like this gonna be a good catch!")
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-catching-fish-with-fishing-net-cartoon-vector-icon-illustration-animal-nature-isolated_138676-5505.jpg"
                )
                embed.set_footer(text=f"Invoked by {user.name}",
                                 icon_url=user.avatar.url)
                embed.set_author(name="Kiki Fishing Central")
                await interaction.message.edit(embed=embed, view=self)
                await asyncio.sleep(2)
                embed.clear_fields()
                self.remove_item(button3)
                self.remove_item(button1)
                button2.label = "Continue Net"
                button2.disabled = False
                button4.disabled = False
                embed.add_field(name="You have filled your buckets with:",
                                value=f"**{bucket}**")
                embed.add_field(name="You have gained some xp!",
                                value=f"{xp} xp added to your progress!")
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/premium-vector/cute-cat-bring-fish-with-trolley-cartoon-vector-icon-illustration-animal-nature-icon-isolated-flat_138676-5771.jpg?w=1380"
                )
                embed.set_footer(text=f"Invoked by {user.name}",
                                 icon_url=user.avatar.url)
                await economy.add_xp(user.id, "xp", xp)
                await interaction.message.edit(embed=embed, view=self)
                self.add_item(button1)
                self.add_item(button3)

            else:
                embed = discord.Embed(color=discord.Color.random())
                embed.add_field(
                    name="You don't have any net to fish.",
                    value=
                    "Try buying nets from !shop or try other options instead!."
                )
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/premium-vector/cute-cat-catching-fish-with-ufo-cartoon-vector-icon-illustration-animal-technology-icon-isolated_138676-4791.jpg?w=826"
                )
                embed.set_footer(text=f"Invoked by {user.name}",
                                 icon_url=user.avatar.url)
                button1.disabled = False
                button2.disabled = True
                button3.disabled = False
                button4.disabled = False
                self.timeout = None
                await interaction.response.edit_message(embed=embed, view=self)

        else:
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(
                name="Your fishing level is not enough to use a net!",
                value=
                f"You need to be at least **level 5** for using Net. \n\n Your current fishing level is **{flvl}**."
            )
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-catching-fish-with-fishing-net-cartoon-vector-icon-illustration-animal-nature-isolated_138676-5505.jpg"
            )
            embed.set_footer(text=f"Invoked by {user.name}",
                             icon_url=user.avatar.url)
            embed.set_author(name="Kiki Fishing Central")
            button1.disabled = False
            button2.disabled = True
            button3.disabled = True
            button4.disabled = False
            self.timeout = None
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Sail",
                       style=discord.ButtonStyle.blurple,
                       emoji="⚓",
                       custom_id="sail")
    async def gbut3(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        r = await economy.get_user_lvl(interaction.user.id)
        data = await economy.get_user(interaction.user.id)
        inv = data.items
        flvl = r.fish
        button1 = [x for x in self.children if x.custom_id == "fish"][0]
        button2 = [x for x in self.children if x.custom_id == "net"][0]
        button3 = [x for x in self.children if x.custom_id == "sail"][0]
        button4 = [x for x in self.children if x.custom_id == "quit"][0]

        fgear = [f"{i}" for i in f_ships if i in inv]

        count = len(fgear)
        embed = discord.Embed(color=discord.Color.random())
        if flvl >= 10:
            if count != 0:
                ship = "ship" if not fgear else random.choice(fgear).title()
                fc = 0
                control = []
                while count != 0:
                    for i in range(count):
                        if "raft" in fgear and "1" not in control:
                            control.append("1")
                            fc = fc + 1
                        else:
                            fc = fc + 0
                        if "sloop" in fgear and "2" not in control:
                            control.append("2")
                            fc = fc + 2
                        else:
                            fc = fc + 0
                        if "barque" in fgear and "3" not in control:
                            control.append("3")
                            fc = fc + 3
                        else:
                            fc = fc + 0
                        if "clipper" in fgear and "4" not in control:
                            control.append("4")
                            fc = fc + 4
                        else:
                            fc = fc + 0
                        if "long boat" in fgear and "5" not in control:
                            control.append("5")
                            fc = fc + 5
                        else:
                            fc = fc + 0
                        if "frigate " in fgear and "6" not in control:
                            control.append("6")
                            fc = fc + 6
                        else:
                            fc = fc + 0
                        if "ghost ship" in fgear and "7" not in control:
                            control.append("7")
                            fc = fc + 7
                        else:
                            fc = fc + 0
                    break
                if ship == "Raft":
                    bchance = 15
                elif ship == "Sloop":
                    bchance = 20
                elif ship == "Barque":
                    bchance = 25
                elif ship == "Clipper":
                    bchance = 30
                elif ship == "Long Boat":
                    bchance = 35
                elif ship == "Frigate":
                    bchance = 40
                elif ship == "Ghost Ship":
                    bchance = 50

                echance = fc + flvl + bchance
                chance = random.uniform(0, 100)

                embed = discord.Embed(color=discord.Color.random())
                embed = discord.Embed(
                    title="Sailing Journey Started",
                    description=
                    "An epic journey for sea artifacts, Beware Pirates!")
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/premium-vector/cute-cat-fishing-sea-boat-cartoon-icon-illustration_138676-2265.jpg?w=2000"
                )
                embed.set_author(name="Kiki Fishing Central")

                await interaction.response.edit_message(embed=embed, view=self)
                await asyncio.sleep(2)
                embed.clear_fields()
                embed.add_field(
                    name="Your search continues...",
                    value=f"Your {ship} sailing smoothly in the ocean.")
                embed.set_author(name="Kiki Fishing Central")
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/treasure-map-with-magnifying-glass-cartoon-vector-icon-illustration-education-nature-icon-isolated_138676-4864.jpg?w=1380&t=st=1663638828~exp=1663639428~hmac=8be95f37111217daec1a4e34788dc1b5a362b568efe8bc64ff27de67865de9e5"
                )
                await interaction.message.edit(embed=embed)

                await asyncio.sleep(2)
                a = random.randint(0, 6)
                fail = sailfails[a]
                if echance > 25 and echance <= 35:

                    if chance <= 30:
                        art = f_collectibles["Common"].items()
                        rarity = "Common"
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']

                    elif chance > 30:
                        embed.add_field(
                            name=f"{fail}",
                            value="Wishing you luck on your next journey.")
                        embed.set_author(name="Kiki Fishing Central")
                        embed.set_footer(
                            text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/cute-cat-holding-fish-board-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated_138676-5221.jpg?w=2000"
                        )
                        await interaction.message.edit(embed=embed)

                elif echance > 35 and echance <= 50:

                    if chance < 17:
                        art = f_collectibles["Uncommon"].items()
                        rarity = "Uncommon"
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']

                    elif chance >= 17 and chance <= 30:
                        rarity = "Common"
                        art = f_collectibles["Common"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                    elif chance > 30:
                        embed.add_field(
                            name=f"{fail}",
                            value="Wishing you luck on your next journey.")
                        embed.set_author(name="Kiki Fishing Central")
                        embed.set_footer(
                            text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/cute-cat-holding-fish-board-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated_138676-5221.jpg?w=2000"
                        )
                        await interaction.message.edit(embed=embed)

                elif echance > 50 and echance <= 65:

                    if chance < 10:
                        art = f_collectibles["Rare"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Rare"
                    elif chance >= 10 and echance < 17:
                        art = f_collectibles["Uncommon"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Uncommon"
                    elif chance >= 17 and chance <= 30:
                        art = f_collectibles["Common"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Common"

                    elif chance > 30:
                        embed.add_field(
                            name=f"{fail}",
                            value="Wishing you luck on your next journey.")
                        embed.set_author(name="Kiki Fishing Central")
                        embed.set_footer(
                            text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/cute-cat-holding-fish-board-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated_138676-5221.jpg?w=2000"
                        )
                        await interaction.message.edit(embed=embed)

                elif echance > 65 and chance <= 80:

                    if chance < 5:
                        art = f_collectibles["Epic"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Epic"

                    elif chance >= 5 and chance < 10:
                        art = f_collectibles["Rare"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Rare"

                    elif chance >= 10 and chance < 17:
                        art = f_collectibles["Uncommon"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Uncommon"

                    elif chance >= 17 and chance <= 30:
                        art = f_collectibles["Common"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Common"

                    elif chance > 30:
                        embed.add_field(
                            name=f"{fail}",
                            value="Wishing you luck on your next journey.")
                        embed.set_author(name="Kiki Fishing Central")
                        embed.set_footer(
                            text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/cute-cat-holding-fish-board-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated_138676-5221.jpg?w=2000"
                        )
                        await interaction.message.edit(embed=embed)

                elif echance > 80:

                    if chance <= 30 and chance > 17:
                        art = f_collectibles["Common"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Common"
                        await economy.add_item(interaction.user.id, name)
                    elif chance >= 10 and chance < 17:
                        art = f_collectibles["Uncommon"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Uncommon"
                    elif chance >= 5 and chance < 10:
                        art = f_collectibles["Rare"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Rare"
                    elif chance >= 3 and chance < 5:
                        art = f_collectibles["Epic"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Epic"
                    elif chance < 3:
                        art = f_collectibles["Legendary"].items()
                        aitem = random.choice(list(art))
                        name = aitem[0].lower()
                        des = aitem[1]['description']
                        rarity = "Legendary"

                    elif chance > 30:
                        embed.add_field(
                            name=f"{fail}",
                            value="Wishing you luck on your next journey.")
                        embed.set_author(name="Kiki Fishing Central")
                        embed.set_footer(
                            text=f"Invoked by {interaction.user.name}",
                            icon_url=interaction.user.avatar.url)
                        embed.set_thumbnail(
                            url=
                            "https://img.freepik.com/free-vector/cute-cat-holding-fish-board-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated_138676-5221.jpg?w=2000"
                        )
                        await interaction.message.edit(embed=embed)

                if name in inv:
                    if rarity == "Common":
                        coins = 20
                    elif rarity == "Uncommon":
                        coins = 30
                    elif rarity == "Rare":
                        coins = 50
                    elif rarity == "Epic":
                        coins = 70
                    elif rarity == "Legendary":
                        coins = 100
                    embed.clear_fields()
                    embed.add_field(
                        name="You have successfully finished your journey!",
                        value=
                        f"You have found another  **{name.title()}** \n\n Kiki Appraiser said it's a fake but take the item from you in exchange some coins."
                    )
                    embed.add_field(
                        name="You have gained:",
                        value=f"{coins} Kiki Coins for your efforts.")
                    await economy.add_money(interaction.user.id, "wallet",
                                            coins)
                else:
                    embed.clear_fields()
                    embed.add_field(
                        name="You have successfully finished your journey!",
                        value=
                        f"You have brought back **{name.title()}** from the sea riches. \n\n Kiki Appraiser says: It's {rarity} item. It can be described as: **{des}** about your new artifact."
                    )
                    await economy.add_item(interaction.user.id, name)
                embed.set_author(name="Kiki Fishing Central")
                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                 icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/premium-vector/treasure-cartoon-icon-illustration_138676-1963.jpg?w=1380"
                )
                await interaction.message.edit(embed=embed)

            else:
                embed.add_field(
                    name="You don't have a ship to sail.",
                    value="Try buying one from !shop to start your journey.")
                embed.set_author(name="Kiki Fishing Central")
                embed.set_footer(text=f"Invoked by {interaction.user.name}",
                                 icon_url=interaction.user.avatar.url)
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-holding-fish-board-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolated_138676-5221.jpg?w=2000"
                )
                button3.disabled = True
                await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(
                name="Your fishing level is not enough to go sailing!",
                value=
                f"You need to be at least **level 10** to sail across. \n\n Your current fishing level is **{flvl}**."
            )
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-catching-fish-with-fishing-net-cartoon-vector-icon-illustration-animal-nature-isolated_138676-5505.jpg"
            )
            embed.set_author(name="Kiki Fishing Central")
            button3.disabled = True
            self.timeout = None
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Quit",
                       style=discord.ButtonStyle.red,
                       custom_id="quit",
                       emoji="✖")
    async def gbut4(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        self.clear_items()
        self.stop()
        self.value = "4"
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Come back soon!")
        embed.add_field(name="You have quit from fishing central!",
                        value="Don't forget to pack your buckets!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                         icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/premium-vector/cute-cat-shopping-cartoon-icon-illustration_138676-2844.jpg?w=1380"
        )
        await interaction.response.edit_message(embed=embed, view=None)

    async def interaction_check(self,
                                interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            embed = discord.Embed(color=discord.Color.random())
            embed = discord.Embed(title="The current screen is not yours.",
                                  description="Please try again")
            embed.add_field(name="Did you try earning your own coins?",
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


class kikifish(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        print("KikiFish.cog loaded.")

    async def cog_check(self, ctx: commands.Context):
        r = await economy.is_registered(ctx.message.author.id)
        return r

    async def cog_check(self, ctx: commands.Context):
        a = await economy.is_lvlregistered(ctx.message.author.id)
        return a

    @commands.command(aliases=['f', 'fishing', 'kikifish'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def fish(self, ctx: commands.Context):
        view = FView(ctx)
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Welcome to Kiki Fishing Central")
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-respect-fish-bone-flag-cartoon-vector-icon-illustration-animal-nature-icon-concept-isolate_138676-4416.jpg?w=360"
        )
        embed.add_field(
            name="*🐠Chose your adventure!🐠*",
            value=
            "🎣Fishing is single catch. \n 🐡Net is a multiple catch. \n ⚓Sail is a journey for riches!"
        )
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                         icon_url=ctx.message.author.avatar.url)

        await ctx.send(embed=embed, view=view)

        await view.wait()

    @commands.command()
    async def stest(self, ctx: commands.Context):
        a = random.randint(0, 6)
        fail = sailfails[a]

        await ctx.send(f"{fail}")


async def setup(bot):
    await bot.add_cog(kikifish(bot))
