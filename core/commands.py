import discord
from discord.ext import commands

from luci.settings import __version__

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Ok!')


@client.command(aliases=['v'])
async def version(discord):
    """
    Pinga o bot para teste sua execução
    """
    await discord.send(__version__)
