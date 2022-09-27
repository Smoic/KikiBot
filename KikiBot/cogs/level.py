from code import interact
from re import A
from tracemalloc import stop
from turtle import back, clear
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
from easy_pil import *


class LevelView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Level Status",
                       style=discord.ButtonStyle.green,
                       custom_id="lstat",
                       emoji="💎")
    async def lvl1(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "lstat"][0]
        button2 = [x for x in self.children if x.custom_id == "lup"][0]
        button3 = [x for x in self.children if x.custom_id == "quit"][0]
        button1.disabled = False
        button2.disabled = False
        button3.disabled = False

        user = await economy.get_user_lvl(interaction.user.id)
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        curxp = user.xp
        curlvl = user.level
        curpoi = user.points
        curfish = user.fish
        curgamb = user.gamble

        embed.set_author(name="Your Level Status")
        embed.add_field(
            name="Current stats are:",
            value=
            f"💎Xp: {curxp} \n\n 🎯Level: {curlvl} \n\n 🎣Fishing: {curfish} \n\n 🎲Gambling: {curgamb} \n\n 🔮Remaining Skill Points: {curpoi}"
        )
        embed.set_footer(text="Summon invoked by {}".format(
            interaction.user.name),
                         icon_url=(interaction.user.avatar))
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
        )

        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Level Up",
                       style=discord.ButtonStyle.blurple,
                       custom_id="lup",
                       emoji="♦")
    async def lvl2(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "lstat"][0]
        button2 = [x for x in self.children if x.custom_id == "lup"][0]
        button3 = [x for x in self.children if x.custom_id == "quit"][0]
        button1.disabled = False
        button2.disabled = False
        button3.disabled = False

        user = await economy.get_user_lvl(interaction.user.id)
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))

        curxp = user.xp
        curlvl = user.level
        curpoi = user.points
        if curlvl == 0:
            lvlup = 100
        else:
            lvlup = 100 * curlvl

        nlvl = int(curxp / lvlup)
        cxp = curxp - (nlvl * lvlup)
        curlvl = curlvl + nlvl
        curpoi = curpoi + nlvl

        if nlvl == 0:
            embed.set_author(name="Kiki Level System")
            embed.add_field(
                name="You don't have enough experience points to level up.",
                value="Try our minigames to gain more xp!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
            )
            await interaction.response.edit_message(embed=embed)
            return False
        else:
            await economy.add_level(interaction.user.id, "level", nlvl)
            await economy.set_xp(interaction.user.id, "xp", cxp)
            await economy.add_level(interaction.user.id, "points", nlvl)
            embed.set_author(name="Kiki Level System")
            embed.add_field(
                name="You have levelled up!",
                value=
                f"Your current level is now: {curlvl}\n\n Your have gained {nlvl} skill points. \n\n You now have {curpoi} skill points remaining.\n\n Your extra {cxp} xp added back to your progress!"
            )
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
            )
            await interaction.response.edit_message(embed=embed)
            return True

    @discord.ui.button(label="Quit",
                       style=discord.ButtonStyle.red,
                       custom_id="quit",
                       emoji="✖")
    async def lvl3(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        self.clear_items()
        self.stop()
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Come back again!")
        embed.add_field(name="You have quit from the leveling central!",
                        value="Train hard for progress!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                         icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-holding-fish-cartoon-vector-illustration_138676-2210.jpg?w=1380&t=st=1661827195~exp=1661827795~hmac=6423de14f15ffa0896cf57b9f71876cc75e0a069e3222a4e0894e72334a75c96"
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


class SkillView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label='Fishing',
                       style=discord.ButtonStyle.green,
                       emoji="🎣",
                       custom_id="skfish")
    async def skl1(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        user = await economy.get_user_lvl(interaction.user.id)
        curfish = user.fish
        curpoi = user.points

        button1 = [x for x in self.children if x.custom_id == "skfish"][0]
        button2 = [x for x in self.children if x.custom_id == "skgam"][0]
        button3 = [x for x in self.children if x.custom_id == "quit"][0]
        button1.disabled = False
        button2.disabled = False
        button3.disabled = False

        npoints = curpoi - 1
        amount = 1

        if curpoi > 0:
            embed = discord.Embed(color=discord.Color.random())
            embed = discord.Embed(
                title="You choose fishing!",
                description="Your fishing skill has been increased!")
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/cute-cat-rocker-sing-with-guitar-cartoon-vector-icon-illustration-animal-music-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3794.jpg?w=1380"
            )
            embed.set_author(name="Kiki RPS")
            embed.add_field(name=f"Your current fishing skill is {curfish+1}",
                            value=f"You have {curpoi-1} points remaining.")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
            )

            await economy.add_level(interaction.user.id, "fish", amount)
            await economy.set_xp(interaction.user.id, "points", npoints)
            if (curpoi - 1) == 0:
                embed = discord.Embed(color=discord.Color.random())
                embed.add_field(
                    name=f"Your current fishing skill is {curfish+1}",
                    value=f"You have {curpoi-1} points remaining.")
                embed.add_field(
                    name="You don't have any unused skill points left.",
                    value="Please come back when you level up!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
                )
                button1.disabled = True
                button2.disabled = True
                button3.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

                self.value = "1"

        await interaction.response.edit_message(embed=embed, view=self)

        if curpoi == 0:
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(
                name="You don't have any unused skill points left.",
                value="Please come back when you level up!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
            )
            button1.disabled = True
            button2.disabled = True
            button3.disabled = False
            await interaction.response.edit_message(embed=embed, view=self)
            self.value = "1"

    @discord.ui.button(label="Gambling",
                       style=discord.ButtonStyle.blurple,
                       custom_id="skgam",
                       emoji="🎲")
    async def skl2(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        button1 = [x for x in self.children if x.custom_id == "skfish"][0]
        button2 = [x for x in self.children if x.custom_id == "skgam"][0]
        button3 = [x for x in self.children if x.custom_id == "quit"][0]
        button1.disabled = True
        button2.disabled = True
        button3.disabled = False

        user = await economy.get_user_lvl(interaction.user.id)
        curgam = user.gamble
        curpoi = user.points

        button1 = [x for x in self.children if x.custom_id == "skfish"][0]
        button2 = [x for x in self.children if x.custom_id == "skgam"][0]
        button3 = [x for x in self.children if x.custom_id == "quit"][0]
        button1.disabled = False
        button2.disabled = False
        button3.disabled = False

        npoints = curpoi - 1
        amount = 1

        if curpoi > 0:
            embed = discord.Embed(color=discord.Color.random())
            embed = discord.Embed(
                title="You choose gambling!",
                description="Your gambling skill has been increased!")
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/premium-vector/cute-cat-rocker-sing-with-guitar-cartoon-vector-icon-illustration-animal-music-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3794.jpg?w=1380"
            )
            embed.set_author(name="Kiki RPS")
            embed.add_field(name=f"Your current gambling skill is {curgam+1}",
                            value=f"You have {curpoi-1} points remaining.")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
            )

            await economy.add_level(interaction.user.id, "gamble", amount)
            await economy.set_xp(interaction.user.id, "points", npoints)
            if curpoi - 1 == 0:
                embed = discord.Embed(color=discord.Color.random())
                embed.add_field(
                    name=f"Your current gambling skill is {curgam+1}",
                    value=f"You have {curpoi-1} points remaining.")
                embed.add_field(
                    name="You don't have any unused skill points left.",
                    value="Please come back when you level up!")
                embed.set_footer(text="Summon invoked by {}".format(
                    interaction.user.name),
                                 icon_url=(interaction.user.avatar))
                embed.set_thumbnail(
                    url=
                    "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
                )
                button1.disabled = True
                button2.disabled = True
                button3.disabled = False
                await interaction.response.edit_message(embed=embed, view=self)

                self.value = "1"

        await interaction.response.edit_message(embed=embed, view=self)

        if curpoi == 0:
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(
                name="You don't have any unused skill points left.",
                value="Please come back when you level up!")
            embed.set_footer(text="Summon invoked by {}".format(
                interaction.user.name),
                             icon_url=(interaction.user.avatar))
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
            )
            button1.disabled = True
            button2.disabled = True
            button3.disabled = False
            await interaction.response.edit_message(embed=embed, view=self)
            self.value = "2"

    @discord.ui.button(label="Quit",
                       style=discord.ButtonStyle.red,
                       custom_id="quit",
                       emoji="✖")
    async def skl3(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        self.clear_items()
        self.stop()
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Come back again!")
        embed.add_field(name="You have quit from the leveling central!",
                        value="Train hard for progress!")
        embed.set_footer(text=f"Invoked by {interaction.user.name}",
                         icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-holding-fish-cartoon-vector-illustration_138676-2210.jpg?w=1380&t=st=1661827195~exp=1661827795~hmac=6423de14f15ffa0896cf57b9f71876cc75e0a069e3222a4e0894e72334a75c96"
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


class level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        print("Level.cog loaded.")

    async def cog_check(self, ctx: commands.Context):
        a = await economy.is_lvlregistered(ctx.message.author.id)
        return a

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user = message.author
        data = await economy.get_user_lvl(user.id)
        dxp = data.xp
        dlvl = data.level

        if dlvl == 0:
            lvlup = 100
        else:
            lvlup = 100 * dlvl

        if dxp >= lvlup:
            await economy.add_level(user.id, "level", 1)
            nxp = dxp - lvlup
            await economy.set_xp(user.id, "xp", nxp)
            await economy.add_level(user.id, "points", 1)
            embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
            embed.set_author(name="Kiki Leveling Central")
            embed.add_field(
                name=f"{user.name} has levelled up from {dlvl} to {dlvl+1}",
                value=
                f"You can now distribute your points into your stats by using !skill or !s command. \n\nYour excess {nxp} xp added to your current progress. \n\nYou can do !profile or !p command to see your profile card!"
            )
            embed.set_thumbnail(
                url=
                "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
            )
            await message.channel.send(
                f"{user.mention} Congrats on your new level!", embed=embed)

    @commands.command(aliases=['l'])
    async def level(self, ctx: commands.Context):
        view = LevelView(ctx)
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Kiki Leveling Central")
        embed.set_footer(text="Summon invoked by {}".format(
            ctx.message.author.name),
                         icon_url=(ctx.message.author.avatar))
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
        )

        await ctx.send(embed=embed, view=view)

    @commands.group(invoke_without_command=True, aliases=['sk'])
    async def skill(self, ctx: commands.Context):
        user = await economy.get_user_lvl(ctx.message.author.id)
        curpoi = user.points
        view = SkillView(ctx)
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Kiki Leveling Central")
        embed.add_field(
            name="Please choose the skill you want to level up",
            value=f"You have {curpoi} unused skill points remaining.")
        embed.set_footer(text="Summon invoked by {}".format(
            ctx.message.author.name),
                         icon_url=(ctx.message.author.avatar))
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
        )

        await ctx.send(embed=embed, view=view)
        await view.wait()

    @skill.command()
    async def reset(self, ctx: commands.Context):
        user = await economy.get_user(ctx.message.author.id)
        items = user.items
        item = "skill reset"
        item = item.lower()
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))
        embed.set_author(name="Kiki Leveling Central")
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-cat-sitting-book-cartoon-vector-icon-illustration-animal-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4203.jpg?w=1380&t=st=1661481168~exp=1661481768~hmac=640ba6cac721ca3e6c132b840f44b3e7020aebfc5821bbdf672f45c25b7da21b"
        )
        embed.set_footer(text="Summon invoked by {}".format(
            ctx.message.author.name),
                         icon_url=(ctx.message.author.avatar))
        if item in items:
            r = await economy.get_user_lvl(ctx.message.author.id)
            curfish = r.fish
            curgam = r.gamble
            curpoi = r.points
            npoints = curfish + curgam
            await economy.remove_item(ctx.message.author.id, item)
            await economy.set_xp(ctx.message.author.id, "fish", 0)
            await economy.set_xp(ctx.message.author.id, "gamble", 0)
            await economy.add_level(ctx.message.author.id, "points", npoints)
            embed.add_field(
                name="You have successfully reset your skill points!",
                value=
                f"{npoints} added back to your progress. \n You currently have {curpoi+npoints} skill up points remaining."
            )
            await ctx.send(embed=embed)
        else:
            embed.add_field(name="You don't have skill reset item!",
                            value="Try buying it from shop!")
            await ctx.send(embed=embed)

    @commands.command(aliases=['p'])
    async def profile(self, ctx: commands.Context):

        user = ctx.message.author
        r = await economy.get_user_lvl(user.id)
        xp = r.xp
        level = r.level
        points = r.points
        ufish = r.fish
        ugamb = r.gamble

        if level == 0:
            level = 1
        else:
            level = level

        u_data = {
            "name": f"{user.name}#{user.discriminator}",
            "xp": xp,
            "level": level,
            "points": points,
            "fishing": ufish,
            "gambling": ugamb,
            "next_level": 100 * level,
            "points": points,
        }

        background = Editor(Canvas((900, 300), color="#544377"))
        profile_picture = await load_image_async(str(user.avatar.url))
        profile = Editor(profile_picture).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)
        poppins_small2 = Font.poppins(size=25)

        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

        background.polygon(card_right_shape, color="#ABB81F")
        background.paste(profile, (30, 30))

        background.rectangle((30, 240), width=610, height=40, color="#FFFFFF")
        background.bar((10, 240),
                       max_width=650,
                       height=40,
                       percentage=u_data["xp"],
                       color="#282828",
                       radius=20)
        background.text((200, 40),
                        u_data["name"],
                        font=poppins,
                        color="#FFFFFF")

        background.rectangle((200, 100), width=350, height=2, fill="#FFC300")

        background.text(
            (200, 110),
            f"Level - {u_data['level']} | XP - {u_data['xp']}/{u_data['next_level']}",
            font=poppins_small2,
            color="#FFFFFF")
        background.text(
            (200, 150),
            f"Fishing - {u_data['fishing']} | Gambling - {u_data['gambling']} ",
            font=poppins_small2,
            color="#FFFFFF")
        background.text((200, 185),
                        f"Remaining Skill Points - {u_data['points']}",
                        font=poppins_small2,
                        color="#FFFFFF")
        file = discord.File(fp=background.image_bytes,
                            filename="levelcard.png")
        await ctx.send(file=file)


async def setup(bot):
    await bot.add_cog(level(bot))
