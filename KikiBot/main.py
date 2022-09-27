from email import message
from imaplib import Commands
from importlib.resources import contents
from time import sleep
import click
import discord
import os
import asyncio
from discord.ext import commands, tasks
from discord.ui import Button, View
import sqlite3
import random
from DiscordEconomy.Sqlite import Economy
import DiscordEconomy
import tracemalloc
import setup
from lists.itemslist import *
from discord.ui import Select, View
from discord import AllowedMentions
import re
import cogs.econ

#Global vars
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
economy = Economy()
TOKEN = (
    "")
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

bot.remove_command("help")


@bot.event
async def on_ready():
    await economy.__is_table_exists()
    print(f'\n{bot.user.name} - {bot.user.id}, has connected to Discord!')


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    print("Loaded Successfully!")


@bot.event
async def on_command_error(ctx: commands.Context, error):
    embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89))

    if isinstance(error, commands.CommandNotFound):
        embed.add_field(name="Error",
                        value="""This command does not exists!""")
        embed.set_author(name="KikiVerse")
        embed.set_thumbnail(
            url=
            "https://img.freepik.com/free-vector/cute-bulb-cat-cartoon_138676-2549.jpg?w=1380&t=st=1662061963~exp=1662062563~hmac=b4f62568c19e7121c0fe975e0191b030c8f4b61e07b7044208916e1e878b02f7"
        )
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.CommandOnCooldown):
        embed.add_field(name="You are on cooldown!",
                        value=f"{round(error.retry_after,1)} seconds left.")
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name="You are missing an argument.", value=error)
        ctx.command.reset_cooldown(ctx)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.BadArgument):
        embed.add_field(name="You have entered a bad argument.", value=error)
        ctx.command.reset_cooldown(ctx)
        await ctx.send(embed=embed, delete_after=5)


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.new_event_loop().run_until_complete(main())
