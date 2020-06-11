from random import choice

import discord
from discord.ext import commands

from core.output_vectors import offended
from core.utils import validate_text_offense
from luci.settings import __version__, SELF_ID

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Ok!')


@client.event
async def on_message(message):
    """
    Handler para mensagens do chat.
    """
    channel = message.channel
    await client.process_commands(message)

    if message.author.bot:
        return

    text = message.content

    # Verify if message is offensive
    is_offensive = validate_text_offense(text)
    if is_offensive:
        await channel.send(f'{message.author.mention} {choice(offended)}')

    #############################################################
    # Ao mencionar @LUCI
    #############################################################
    if SELF_ID in message.content:
        pass
        # Answer


@client.command(aliases=['v'])
async def version(discord):
    """
    Pinga o bot para teste sua execução
    """
    await discord.send(__version__)
